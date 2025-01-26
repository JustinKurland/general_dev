from threat_metrix import ThreatMetrixDataExtraction
from datetime import datetime, timedelta

def orchestrate_all_modules(api_key):
    # Get the current system date and define a time window of 1 day
    current_time = datetime.now()
    start_time = (current_time - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    end_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    # Extract data from ThreatMetrix for the time window
    threatmetrix_extractor = ThreatMetrixDataExtraction(api_key)
    threatmetrix_data = threatmetrix_extractor.fetch_threatmetrix_data(start_time, end_time)


    # Combine and return all results in a single dictionary
    return {
        'start_time': start_time,
        'end_time': end_time
    }

if __name__ == "__main__":
    api_key = "your_api_key_here"
    final_results = orchestrate_all_modules(api_key)
    print(final_results)
