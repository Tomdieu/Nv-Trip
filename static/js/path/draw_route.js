/*
*   
* map : map object
* origin,destination : Object {coordonates}
* origin:{
    "name":[],
    "coordinates":[]
}
*
*/
function drawRoute(map, origin, destination) {


    var coords = [
        origin.coords,
        destination.coords
    ]

    console.log({ coords });
    console.log(coords[0]);
    console.log(coords[1]);

    var drive_depart_marker = new mapboxgl.Marker()
        .setLngLat(coords[0])
        .addTo(map);

    var driver_arival_marker = new mapboxgl.Marker()
        .setLngLat(coords[1])
        .addTo(map);

    drive_depart_marker.setPopup(
        new mapboxgl.Popup({ offset: 25 }) // add popups
        .setHTML(origin.name)
    )


    // Create a default Marker, colored black, rotated 45 degrees.
    driver_arival_marker = new mapboxgl.Marker({ color: 'black' })
        .setLngLat(coords[1])
        .addTo(map);


    driver_arival_marker.setPopup(
        new mapboxgl.Popup({ offset: 25 }) // add popups
        .setHTML(destination.name)
    )

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
            instructions.insertAdjacentHTML('beforeend', `<div class='flx'><div class='ctr'><i class='bi bi-arrow-90deg-${step.driving_side}'></i></div><div>${step.maneuver.instruction}</div> </div>`);
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


        });
        map.on('style.load', function() {
            addRoutes(coords);
        });
        // map.on('styledata', () => {
        //     const waiting = () => {
        //         if (!map.isStyleLoaded()) {
        //             setTimeout(waiting, 200);
        //         } else {
        //             addRoutes(coords);

        //             return;
        //         }
        //     };
        //     waiting();
        // });

    }
    xmlhttp.send();


    function addRoutes(coords) {



        if (map.getSource('route')) {
            map.removeLayer('route');
            map.removeSource('route');
        } else {
            const { coordinates } = coords;
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