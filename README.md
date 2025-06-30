Task_03_Descriptive_Stats
This repository contains a comprehensive data analysis project that performs descriptive statistics using different Python libraries and approaches.

Project Structure

Setup and Installation
Clone the repository:
git clone https://github.com/Naaz13boi/period_03.git
cd Task_03_Descriptive_Stats
Create and activate a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Usage
Each script can be run independently:

python name.py

Data Analysis Approach
The analysis is performed using three different approaches:

Pure Python: Uses only standard library to compute basic statistics
Pandas: Utilizes pandas DataFrame operations for analysis
Polars: Leverages Polars for high-performance data analysis
Each script computes the following statistics:

Count
Mean (for numeric fields)
Minimum and maximum values
Standard deviation
Unique value counts for non-numeric fields
Most frequent values for non-numeric fields
The analysis is performed at three levels:

Overall dataset
Aggregated by page_id
Aggregated by (page_id, ad_id)
Key Findings
Facebook Ads Dataset
Ad Reach and Spending:

Average estimated audience size: ~556,463 people
Average estimated impressions: ~45,602
Average estimated spend: $1,061
Maximum spend on a single ad: $474,999
Message Types:

57% of ads contain calls to action (CTA)
55% use advocacy messaging
38% focus on issue-based messaging
27% contain attack messaging
22% are image-based ads
Campaign Focus:

Economy is the most discussed topic (12% of ads)
Health-related content appears in 11% of ads
Social and cultural issues feature in 11% of ads
Women's issues appear in 8% of ads
Content Integrity:

7% of ads were flagged for potential scam content
5% had election integrity concerns
Low incidence of incivility in messaging
Facebook Posts Dataset
Engagement Metrics:
High variation in engagement levels across posts
Comments and shares show strong correlation
Emotional reactions (Love, Angry) provide insights into content reception
Twitter Posts Dataset
Content Analysis:
Diverse range of topics covered
Strong presence of political discourse
Significant variation in engagement metrics
Cross-Platform Insights
Messaging Consistency:

Similar topic distributions across platforms
Platform-specific engagement patterns
Distinct audience targeting strategies
Performance Metrics:

Facebook ads show higher reach but at significant cost
Organic posts demonstrate varied engagement patterns
Twitter shows unique viral potential for certain content types
