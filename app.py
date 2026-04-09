from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/plan')
def plan():
    return render_template('plan_shipment.html')

@app.route('/tracker')
def tracker():
    return render_template('live_tracker.html')

@app.route('/optimizer')
def optimizer():
    return render_template('route_optimizer.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
