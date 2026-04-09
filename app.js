// Global Javascript for Vanilla implementations (if needed)

// Color constants for javascript use
const COLORS = {
    success: '#00ff88',
    warning: '#ffaa00',
    danger: '#ff4444',
    accent: '#00d4ff'
};

// Utility to create Leaflet glowing markers in Vanilla JS
function createGlowMarker(color) {
    return L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="background-color: ${color}; width: 15px; height: 15px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px ${color}"></div>`,
        iconSize: [15, 15],
        iconAnchor: [7.5, 7.5]
    });
}

function createPulseGlowMarker(color) {
    return L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 15px ${color}; animation: pulseGlow 1.5s infinite;"></div>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
}
