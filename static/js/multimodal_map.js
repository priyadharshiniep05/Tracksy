// Draw great circle arc between two lat/lng points (for air routes)
function greatCircleArc(latlng1, latlng2, numPoints=100) {
    const lat1 = latlng1.lat * Math.PI / 180;
    const lon1 = latlng1.lng * Math.PI / 180;
    const lat2 = latlng2.lat * Math.PI / 180;
    const lon2 = latlng2.lng * Math.PI / 180;

    const d = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin((lat1 - lat2) / 2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin((lon1 - lon2) / 2), 2)));
    const pts = [];
    for (let f = 0; f <= 1; f += 1/numPoints) {
        const A = Math.sin((1 - f) * d) / Math.sin(d);
        const B = Math.sin(f * d) / Math.sin(d);
        const x = A * Math.cos(lat1) * Math.cos(lon1) + B * Math.cos(lat2) * Math.cos(lon2);
        const y = A * Math.cos(lat1) * Math.sin(lon1) + B * Math.cos(lat2) * Math.sin(lon2);
        const z = A * Math.sin(lat1) + B * Math.sin(lat2);
        const lat = Math.atan2(z, Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2)));
        const lon = Math.atan2(y, x);
        pts.push([lat * 180 / Math.PI, lon * 180 / Math.PI]);
    }
    return pts;
}

// Draw curved sea lane between ports
function seaLaneCurve(portA, portB) {
    // For simplicity locally returning straight line offset
    const pts = [];
    for(let i=0; i<=10; i++) {
        let f = i/10;
        let lat = portA.lat + (portB.lat - portA.lat)*f;
        let lng = portA.lng + (portB.lng - portA.lng)*f;
        pts.push([lat, lng]);
    }
    return pts;
}

// Animated plane/ship icon that rotates to face direction of travel
function createTransportIcon(mode, heading) {
    let html = `<div style="transform: rotate(${heading}deg); font-size: 20px;">`;
    if(mode === 'air') html += '✈️';
    else if(mode === 'sea') html += '🚢';
    else if(mode === 'rail') html += '🚆';
    else html += '🚚';
    html += '</div>';

    return L.divIcon({
        className: 'custom-div-icon',
        html: html,
        iconSize: [30, 42],
        iconAnchor: [15, 21]
    });
}

// Draw complete multimodal route on map with all legs
function drawMultimodalRoute(map, legs) {
    legs.forEach(leg => {
        let pts;
        if(leg.mode === 'air') {
            pts = greatCircleArc({lat:leg.from[0], lng:leg.from[1]}, {lat:leg.to[0], lng:leg.to[1]});
        } else if (leg.mode === 'sea') {
            pts = seaLaneCurve({lat:leg.from[0], lng:leg.from[1]}, {lat:leg.to[0], lng:leg.to[1]});
        } else {
            pts = [leg.from, leg.to];
        }
        
        L.polyline(pts, {
            color: leg.mode === 'air' ? '#635BFF' : leg.mode === 'sea' ? '#0EA5E9' : '#00D4C8',
            weight: 3,
            dashArray: leg.mode === 'sea' ? '10, 10' : ''
        }).addTo(map);
    });
}

// Draw disruption circle overlays
function drawDisruptionOverlays(map, disruptions) {
    disruptions.forEach(d => {
        const color = d.severity === 'critical' ? '#EF4444' : d.severity === 'high' ? '#F59E0B' : '#0EA5E9';
        L.circle([d.lat, d.lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.3,
            radius: d.radius_km * 1000
        }).bindPopup(`<b>${d.title}</b><br>${d.description}`).addTo(map);
    });
}

// Animate marker smoothly between two points
function smoothMoveMarker(marker, fromLatlng, toLatlng, durationMs) {
    let start = null;
    const latDiff = toLatlng[0] - fromLatlng[0];
    const lngDiff = toLatlng[1] - fromLatlng[1];

    function step(timestamp) {
        if (!start) start = timestamp;
        let progress = timestamp - start;
        let p = Math.min(progress / durationMs, 1);
        
        let currentLat = fromLatlng[0] + latDiff * p;
        let currentLng = fromLatlng[1] + lngDiff * p;
        
        marker.setLatLng([currentLat, currentLng]);

        if (progress < durationMs) {
            window.requestAnimationFrame(step);
        }
    }
    window.requestAnimationFrame(step);
}
