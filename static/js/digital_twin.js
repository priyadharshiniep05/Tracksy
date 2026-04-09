function runDigitalTwinSimulation(orderId, scenario) {
    const btn = document.getElementById('runSimBtn');
    if(btn) btn.innerHTML = '<span class="live-dot mr-2"></span> Running 100 Monte Carlo iterations...';
    
    fetch('/api/digital_twin/simulate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({order_id: orderId, scenario_type: scenario})
    }).then(r => r.json()).then(data => {
        if(btn) btn.innerHTML = 'Run Simulation';
        
        document.getElementById('simResults').classList.remove('hidden');
        document.getElementById('p50eta').innerText = data.p50_eta || 'N/A';
        document.getElementById('p95eta').innerText = data.p95_eta || 'N/A';
        document.getElementById('costImpact').innerText = `$${data.cost_impact_usd || 0}`;
        document.getElementById('recommendation').innerText = data.recommended_action || '';
        
        anime({
            targets: '#simResults .glass-card',
            translateY: [20, 0],
            opacity: [0, 1],
            delay: anime.stagger(100)
        });
    });
}
