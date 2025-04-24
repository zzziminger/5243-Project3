
# Statistical Analysis & Results (Methodological Summary)

To evaluate the effectiveness of introducing a tutorial into our web application, we conducted a rigorous analysis grounded in both exploratory data analysis (EDA) and statistical hypothesis testing. The objective was to determine whether the tutorial influenced key user behaviors, such as task completion, user engagement, and bounce rates.

## Exploratory Data Analysis (EDA)

We began by preprocessing both datasets—one from the version **with the tutorial** and one **without**—by normalizing column values. This included:

- Cleaning whitespace from `eventName` and `eventLabels`
- Handling missing labels by filling with `"Unlabeled"`
- Truncating `eventLabels` at the first dash (`-`) to group similar interactions (e.g., `"User Guide - 52s"` was mapped to `"User Guide"`)

This allowed for more interpretable and meaningful aggregation of events, especially for analyzing engagement duration by content section (e.g., tab views). (See our section on acquiring data where we talk about why we had to remove the extra information at the end of the `Tab Duration` labels.)

We then aggregated the data by `(eventName, eventLabels)` to observe the most frequent interactions and their distribution across both versions of the app. This revealed key interaction patterns, such as:

- Frequency of clicks on buttons like `"Apply Numeric"` or `"Clean Data"`
- Engagement with various tabs or content panels through `"Tab Duration"` and `"Tab Viewed"` events
- Bounce behavior captured through the `"Page Leave"` event

This EDA phase helped to identify metrics of interest for statistical testing.

## Statistical Analysis

Based on the exploratory findings and the experiment design, we selected the following **key performance metrics**:

1. **Task Completion** – Measured by counts of clicks on `"Apply Numeric"` and `"Clean Data"` buttons  
2. **Page Leaves** – Measured by `"Page Leave"` events with no associated label (interpreted as bounce behavior)  
3. **Tab Engagement** – Measured by the total `userEngagementDuration` for `"Tab Duration"` events, grouped by tab name  
4. **Tutorial Usage** – Measured by clicks on `"Start Tutorial"` and `"Skip Tutorial"` within the treatment group  

We applied the following statistical methods to evaluate these metrics:

### 1. Chi-Squared Test of Independence

Used to assess whether there were statistically significant differences in categorical event outcomes (e.g., whether the user completed a task or left the page) between the control and treatment groups. For each test:

- A 2x2 contingency table was constructed:

  ```
  ┌────────────────────┬────────────────────────────┐
  │                    │ Event Occurred / Not Occurred │
  ├────────────────────┼────────────────────────────┤
  │ No Tutorial        │ count                       │
  │ With Tutorial      │ count                       │
  └────────────────────┴────────────────────────────┘
  ```

- We compared raw event counts (e.g., task completions) relative to total events per group.
- The **Chi-squared statistic** and **p-value** were computed to determine significance.

### 2. Welch’s t-Test

Used to compare **average engagement durations** between the control and treatment groups for tab viewing behavior. This test was selected due to:

- Unequal sample sizes and potentially unequal variances
- Continuous nature of the metric (`userEngagementDuration`)

Engagement durations from `"Tab Duration"` events were extracted and compared using a two-tailed Welch’s t-test. This allowed us to test the null hypothesis that the mean engagement durations for the two groups were equal.

### 3. Tutorial Uptake Rate

Although not a formal hypothesis test, we also calculated the **uptake rate of the tutorial**:

- The denominator was the total number of users who triggered a `first_visit` event (used as a proxy for unique users).
- The numerator was the number of users who clicked `"Start Tutorial"`.
- This was expressed as a proportion to describe how widely the tutorial was adopted.

---

This comprehensive approach ensured that both surface-level behavior (via EDA) and deeper causal relationships (via statistical inference) were accounted for in evaluating the impact of the tutorial.
