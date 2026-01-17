from datetime import datetime

def run_ai_risk_check(lat, lng):
    hour = datetime.now().hour

    if hour >= 22 or hour <= 5:
        return "High", "Late night risk detected"

    if 12.0 <= lat <= 13.0 and 77.0 <= lng <= 78.0:
        return "Medium", "Isolated area detected"

    return "Low", "Area appears safe"
