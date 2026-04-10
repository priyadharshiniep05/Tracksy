/**
 * Tracksy Simulation Demo Engine
 * Manages automated vehicle movement and disruption triggers
 */

const SimulationEngine = {
    isActive: false,
    interval: null,

    toggle() {
        this.isActive = !this.isActive;
        const btn = document.getElementById('btn-simulation');
        if (this.isActive) {
            btn.classList.add('bg-teal', 'text-navy');
            btn.innerText = 'Demo Mode: ON';
            this.start();
        } else {
            btn.classList.remove('bg-teal', 'text-navy');
            btn.innerText = 'Demo Mode: OFF';
            this.stop();
        }
    },

    start() {
        console.log('Simulation started.');
        this.interval = setInterval(async () => {
            // Fetch live positions from backend
            try {
                const data = await Tracksy.fetch('/tracking/live');
                // Normally we'd use EventSource, but for simulation demo,
                // we'll just poll or handle the stream via WebSocket
                if (typeof mapManager !== 'undefined') {
                    mapManager.updateVehiclePositions(data);
                }
            } catch (e) {
                console.error('Simulation poll failed', e);
            }
        }, 3000);
    },

    stop() {
        console.log('Simulation stopped.');
        if (this.interval) clearInterval(this.interval);
    },

    async triggerDisruption() {
        try {
            const result = await Tracksy.fetch('/disruptions/simulate', { method: 'POST' });
            Tracksy.toast(`🚨 Disruption Triggered: ${result.description}`, 'error');
            
            // Broadcast via WebSocket (simulated)
            if (typeof wsClient !== 'undefined' && wsClient.socket) {
                wsClient.socket.send(JSON.stringify({
                    type: 'disruption_event',
                    ...result
                }));
            }
        } catch (e) {
            Tracksy.toast('Simulation error', 'error');
        }
    }
};
