var map = null;

mapboxgl.accessToken = token;

console.log(token);

navigator.geolocation.getCurrentPosition((pos) => {
    let lat, lng, accuracy;
    lat = pos.coords.latitude,
        lng = pos.coords.longitude,
        accuracy = pos.coords.accuracy;
    console.log('Position', {
        lat,
        lng,
        accuracy
    })
    setUpMap({
        lat,
        lng,
        accuracy
    })
}, () => {
    let {
        lat,
        lng
    } = {
        lat: 3.866667,
        lng: 11.516667
    };
    let accuracy = 2;
    setUpMap({
        lng,
        lat,
        accuracy
    });
})

function setUpMap({
    lat,
    lng,
    accuracy
}) {
    map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v11",
        center: [lng, lat],
        zoom: 10
    })

    const nav = new mapboxgl.NavigationControl()
    map.addControl(nav)

    map.on('click', (e) => {
        console.log(e)
        marker = new mapboxgl.Marker()
        marker.setLngLat(e.lngLat)
        marker.addTo(map)
    })

    map.on('move', (e) => {
        console.log(map.getBounds())
    })
}

const origin_geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    types: 'country,region,place,postcode,locality,neighborhood,poi,address,district',

    // types: 'country,region,place,postcode,locality,neighborhood',
    placeholder: 'Enter the Origin'
});

origin_geocoder.addTo('#origin')

const destination_geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    types: 'country,region,place,postcode,locality,neighborhood,poi,address,district',

    // types: 'country,region,place,postcode,locality,neighborhood',
    placeholder: 'Enter The Destination'
})

destination_geocoder.addTo('#destination')

const search_geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    types: 'country,region,place,postcode,locality,neighborhood,poi,address,district',
    placeholder: 'Search A Place or Address ...',
    mapboxgl: mapboxgl,
    country: 'cm'
    // bbox: [10.2309250601938, 3.12103306360487, 13.2473659999523, 6.26028399968965],
    // proximity: {
    //     longitude: 11.52028,
    //     latitude: 3.86139
    // }

})

search_geocoder.addTo('#search')


search_geocoder.on('result', (e) => {
    dt = JSON.stringify(e.result);
    data = JSON.parse(dt)
    center = data["center"];
    console.log(dt)
    // This make an animation to when moving to the search position
    map.flyTo({
        center: center,
        essential: true,
        zoom: 14
    })

})

// const apiKey = "AAPK77166738bb3b4a919246a91ee39f974asYwya5YTeUz9piFikqfoeCdI0EF-3l-fqzFJIaMjCjoqQra8qVTHG3hIVdFROjZ6";

// const basemapEnum = "ArcGIS:Navigation";

// const map = new mapboxgl.Map({
//     container: "map",
//     style: `https://basemaps-api.arcgis.com/arcgis/rest/services/styles/${basemapEnum}?type=style&token=${apiKey}`,
//     zoom: 13,

//     center: [-122.4194, 37.7749] // San Francisco

// });

// map.once("load", () => {

//     map.addSource("places", {
//         type: "geojson",
//         data: {
//             type: "FeatureCollection",
//             features: []
//         }
//     });

//     map.addLayer({
//         id: "places-circle",
//         source: "places",
//         type: "circle",

//         paint: {
//             "circle-color": "hsla(200, 80%, 80%, 0.7)",
//             "circle-stroke-color": "hsl(200, 80%, 40%)",
//             "circle-stroke-width": 1,
//             "circle-radius": 3
//         }
//     });

//     map.addLayer({
//         id: "places-text",
//         source: "places",
//         type: "symbol",
//         layout: {
//             "text-field": ["get", "PlaceName"],
//             "text-font": ["Arial Bold"],
//             "text-variable-anchor": ["left", "right"],
//             "text-justify": "left",
//             "text-radial-offset": 0.5
//         },
//         paint: {
//             "text-color": "hsl(200, 80%,40%)",
//             "text-halo-color": "white",
//             "text-halo-width": 2
//         }
//     });

//     showPlaces();

// });

// function showPlaces() {

//     const authentication = arcgisRest.ApiKeyManager.fromKey(apiKey);

//     const category = document.getElementById("places-select").value;
//     if (!category) {
//         return;
//     }
//     arcgisRest
//         .geocode({
//             authentication,
//             outFields: "Place_addr,PlaceName",

//             params: {
//                 category,
//                 location: map.getCenter().toArray().join(","),
//                 maxLocations: 25
//             }
//         })

//         .then((response) => {
//             map.getSource("places").setData(response.geoJson);
//         })

//         .catch((error) => {
//             alert("There was a problem using the geocoder. See the console for details.");
//             console.error(error);
//         });

// }

// document.getElementById("places-select").addEventListener("change", showPlaces);