-- Project 3: Subscription Churn & Cohort Retention Analyzer
-- Database Schema & Analytical Query Script

DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS user_activity;

-- Table for user subscription signup details
CREATE TABLE subscriptions (
    user_id INT PRIMARY KEY,
    signup_date DATE,
    plan_type VARCHAR(50)
);

-- Table for monthly active usage / renewals
CREATE TABLE user_activity (
    activity_id INT PRIMARY KEY,
    user_id INT,
    activity_month DATE,
    engagement_score INT
);

-- Populate Subscriptions
INSERT INTO subscriptions (user_id, signup_date, plan_type) VALUES
(101, '2026-01-15', 'Pro'),
(102, '2026-01-20', 'Basic'),
(103, '2026-02-10', 'Pro'),
(104, '2026-02-18', 'Enterprise'),
(105, '2026-03-05', 'Basic');

-- Populate User Activity
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

-- Core Cohort Extraction Query
SELECT 
    s.user_id,
    s.plan_type,
    STRFTIME('%Y-%m', s.signup_date) AS cohort_month,
    STRFTIME('%Y-%m', u.activity_month) AS activity_month,
    u.engagement_score
FROM subscriptions s
JOIN user_activity u ON s.user_id = u.user_id
ORDER BY s.user_id, u.activity_month;
