/**
 * Tracksy Charts Wrapper
 * Chart.js configurations for analytics
 */

const ChartManager = {
    colors: {
        teal: '#00D4C8',
        danger: '#EF4444',
        info: '#3B82F6',
        slate: '#1E3A5F',
        text: '#94A3B8'
    },

    initDelayTrends(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.day),
                datasets: [
                    {
                        label: 'Traffic',
                        data: data.map(d => d.traffic),
                        borderColor: this.colors.teal,
                        tension: 0.4,
                        fill: true,
                        backgroundColor: 'rgba(0, 212, 200, 0.1)'
                    },
                    {
                        label: 'Weather',
                        data: data.map(d => d.weather),
                        borderColor: this.colors.danger,
                        tension: 0.4
                    }
                ]
            },
            options: this.getCommonOptions('Delay Trends by Category')
        });
    },

    initCostBreakdown(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.mode),
                datasets: [{
                    label: 'Cost (USD)',
                    data: data.map(d => d.cost),
                    backgroundColor: [this.colors.teal, this.colors.info, this.colors.slate, this.colors.danger]
                }]
            },
            options: this.getCommonOptions('Cost Breakdown by Mode')
        });
    },

    initCarbonStats(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.mode),
                datasets: [{
                    data: data.map(d => d.emissions),
                    backgroundColor: [this.colors.teal, this.colors.info, this.colors.slate, this.colors.danger],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: this.colors.text } }
                }
            }
        });
    },

    getCommonOptions(title) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: this.colors.text } },
                title: { display: false, text: title, color: 'white' }
            },
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: this.colors.text } },
                x: { grid: { display: false }, ticks: { color: this.colors.text } }
            }
        };
    }
};
