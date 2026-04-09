const socket = io();

socket.on('connect', () => {
    console.log('Socket connected.');
});

socket.on('location_updated', (data) => {
    // Expected structure: {order_id, lat, lng, progress_percent, speed_kmh, next_waypoint}
    const evt = new CustomEvent('trackingUpdate', { detail: data });
    window.dispatchEvent(evt);
});

socket.on('order_status_changed', (data) => {
    // Update local UI
    // Example: change pill status
});

socket.on('delay_detected', (data) => {
    alert(`Order ${data.order_id} delayed: ${data.message}`);
});

socket.on('disruption_alert', (data) => {
    const banner = document.getElementById('disruptionBanner');
    if(banner) {
        banner.classList.remove('hidden');
        document.getElementById('disruptTitle').innerText = data.title;
        document.getElementById('disruptDesc').innerText = data.description;
    }
});
