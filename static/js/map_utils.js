function initMap(elementId, centerLat = 20.5937, centerLng = 78.9629, zoom = 5) {
    const map = L.map(elementId).setView([centerLat, centerLng], zoom);
    
    // Check if dark mode
    const isDark = document.documentElement.classList.contains('dark');
    
    const tileUrl = isDark ? 
        'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png' : 
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        
    L.tileLayer(tileUrl, {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    
    return map;
}

function addOrderMarker(map, orderId, lat, lng, type='truck', color='teal') {
    const colors = {
        'teal': '#00D4C8',
        'orange': '#F59E0B',
        'red': '#EF4444',
        'green': '#10B981'
    };
    
    const iconHtml = `<div class="map-marker-pulse" style="background-color: ${colors[color]}; border: 2px solid white; box-shadow: 0 0 10px ${colors[color]}"></div>`;
    
    const customIcon = L.divIcon({
        html: iconHtml,
        className: '',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
    
    const marker = L.marker([lat, lng], {icon: customIcon}).addTo(map);
    marker.bindPopup(`<b>Order:</b> ${orderId}`);
    return marker;
}

function drawRoute(map, waypoints, color = '#00D4C8') {
    if(!waypoints || waypoints.length < 2) return null;
    const polyline = L.polyline(waypoints, {color: color, weight: 3, dashArray: '5, 5'}).addTo(map);
    map.fitBounds(polyline.getBounds(), {padding: [50, 50]});
    return polyline;
}

function addOriginDestMarkers(map, oLat, oLng, dLat, dLng) {
    L.marker([oLat, oLng]).addTo(map).bindPopup("Origin");
    L.marker([dLat, dLng]).addTo(map).bindPopup("Destination");
}
