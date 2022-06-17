// getting the position of the user
function getPosition() {
    let lat = 0,
        lng = 0;
    acc = null;
    const position = (e) => {
        lat = e.coords.latitude;
        lng = e.coords.longitude;
        acc = e.coords.accuracy;
    }
    if (!navigator.geolocation) {
        alert("Geolocation not enable on your divice");
        return {
            lat,
            lng
        }
    } else {
        navigator.geolocation.getCurrentPosition(position);
        return {
            lat,
            lng
        };
    }
}

// Initialising map
function initMap() {

    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionService = new google.maps.DirectionsService();
    const lat = 3,
        lng = 3;
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: {
            lat,
            lng
        }
    });

    directionsRenderer.setMap(map);

    calculateAndDisplayRoute(directionService, directionsRenderer);
    document.getElementById("mode").addEventListener("change", () => {
        calculateAndDisplayRoute(directionService, directionsRenderer);
    });

    var options = {
        types: ["(cities)"],
    };
    var origin = document.getElementById("from");
    var destination = document.getElementById("to");

    auto_complete_origin = new google.maps.places.Autocomplete(
        origin,
        options
    );
    auto_complete_destination = new google.maps.places.Autocomplete(
        destination,
        options
    );
}


// calculate the distance and display route

function calculateAndDisplayRoute(directionService, directionsRenderer) {
    const selectedMode = document.getElementById("mode");

    directionService.route({
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,

        travelMode: google.maps.TravelMode[selectedMode]
    }).then((respone) => {
        directionsRenderer.setDirections(reponse);
    }).catch((err) => {
        alert("Direction Requested Fail! Due to " + err.status);
    });
}


// document.getElementsByTagName("body")[0].addEventListener("load", () => {
//     initMap();
// });