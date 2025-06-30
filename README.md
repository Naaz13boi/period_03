# Task_03_Descriptive_Stats

This repository provides a comprehensive data analysis project focused on calculating descriptive statistics using various Python libraries and methodologies.

## Project Structure

The repository is organized as follows:

*   `withpanda.py`: A Python script demonstrating analysis with the Pandas library.
*   `requirements.txt`: Lists all project dependencies.
*   `README.md`: This file, containing project details.

## Setup and Installation

To get started with this project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Naaz13boi/period_03.git
    cd Task_03_Descriptive_Stats
    ```

2.  **Create and activate a virtual environment** (recommended for managing dependencies):
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Each analysis script can be executed independently from the command line:

```bash
python <script_name.py>
```

For example, to run the Pandas analysis script:
```bash
python withpanda.py
```

## Data Analysis Approach

This project explores descriptive statistics from three distinct perspectives:

*   **Pure Python:** Employs only the Python standard library for fundamental statistical computations.
*   **Pandas:** Leverages the powerful capabilities of the Pandas library for data manipulation and analysis.
*   **Polars:** Utilizes the Polars library for high-performance data analysis, particularly effective with larger datasets.

### Statistics Computed

For each dataset and approach, the following descriptive statistics are calculated:

*   **Count:** The total number of observations.
*   **Mean:** The average value for numerical fields.
*   **Minimum and Maximum:** The smallest and largest values observed.
*   **Standard Deviation:** A measure of the dispersion of data points from the mean.
*   **Unique Value Counts:** For categorical or non-numeric fields, the number of distinct values.
*   **Most Frequent Values:** For non-numeric fields, the values that appear most often.

### Levels of Analysis

The analysis is conducted at three granularities:

1.  **Overall Dataset:** Statistics for the entire dataset.
2.  **Aggregated by page\_id:** Statistics grouped by the unique identifier for each page.
3.  **Aggregated by (page\_id, ad\_id):** Statistics further broken down by page and advertisement identifiers.

## Key Findings

### Facebook Ads Dataset

**Audience Reach and Financials:**
*   The average estimated audience size reached by ads was approximately 556,463 individuals.
*   On average, ads received around 45,602 impressions.
*   The average reported spend per ad was $1,061.
*   The highest recorded spend for a single ad reached $474,999.

**Message Classification:**
*   Approximately 57% of ads incorporated a call to action (CTA).
*   A majority of ads, 55%, utilized advocacy messaging.
*   Issue-based messaging was present in 38% of ads.
*   Attack messaging was found in 27% of the ads.
*   Image-based advertisements constituted 22% of the total.

**Campaign Topic Focus:**
*   The economy was the most frequently discussed topic, appearing in 12% of ads.
*   Health-related content was featured in 11% of ads.
*   Social and cultural issues comprised another 11% of the ad content.
*   Women's issues were addressed in 8% of the ads.

**Content Integrity:**
*   A small percentage, 7%, of ads were identified as potentially containing scam content.
*   Around 5% of ads raised concerns related to election integrity.
*   The incidence of uncivil language within ad messaging was generally low.

### Facebook Posts Dataset

**Engagement Metrics:**
*   Engagement levels varied significantly across different posts.
*   A strong positive correlation was observed between the number of comments and shares.
*   Emotional reactions, such as "Love" and "Angry," offered valuable insights into how content was received by the audience.

### Twitter Posts Dataset

**Content Analysis:**
*   A wide array of topics were discussed in the tweets.
*   Political discourse was a prominent theme.
*   Engagement metrics exhibited considerable diversity.

## Cross-Platform Insights

**Messaging Consistency:**
*   The distribution of topics across Facebook and Twitter was found to be broadly similar.
*   Each platform demonstrated distinct patterns in user engagement.
*   Audience targeting strategies appeared to differ across the platforms.

**Performance Metrics:**
*   Facebook advertisements generally achieved higher reach but incurred substantial costs.
*   Organic posts on Facebook showed varied engagement outcomes.
*   Twitter content demonstrated a notable potential for rapid and widespread dissemination (virality) for specific types of posts.

