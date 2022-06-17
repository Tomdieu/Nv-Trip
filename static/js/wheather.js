const searchWrapper = document.querySelector('.search-input');
const inputBox = document.querySelector('.place');
const suggBox = document.querySelector('.autocom-box');

const frm = document.querySelector('form');

frm.onsubmit = (e) =>{
    e.preventDefault();
}


// using mapbox to display the map


mapboxgl.accessToken = mapbox_token;
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [11.5532631, 3.8799389], // starting position [lng, lat]
    zoom: 15 // starting zoom
});


map.on('move',(e)=>{
    // console.log(map.getBounds())
    var bounds = map.getBounds();
    const sw = bounds._sw;
    const ne = bounds._ne;
    var center = map.getCenter();
    // console.log(center);
    // console.log(sw,ne);
    displayWheather(center.lat,center.lng);
})

function displayWheather(lat,lng){
    const options = {
        method: 'GET',
        headers: {
            'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com',
            'X-RapidAPI-Key': '10c1e7adbemshcfbf5031185c1c6p1702afjsn717f338b7ab3'
        }
    };

    fetch(`https://community-open-weather-map.p.rapidapi.com/find?&lon=${lng}&lat=${lat}`, options)
        .then(response => response.json())
        .then(response => {
            console.log(response);
            const data = response;
            console.log(data);
            data?.list?.map((data,i)=>{
               
                const el = document.createElement('div');
                el.className = 'marker';
                el.style.width = '44px';
                el.style.height = '44px';
                el.style.backgroundClip = 'red';

                const img = document.createElement('img');
                imgUrl = `https://openweathermap.org/img/w/${data.weather[0].icon}.png`;
                img.setAttribute('src',imgUrl);
                el.appendChild(img);
                new mapboxgl.Marker(el)
                    .setLngLat([lng,lat])
                    .addTo(map);
                 console.log(el);
            })
        })
        .catch(err => console.error(err));
}


async function getData(text) {
    try {
        url = `http://api.positionstack.com/v1/forward?access_key=${ps_token}&query=${text}&limit=7`;
        let res = await fetch(url);
        return await res.json();
    } catch (error) {

    }
}



inputBox.addEventListener('input', async (e) => {
    let userData = e.target.value;
    userData = userData.toLowerCase();
    let emptyArray = [];
    // console.log(e);
    if (userData) {
        // emptyArray = sugg.filter((dt) => {
        //     return dt.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        // });
       

        if(userData.length >= 3){
            var places = await getData(userData);

            var data = places.data;

            console.log({data})
           

             emptyArray = data.map((dt) => {
                 // return data = '<li>' + dt + '</li>';
                 return data = '<button>' + dt['label'] + '</button>';

             })

            // console.log(emptyArray);
            searchWrapper.classList.add('active');
            showSuggestion(emptyArray);
            // list = suggBox.querySelectorAll('li');
            list = suggBox.querySelectorAll('button');

            // console.log(list);
            list.forEach(element => {
                element.addEventListener('click',(e) => {
                    inputBox.value = e.target.textContent;
                    searchWrapper.classList.remove('active');
                    var coordinates;
                    url = `http://api.positionstack.com/v1/forward?access_key=${ps_token}&query=${inputBox.value}&limit=1`;
                    var xml = new XMLHttpRequest();
                    xml.responseType = 'json';
                    xml.onreadystatechange = function (){
                        if(this.readyState == 4 && this.status == 200){
                            // console.log(this.response);
                            coordinates = this.response.data;
                            // console.log(coordinates);
                            const [latitude, longitude] = [coordinates[0].latitude,coordinates[0].longitude];
                            // console.log(latitude,longitude)
                            displayWheather(latitude, longitude);
                            map.flyTo({
                                center:[longitude,latitude],
                                zoom:15,
                                essential: true,
                                speed:1,
                                bearing: 0,
                            })
                        }
                    }
                    xml.open('GET',url,true);
                    xml.send();
                });
            });

        }

        
    } else {
        searchWrapper.classList.remove('active');

    }


})

function showSuggestion(list) {
    let listData;
    // console.log({list});
    if (list.length == 0) {
        userValue = inputBox.value;
        listData = '<button>' + userValue + '</button>';
        // console.log(listData);
    } else {
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}



























// const data = null;

// const xhr = new XMLHttpRequest();
// xhr.withCredentials = true;

// xhr.addEventListener("readystatechange", function () {
//     if (this.readyState === this.DONE) {
//         console.log(this.responseText);
//     }
// });

// xhr.open("GET", "https://travel-advisor.p.rapidapi.com/restaurants/list-in-boundary?bl_latitude=11.847676&tr_latitude=12.838442&bl_longitude=109.095887&tr_longitude=109.149359&restaurant_tagcategory_standalone=10591&restaurant_tagcategory=10591&limit=30&currency=USD&open_now=false&lunit=km&lang=en_US");
// xhr.setRequestHeader("X-RapidAPI-Host", "travel-advisor.p.rapidapi.com");
// xhr.setRequestHeader("X-RapidAPI-Key", "10c1e7adbemshcfbf5031185c1c6p1702afjsn717f338b7ab3");

// xhr.send(data);
