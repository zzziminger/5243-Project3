
# Google Analytics Data Collection (via API)

## Background

Initially, our plan was to use **Google Analytics 4 (GA4)** raw data through BigQuery integration. However, we later discovered that BigQuery **only begins collecting data after the integration is enabled**. Since our web application had already been shared with users and data was actively being generated, we were unable to access historical event-level data through BigQuery.

To address this limitation, we turned to the **Google Analytics Data API (v1beta)**, which allows for programmatic access to aggregated GA4 metrics and dimensions.

## API-Based Extraction Strategy

We used Python and the official `google-analytics-data` library to send a query to the GA4 API. The script is based on the `BetaAnalyticsDataClient` and collects a structured report of user interactions across a specific date range.

### Key components of the extraction:

- **PROPERTY_ID**: The GA4 property ID of our app
- **KEY_PATH**: The path to our private service account credentials (for authentication)
- **START_DATE / END_DATE**: The full time span of the A/B testing period
- **DIMENSIONS**:
  - `eventName`: the type of interaction (e.g., Click, Page Leave, Tab Viewed)
  - `date`: the date of the event
  - `city`, `country`, `deviceCategory`, `browser`: user-level metadata
  - `sessionSourceMedium`: how the user found the site
  - `pagePath`: which page the event occurred on
- **METRICS**:
  - `eventCount`: how many times that event occurred
  - `userEngagementDuration`: the total time users were engaged (per dimension group)
  - `engagedSessions`: the number of sessions with engagement
  - `screenPageViews`: page views during the session

The API aggregates data across all provided **dimensions**. For example, if multiple users triggered the same event on the same day, city, and browser, the result would be **a single row** with the summed metrics for that group.

### Script Output

The results were written to two csv files for our two sites which contains detailed aggregate analytics grouped by the above dimensions.

## Realization About Engagement Timing

At one point, we considered analyzing tab-specific engagement durations by parsing custom labels such as `"User Guide - 52s"` from GA event parameters. However, we realized that this was unnecessary because:

- GA4 already tracks **userEngagementDuration** as part of each event group
- The use of dimensions such as `eventName` and `eventLabels` provides sufficient context for interpreting the engagement data
- Relying on `userEngagementDuration` ensures accuracy and consistency across all event types

As a result, we stopped parsing time manually from event labels and focused solely on the `userEngagementDuration` metric that was already provided in the API response.
