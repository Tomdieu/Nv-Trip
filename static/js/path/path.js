// creating the map

// var map = null;

mapboxgl.accessToken = mapbox_token;
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [11.5532631, 3.8799389], // starting position [lng, lat]
    zoom: 15 // starting zoom
});
map.addControl(new mapboxgl.FullscreenControl({ container: document.querySelector('body') }));

map.addControl(new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    trackUserLocation: true,
    showUserHeading: true
}));

const nav = new mapboxgl.NavigationControl({ visualizePitch: true });
map.addControl(nav, 'bottom-right');


var results = data;

if (results) {

    var coords = [
            [origin_coordinates.lng, origin_coordinates.lat],
            [destination_coordinates.lng, destination_coordinates.lat]
        ]
        // var coords = [
        // 	[origin_coordinates.lat,origin_coordinates.lng],
        // 	[destination_coordinates.lat,destination_coordinates.lng]
        // ]

    console.log(coords);

    // Create a default Marker and add it to the map.
    const marker1 = new mapboxgl.Marker()
        .setLngLat(coords[0])
        .addTo(map);

    marker1.setPopup(
        new mapboxgl.Popup({ offset: 25 }) // add popups
        .setHTML(document.getElementsByName('origin')[0].value)
    )


    // Create a default Marker, colored black, rotated 45 degrees.
    const marker2 = new mapboxgl.Marker({ color: 'black' })
        .setLngLat(coords[1])
        .addTo(map);


    marker2.setPopup(
        new mapboxgl.Popup({ offset: 25 }) // add popups
        .setHTML(document.getElementsByName('destination')[0].value)
    )

    console.log(coords)

    var instructions = document.querySelector('#instructions');

    coords = coords.join(';');
    let url = `https://api.mapbox.com/directions/v5/mapbox/${profile}/${coords}?geometries=geojson&language=en&overview=simplified&steps=true&access_token=${mapboxgl.accessToken}`;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.responseType = 'json';
    xmlhttp.open('GET', url, true);
    xmlhttp.onload = () => {
        var jsonResponse = xmlhttp.response;
        console.log({ jsonResponse })
        var dist = jsonResponse.routes[0].distance * 0.001;
        var dur = jsonResponse.routes[0].duration / 60;
        var steps = jsonResponse.routes[0].legs[0].steps;
        var coords = jsonResponse.routes[0].geometry;
        // console.log(steps.intersections);
        console.log(coords);
        console.log({ steps });

        steps.forEach((step, index) => {
            instructions.insertAdjacentHTML('beforeend', `<div><div class='flx'><div class='ctr'><i class='bi bi-arrow-90deg-${step.driving_side}'></i></div>${step.driving_side}<div>${step.maneuver.instruction}</div> </div></div>`);
            // instructions.insertAdjacentHTML('beforeend', '<p>' + step.driving_side + ' ' + step.maneuver.instruction + '</p>');
            let txt = step.driving_side;
            const { coordinates } = step['geometry'];
        })

        document.getElementById('distance').innerText = 'Distance : ' + dist.toFixed(2) + ' Km';

        document.getElementById('time').innerText = 'Duration : ' + dur.toFixed(2) + ' Min';
        map.on('load', () => {
            // Insert the layer beneath any symbol layer.
            const layers = map.getStyle().layers;
            const labelLayerId = layers.find(
                (layer) => layer.type === 'symbol' && layer.layout['text-field']
            ).id;

            // The 'building' layer in the Mapbox Streets
            // vector tileset contains building height data
            // from OpenStreetMap.
            map.addLayer({
                    'id': 'add-3d-buildings',
                    'source': 'composite',
                    'source-layer': 'building',
                    'filter': ['==', 'extrude', 'true'],
                    'type': 'fill-extrusion',
                    'minzoom': 15,
                    'paint': {
                        'fill-extrusion-color': '#aaa',

                        // Use an 'interpolate' expression to
                        // add a smooth transition effect to
                        // the buildings as the user zooms in.
                        'fill-extrusion-height': [
                            'interpolate', ['linear'],
                            ['zoom'],
                            15,
                            0,
                            15.05, ['get', 'height']
                        ],
                        'fill-extrusion-base': [
                            'interpolate', ['linear'],
                            ['zoom'],
                            15,
                            0,
                            15.05, ['get', 'min_height']
                        ],
                        'fill-extrusion-opacity': 0.6
                    }
                },
                labelLayerId
            );
        });

        /** The following line sare use to ensure that the style load first before 
        the route is draw on the map
        */ 
        // map.on('style.load', function () {
        // 	addRoutes(coords);
        // });
        map.on('styledata', () => {
            const waiting = () => {
                if (!map.isStyleLoaded()) {
                    setTimeout(waiting, 200);
                } else {
                    addRoutes(coords);

                    return;
                }
            };
            waiting();
        });

    }
    xmlhttp.send();


    function addRoutes(coords) {



        if (map.getSource('route')) {
            map.removeLayer('route');
            map.removeSource('route');
        } else {
            const { coordinates } = coords;
            // const camera = map.getFreeCameraOptions();

            // const position = coordinates[0];
            // const altitude = 45;

            // camera.position = mapboxgl.MercatorCoordinate.fromLngLat(position, altitude);
            // camera.lookAtPoint(coordinates[coordinates.length-1]);

            // map.setFreeCameraOptions(camera);
            map.flyTo({
                center: coordinates[0],
                essential: true,
                spedd: 0.2,

            });
            console.log('has enter');
            map.addSource('route', {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': coordinates
                    }
                }
            });
            map.addLayer({
                'id': 'route',
                'type': 'line',
                'source': 'route',
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': '#1db7dd',
                    'line-width': 8,
                    "line-opacity": 0.8

                }
            });
        }
    }

    function removeRoute() {
        if (map.getSource('route')) {
            map.removeLayer('route');
            map.removeSource('route');
            instructions.innerHTML = '';
        } else {
            return;
        }
    }

}