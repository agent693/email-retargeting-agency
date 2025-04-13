class AnalyticsAgent:
    def analyze_clicks(self, delivery_results):
        return [result for result in delivery_results if result["clicked"]]
