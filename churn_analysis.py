# Project 3: Subscription Churn & Cohort Retention Analyzer
# Author: Data Analyst Portfolio

import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_cohort_analysis():
    # 1. Connect and create SQLite database
    conn = sqlite3.connect('subscription_churn_analytics.db')
    cursor = conn.cursor()

    # 2. Ingest Schema and Sample Data
    cursor.executescript("""
    DROP TABLE IF EXISTS subscriptions;
    DROP TABLE IF EXISTS user_activity;

    CREATE TABLE subscriptions (
        user_id INT PRIMARY KEY,
        signup_date DATE,
        plan_type VARCHAR(50)
    );

    CREATE TABLE user_activity (
        activity_id INT PRIMARY KEY,
        user_id INT,
        activity_month DATE,
        engagement_score INT
    );

    INSERT INTO subscriptions (user_id, signup_date, plan_type) VALUES
    (101, '2026-01-15', 'Pro'),
    (102, '2026-01-20', 'Basic'),
    (103, '2026-02-10', 'Pro'),
    (104, '2026-02-18', 'Enterprise'),
    (105, '2026-03-05', 'Basic');

    INSERT INTO user_activity (activity_id, user_id, activity_month, engagement_score) VALUES
    (1, 101, '2026-01-01', 85),
    (2, 101, '2026-02-01', 90),
    (3, 101, '2026-03-01', 78),
    (4, 102, '2026-01-01', 40),
    (5, 102, '2026-02-01', 20),
    (6, 103, '2026-02-01', 95),
    (7, 103, '2026-03-01', 92),
    (8, 104, '2026-02-01', 88),
    (9, 104, '2026-03-01', 85),
    (10, 105, '2026-03-01', 60);
    """)
    conn.commit()

    # 3. Query Cohort Data
    query = """
    SELECT 
        s.user_id,
        STRFTIME('%Y-%m', s.signup_date) AS cohort_month,
        STRFTIME('%Y-%m', u.activity_month) AS activity_month
    FROM subscriptions s
    JOIN user_activity u ON s.user_id = u.user_id;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    # 4. Calculate Cohort Index
    df['cohort_month_dt'] = pd.to_datetime(df['cohort_month'])
    df['activity_month_dt'] = pd.to_datetime(df['activity_month'])

    df['cohort_index'] = (
        (df['activity_month_dt'].dt.year - df['cohort_month_dt'].dt.year) * 12 +
        (df['activity_month_dt'].dt.month - df['cohort_month_dt'].dt.month)
    )

    # 5. Build Retention Matrix
    cohort_pivot = df.pivot_table(index='cohort_month', columns='cohort_index', values='user_id', aggfunc='nunique')
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0) * 100

    # 6. Plot Heatmap
    plt.figure(figsize=(8, 5))
    sns.heatmap(retention_matrix, annot=True, fmt='.1f', cmap='Blues', cbar=True)
    plt.title('Customer Subscription Cohort Retention Heatmap (%)')
    plt.xlabel('Months Since Signup (Cohort Index)')
    plt.ylabel('Cohort Month')
    plt.show()

if __name__ == '__main__':
    run_cohort_analysis()
