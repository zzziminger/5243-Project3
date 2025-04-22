from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account
import csv

# === Your Setup ===
PROPERTY_ID = "485718616"
KEY_PATH = "ds-proj3-1266855cca6b.json" #if you want to run this contact me for this file
START_DATE = "2025-01-01"
END_DATE = "2025-04-22"
OUTPUT_CSV = "ga4_detailed_event_report_2.csv"

# Authenticate
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=credentials)

# Build the request
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[
        Dimension(name="eventName"),
        Dimension(name="date"),
        Dimension(name="city"),
        Dimension(name="country"),
        Dimension(name="deviceCategory"),
        Dimension(name="browser"),
        Dimension(name="sessionSourceMedium"),
        Dimension(name="pagePath"),
    ],
    metrics=[
        Metric(name="eventCount"),
        Metric(name="userEngagementDuration"),
        Metric(name="engagedSessions"),
        Metric(name="screenPageViews")
    ],
    date_ranges=[DateRange(start_date=START_DATE, end_date=END_DATE)]
)

# Run the report
response = client.run_report(request)

# Save to CSV
with open(OUTPUT_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write headers
    headers = [dim.name for dim in request.dimensions] + [met.name for met in request.metrics]
    writer.writerow(headers)

    # Write data rows
    for row in response.rows:
        row_data = [dim.value for dim in row.dimension_values] + [met.value for met in row.metric_values]
        writer.writerow(row_data)

print(f"Exported {len(response.rows)} rows to {OUTPUT_CSV}")
