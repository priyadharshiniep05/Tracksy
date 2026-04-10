/**
 * Tracksy Multimodal Logic
 * Segment routing + vehicle icon switching
 */

const MultimodalManager = {
    // Port hub dictionary matches backend seed data
    PORTS: {
        Mumbai: [19.0760, 72.8777],
        Chennai: [13.0827, 80.2707],
        Kolkata: [22.5726, 88.3639],
        Hamburg: [53.5511, 9.9937],
        Rotterdam: [51.9244, 4.4777],
    },

    AIRPORTS: {
        Delhi: [28.7041, 77.1025],
        Dubai: [25.2048, 55.2708],
        London: [51.5074, -0.1278],
        JFK: [40.7128, -74.0060],
    },

    findNearestHub(lat, lon, hubDict) {
        let nearest = null;
        let minDist = Infinity;
        
        for (const [name, coords] of Object.entries(hubDict)) {
            const dist = Math.sqrt((lat - coords[0])**2 + (lon - coords[1])**2);
            if (dist < minDist) {
                minDist = dist;
                nearest = { name, coords };
            }
        }
        return nearest;
    },

    buildMultimodalRoute(origin, dest, mode) {
        const segments = [];
        
        if (mode === 'AIR') {
            const startAirport = this.findNearestHub(origin.lat, origin.lon, this.AIRPORTS);
            const endAirport = this.findNearestHub(dest.lat, dest.lon, this.AIRPORTS);
            
            segments.push({ mode: 'ROAD', from: origin, to: startAirport.coords });
            segments.push({ mode: 'AIR', from: startAirport.coords, to: endAirport.coords });
            segments.push({ mode: 'ROAD', from: endAirport.coords, to: dest });
        } else if (mode === 'SEA') {
            const startPort = this.findNearestHub(origin.lat, origin.lon, this.PORTS);
            const endPort = this.findNearestHub(dest.lat, dest.lon, this.PORTS);
            
            segments.push({ mode: 'ROAD', from: origin, to: startPort.coords });
            segments.push({ mode: 'SEA', from: startPort.coords, to: endPort.coords });
            segments.push({ mode: 'ROAD', from: endPort.coords, to: dest });
        } else {
            segments.push({ mode: 'ROAD', from: origin, to: dest });
        }
        
        return segments;
    }
};
