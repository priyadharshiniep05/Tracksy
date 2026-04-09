function initAllCharts(data) {
    if(!document.getElementById('ordersChart')) return;
    
    const isDark = document.documentElement.classList.contains('dark');
    const textColor = isDark ? '#F9FAFB' : '#111827';
    
    Chart.defaults.color = textColor;
    Chart.defaults.font.family = 'Inter';

    new Chart(document.getElementById('ordersChart'), {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Orders',
                data: data.orders_per_day,
                borderColor: '#00D4C8',
                backgroundColor: 'rgba(0, 212, 200, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Revenue ($)',
                data: data.revenue_per_day,
                borderColor: '#635BFF',
                backgroundColor: 'transparent',
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true },
                y1: { type: 'linear', display: true, position: 'right' }
            }
        }
    });

    if(document.getElementById('statusChart')) {
        new Chart(document.getElementById('statusChart'), {
            type: 'doughnut',
            data: {
                labels: ['Delivered', 'In Transit', 'Delayed', 'Pending'],
                datasets: [{
                    data: data.status_dist,
                    backgroundColor: ['#10B981', '#00D4C8', '#F59E0B', '#6B7280'],
                    borderWidth: 0
                }]
            },
            options: { cutout: '70%'}
        });
    }
}
