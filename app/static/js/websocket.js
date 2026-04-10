/**
 * Tracksy WebSocket Client
 * Real-time updates push to DOM and Map
 */

class WebSocketClient {
    constructor() {
        this.socket = null;
        this.room = 'admin'; // default
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect(room = 'admin') {
        this.room = room;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${room}`;

        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => {
            console.log(`Connected to WebSocket room: ${room}`);
            this.reconnectAttempts = 0;
            const dot = document.getElementById('ws-status-dot');
            if (dot) dot.style.backgroundColor = '#00D4C8';
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            const dot = document.getElementById('ws-status-dot');
            if (dot) dot.style.backgroundColor = '#EF4444';
            
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                const timeout = Math.pow(2, this.reconnectAttempts) * 1000;
                setTimeout(() => {
                    this.reconnectAttempts++;
                    this.connect(this.room);
                }, timeout);
            }
        };
    }

    handleMessage(message) {
        // Dispatch to appropriate trackers or dashboards
        console.log('WS Message Received:', message);
        
        if (message.type === 'disruption_event') {
            this.showDisruptionBanner(message);
        }
        
        if (message.type === 'position_update' && typeof mapManager !== 'undefined') {
            mapManager.addAnimatedMarker(message);
        }
        
        if (message.type === 'new_alert') {
            Tracksy.toast(`🚨 ${message.body}`, message.severity === 'critical' ? 'error' : 'warn');
        }
    }

    showDisruptionBanner(message) {
        const banner = document.getElementById('disruption-banner');
        if (banner) {
            banner.innerHTML = `⚠️ ${message.description} — Affected Orders: ${message.affected_orders_count}`;
            banner.style.display = 'block';
            banner.classList.add('fade-in');
        }
    }
}

const wsClient = new WebSocketClient();
