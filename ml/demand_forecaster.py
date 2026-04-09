import datetime

class DemandForecaster:
    def forecast_demand(self, corridor, days=7):
        base_date = datetime.datetime.now()
        forecasts = []
        for d in range(days):
            date_str = (base_date + datetime.timedelta(days=d)).strftime('%Y-%m-%d')
            forecasts.append({'date': date_str, 'predicted_orders': 20 + d*2, 'confidence': 0.85})
        return forecasts
