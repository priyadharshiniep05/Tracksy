/**
 * Tracksy Map Manager
 * Leaflet integration, animated markers, route drawing
 */

class MapManager {
    constructor(containerId) {
        this.containerId = containerId;
        this.map = null;
        this.markers = {};
        this.routes = {};
        this.ports = [];
        this.airports = [];
    }

    init(options = { center: [20, 78], zoom: 5 }) {
        this.map = L.map(this.containerId).setView(options.center, options.zoom);
        
        // Use CartoDB Dark Matter for a premium dark look
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(this.map);

        return this;
    }

    // Custom SVG Icons
    getIcon(mode) {
        const icons = {
            road: '🚚',
            air: '✈️',
            sea: '🚢',
            rail: '🚆',
            multimodal: '📦'
        };
        return L.divIcon({
            html: `<div class="marker-icon text-2xl filter drop-shadow-lg">${icons[mode] || icons.road}</div>`,
            className: 'custom-div-icon',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
    }

    addAnimatedMarker(order) {
        const { id, lat, lon, mode, tracking_id } = order;
        const icon = this.getIcon(mode.toLowerCase());
        
        if (this.markers[id]) {
            this.markers[id].setLatLng([lat, lon]);
        } else {
            const marker = L.marker([lat, lon], { icon }).addTo(this.map);
            marker.bindPopup(`<b>Order: ${tracking_id}</b><br>Status: IN TRANSIT<br>Mode: ${mode}`);
            this.markers[id] = marker;
        }
        return this.markers[id];
    }

    drawRoute(origin, dest, color = '#00D4C8') {
        const points = [
            [origin.lat, origin.lon],
            [dest.lat, dest.lon]
        ];
        const line = L.polyline(points, {
            color: color,
            weight: 3,
            opacity: 0.6,
            dashArray: '10, 10',
            lineJoin: 'round'
        }).addTo(this.map);
        
        this.map.fitBounds(line.getBounds(), { padding: [50, 50] });
        return line;
    }

    updateVehiclePositions(data) {
        data.forEach(order => {
            this.addAnimatedMarker(order);
        });
    }

    // Mathematical interpolation for smooth movement simulation
    interpolate(p1, p2, fraction) {
        return [
            p1[0] + (p2[0] - p1[0]) * fraction,
            p1[1] + (p2[1] - p1[1]) * fraction
        ];
    }
}

const mapManager = new MapManager('live-fleet-map');
