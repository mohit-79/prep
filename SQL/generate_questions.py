import json
import os

# Complete list of LeetCode SQL 50 problems + 12 Curated OA problems
# with questions, topics, difficulty, solution SQL, and initial key notes.

DATA = [
    # ==================== LEETCODE SQL 50 ====================
    # --- SELECT ---
    {
        "id": 1757,
        "title": "1757. Recyclable and Low Fat Products",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Select",
        "status": "Todo",
        "question": "Table: Products\n+-------------+---------+\n| Column Name | Type    |\n+-------------+---------+\n| product_id  | int     |\n| low_fats    | enum    |\n| recyclable  | enum    |\n+-------------+---------+\nFind the ids of products that are both low fat and recyclable.",
        "solution": "SELECT product_id\nFROM Products\nWHERE low_fats = 'Y' AND recyclable = 'Y';",
        "notes": "Simple WHERE clause filter with logical AND."
    },
    {
        "id": 584,
        "title": "584. Find Customer Referee",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Select / NULL Handling",
        "status": "Todo",
        "question": "Table: Customer\n+-------------+---------+\n| Column Name | Type    |\n+-------------+---------+\n| id          | int     |\n| name        | varchar |\n| referee_id  | int     |\n+-------------+---------+\nFind the names of the customer that are not referred by the customer with id = 2.",
        "solution": "SELECT name\nFROM Customer\nWHERE referee_id != 2 OR referee_id IS NULL;\n-- Or: WHERE IFNULL(referee_id, 0) != 2;",
        "notes": "Trap: SQL three-valued logic. 'referee_id != 2' excludes NULL values! Must check IS NULL or IFNULL."
    },
    {
        "id": 595,
        "title": "595. Big Countries",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Select",
        "status": "Todo",
        "question": "Table: World\nA country is big if: area >= 3,000,000 km2 or population >= 25,000,000.\nFind the name, population, and area of the big countries.",
        "solution": "SELECT name, population, area\nFROM World\nWHERE area >= 3000000 OR population >= 25000000;",
        "notes": "Can use OR, or UNION for index optimization in older MySQL engines."
    },
    {
        "id": 1148,
        "title": "1148. Article Views I",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Select / DISTINCT",
        "status": "Todo",
        "question": "Table: Views (article_id, author_id, viewer_id, view_date)\nFind all the authors that viewed at least one of their own articles, sorted by id ASC.",
        "solution": "SELECT DISTINCT author_id AS id\nFROM Views\nWHERE author_id = viewer_id\nORDER BY id ASC;",
        "notes": "Use DISTINCT to remove duplicate author views and remember ORDER BY id."
    },
    {
        "id": 1683,
        "title": "1683. Invalid Tweets",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "String Functions",
        "status": "Todo",
        "question": "Table: Tweets (tweet_id, content)\nFind the IDs of invalid tweets where length of content is strictly greater than 15.",
        "solution": "SELECT tweet_id\nFROM Tweets\nWHERE LENGTH(content) > 15; -- Or CHAR_LENGTH(content) > 15",
        "notes": "CHAR_LENGTH() measures character count, while LENGTH() counts bytes (matters for multibyte UTF-8 characters)."
    },

    # --- BASIC JOINS ---
    {
        "id": 1378,
        "title": "1378. Replace Employee ID With The Unique Identifier",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Joins (LEFT JOIN)",
        "status": "Todo",
        "question": "Employees (id, name), EmployeeUNI (id, unique_id)\nShow unique_id and name. If employee does not have unique_id, show null.",
        "solution": "SELECT eu.unique_id, e.name\nFROM Employees e\nLEFT JOIN EmployeeUNI eu ON e.id = eu.id;",
        "notes": "LEFT JOIN preserves all employees from the left table even without a matching unique_id."
    },
    {
        "id": 1068,
        "title": "1068. Product Sales Analysis I",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Joins",
        "status": "Todo",
        "question": "Sales (sale_id, product_id, year, quantity, price), Product (product_id, product_name)\nReport product_name, year, and price for each sale_id.",
        "solution": "SELECT p.product_name, s.year, s.price\nFROM Sales s\nJOIN Product p ON s.product_id = p.product_id;",
        "notes": "Straightforward INNER JOIN on product_id."
    },
    {
        "id": 1581,
        "title": "1581. Customer Who Visited but Did Not Make Any Transactions",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Joins / Anti-Join",
        "status": "Todo",
        "question": "Visits (visit_id, customer_id), Transactions (transaction_id, visit_id, amount)\nFind IDs of users who visited without making transactions and number of times they did.",
        "solution": "SELECT v.customer_id, COUNT(v.visit_id) AS count_no_trans\nFROM Visits v\nLEFT JOIN Transactions t ON v.visit_id = t.visit_id\nWHERE t.transaction_id IS NULL\nGROUP BY v.customer_id;",
        "notes": "Classic Anti-Join pattern: LEFT JOIN + WHERE right_table.key IS NULL."
    },
    {
        "id": 197,
        "title": "197. Rising Temperature",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Self Join / Date Functions",
        "status": "Todo",
        "question": "Weather (id, recordDate, temperature)\nFind all dates' Id with higher temperatures compared to its previous dates (yesterday).",
        "solution": "SELECT w1.id\nFROM Weather w1\nJOIN Weather w2 ON DATEDIFF(w1.recordDate, w2.recordDate) = 1\nWHERE w1.temperature > w2.temperature;",
        "notes": "Do NOT use 'w1.id = w2.id + 1' because IDs might not be sequential! Use DATEDIFF(w1.date, w2.date) = 1 or SUBDATE."
    },
    {
        "id": 1661,
        "title": "1661. Average Time of Process per Machine",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Self Join / Aggregation",
        "status": "Todo",
        "question": "Activity (machine_id, process_id, activity_type, timestamp)\nFind the average time each machine takes to complete a process, rounded to 3 decimal places.",
        "solution": "SELECT \n    a1.machine_id,\n    ROUND(AVG(a2.timestamp - a1.timestamp), 3) AS processing_time\nFROM Activity a1\nJOIN Activity a2 \n  ON a1.machine_id = a2.machine_id \n AND a1.process_id = a2.process_id\n AND a1.activity_type = 'start' \n AND a2.activity_type = 'end'\nGROUP BY a1.machine_id;",
        "notes": "Pair 'start' and 'end' activities by self-joining on machine_id + process_id."
    },
    {
        "id": 577,
        "title": "577. Employee Bonus",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "LEFT JOIN / NULL Handling",
        "status": "Todo",
        "question": "Employee (empId, name, supervisor, salary), Bonus (empId, bonus)\nReport the name and bonus amount of each employee with a bonus less than 1000 or no bonus.",
        "solution": "SELECT e.name, b.bonus\nFROM Employee e\nLEFT JOIN Bonus b ON e.empId = b.empId\nWHERE b.bonus < 1000 OR b.bonus IS NULL;",
        "notes": "Make sure to include 'OR b.bonus IS NULL' for employees with no entry in Bonus."
    },
    {
        "id": 1280,
        "title": "1280. Students and Examinations",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "CROSS JOIN + LEFT JOIN",
        "status": "Todo",
        "question": "Students, Subjects, Examinations\nFind the number of times each student attended each exam, ordered by student_id, subject_name.",
        "solution": "SELECT \n    s.student_id, \n    s.student_name, \n    sub.subject_name,\n    COUNT(e.subject_name) AS attended_exams\nFROM Students s\nCROSS JOIN Subjects sub\nLEFT JOIN Examinations e \n  ON s.student_id = e.student_id \n AND sub.subject_name = e.subject_name\nGROUP BY s.student_id, s.student_name, sub.subject_name\nORDER BY s.student_id, sub.subject_name;",
        "notes": "Must produce Cartesian product of Students x Subjects via CROSS JOIN first so 0-count exams appear."
    },
    {
        "id": 570,
        "title": "570. Managers with at Least 5 Direct Reports",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Self Join / Subquery",
        "status": "Todo",
        "question": "Employee (id, name, department, managerId)\nFind managers who have at least five direct reports.",
        "solution": "SELECT m.name\nFROM Employee e\nJOIN Employee m ON e.managerId = m.id\nGROUP BY m.id, m.name\nHAVING COUNT(e.id) >= 5;",
        "notes": "Group by manager's ID (not just name) to handle duplicate names."
    },
    {
        "id": 1934,
        "title": "1934. Confirmation Rate",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "LEFT JOIN + Conditional AVG",
        "status": "Todo",
        "question": "Signups (user_id), Confirmations (user_id, time_stamp, action)\nConfirmation rate = confirmed messages / total requests. Round to 2 decimal places.",
        "solution": "SELECT \n    s.user_id,\n    ROUND(IFNULL(AVG(c.action = 'confirmed'), 0), 2) AS confirmation_rate\nFROM Signups s\nLEFT JOIN Confirmations c ON s.user_id = c.user_id\nGROUP BY s.user_id;",
        "notes": "Trick: AVG(c.action = 'confirmed') calculates true fraction directly! IFNULL handles 0 requests."
    },

    # --- BASIC AGGREGATE FUNCTIONS ---
    {
        "id": 620,
        "title": "620. Not Boring Movies",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Basic Filtering / MOD",
        "status": "Todo",
        "question": "Cinema (id, movie, description, rating)\nReport movies with odd-numbered ID and description not 'boring'. Sort by rating DESC.",
        "solution": "SELECT id, movie, description, rating\nFROM Cinema\nWHERE id % 2 = 1 AND description != 'boring'\nORDER BY rating DESC;",
        "notes": "MOD(id, 2) = 1 or id % 2 = 1 for odd IDs."
    },
    {
        "id": 1251,
        "title": "1251. Average Selling Price",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Aggregate / Range Join",
        "status": "Todo",
        "question": "Prices (product_id, start_date, end_date, price), UnitsSold (product_id, purchase_date, units)\nFind average selling price for each product. Round to 2 decimal places.",
        "solution": "SELECT \n    p.product_id,\n    IFNULL(ROUND(SUM(p.price * u.units) / SUM(u.units), 2), 0) AS average_price\nFROM Prices p\nLEFT JOIN UnitsSold u \n  ON p.product_id = u.product_id \n AND u.purchase_date BETWEEN p.start_date AND p.end_date\nGROUP BY p.product_id;",
        "notes": "Join condition with BETWEEN. Watch for products with 0 units sold (needs IFNULL)."
    },
    {
        "id": 1075,
        "title": "1075. Project Employees I",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Aggregate Functions",
        "status": "Todo",
        "question": "Project (project_id, employee_id), Employee (employee_id, name, experience_years)\nReport average experience years of all employees for each project, rounded to 2 digits.",
        "solution": "SELECT \n    p.project_id,\n    ROUND(AVG(e.experience_years), 2) AS average_years\nFROM Project p\nJOIN Employee e ON p.employee_id = e.employee_id\nGROUP BY p.project_id;",
        "notes": "Standard JOIN and AVG() with ROUND."
    },
    {
        "id": 1633,
        "title": "1633. Percentage of Users Attended a Contest",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Aggregate Functions",
        "status": "Todo",
        "question": "Users (user_id), Register (contest_id, user_id)\nFind percentage of users registered in each contest, rounded to 2 decimals. Sort by percentage DESC, contest_id ASC.",
        "solution": "SELECT \n    contest_id,\n    ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(*) FROM Users), 2) AS percentage\nFROM Register\nGROUP BY contest_id\nORDER BY percentage DESC, contest_id ASC;",
        "notes": "Use a scalar subquery `(SELECT COUNT(*) FROM Users)` in the SELECT clause."
    },
    {
        "id": 1211,
        "title": "1211. Queries Quality and Percentage",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Aggregate / Conditional Logic",
        "status": "Todo",
        "question": "Queries (query_name, result, position, rating)\nQuality = AVG(rating / position). Poor query % = % of ratings < 3. Round both to 2 decimals.",
        "solution": "SELECT \n    query_name,\n    ROUND(AVG(rating / position), 2) AS quality,\n    ROUND(AVG(rating < 3) * 100, 2) AS poor_query_percentage\nFROM Queries\nWHERE query_name IS NOT NULL\nGROUP BY query_name;",
        "notes": "Exclude NULL query_names if any. AVG(rating < 3) evaluates boolean condition to 1 or 0."
    },
    {
        "id": 1193,
        "title": "1193. Monthly Transactions I",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Date Formatting / Grouping",
        "status": "Todo",
        "question": "Transactions (id, country, state, amount, trans_date)\nFind month, country, total count, approved count, total amount, approved amount.",
        "solution": "SELECT \n    DATE_FORMAT(trans_date, '%Y-%m') AS month,\n    country,\n    COUNT(id) AS trans_count,\n    SUM(state = 'approved') AS approved_count,\n    SUM(amount) AS trans_total_amount,\n    SUM(IF(state = 'approved', amount, 0)) AS approved_total_amount\nFROM Transactions\nGROUP BY month, country;",
        "notes": "DATE_FORMAT(trans_date, '%Y-%m') extracts year-month string for group by."
    },
    {
        "id": 1174,
        "title": "1174. Immediate Food Delivery II",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Subquery / First Order Analysis",
        "status": "Todo",
        "question": "Delivery (delivery_id, customer_id, order_date, customer_pref_delivery_date)\nIf order_date == customer_pref_delivery_date -> immediate. Find % of immediate orders in first orders of all customers.",
        "solution": "SELECT \n    ROUND(AVG(order_date = customer_pref_delivery_date) * 100, 2) AS immediate_percentage\nFROM Delivery\nWHERE (customer_id, order_date) IN (\n    SELECT customer_id, MIN(order_date)\n    FROM Delivery\n    GROUP BY customer_id\n);",
        "notes": "Tuple matching (customer_id, order_date) IN (SELECT customer_id, MIN(order_date)...) picks first orders only."
    },
    {
        "id": 550,
        "title": "550. Game Play Analysis IV",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Self Join / Window / Consecutive Date",
        "status": "Todo",
        "question": "Activity (player_id, device_id, event_date, games_played)\nFraction of players that logged in again on the day after their first login date.",
        "solution": "SELECT \n    ROUND(COUNT(a2.player_id) / COUNT(a1.player_id), 2) AS fraction\nFROM (\n    SELECT player_id, MIN(event_date) AS first_login\n    FROM Activity\n    GROUP BY player_id\n) a1\nLEFT JOIN Activity a2 \n  ON a1.player_id = a2.player_id \n AND a2.event_date = DATE_ADD(a1.first_login, INTERVAL 1 DAY);",
        "notes": "Denominator is total distinct players. Numerator is players logging in exactly 1 day after first_login."
    },

    # --- SORTING AND GROUPING ---
    {
        "id": 2356,
        "title": "2356. Number of Unique Subjects Taught by Each Teacher",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "GROUP BY / COUNT(DISTINCT)",
        "status": "Todo",
        "question": "Teacher (teacher_id, subject_id, dept_id)\nCalculate the number of unique subjects each teacher teaches in the university.",
        "solution": "SELECT teacher_id, COUNT(DISTINCT subject_id) AS cnt\nFROM Teacher\nGROUP BY teacher_id;",
        "notes": "Simple COUNT(DISTINCT subject_id) grouped by teacher."
    },
    {
        "id": 1141,
        "title": "1141. User Activity for the Past 30 Days I",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Date Filtering / Aggregation",
        "status": "Todo",
        "question": "Activity (user_id, session_id, activity_date, activity_type)\nFind daily active user count for a period of 30 days ending 2019-07-27 inclusively.",
        "solution": "SELECT \n    activity_date AS day,\n    COUNT(DISTINCT user_id) AS active_users\nFROM Activity\nWHERE activity_date BETWEEN DATE_SUB('2019-07-27', INTERVAL 29 DAY) AND '2019-07-27'\nGROUP BY activity_date;",
        "notes": "30 days ending 2019-07-27 means start date is 2019-07-27 - 29 days (2019-06-28)."
    },
    {
        "id": 1070,
        "title": "1070. Product Sales Analysis III",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Subquery / Ranking",
        "status": "Todo",
        "question": "Sales (sale_id, product_id, year, quantity, price)\nSelect product_id, first_year, quantity, and price for the first year of every product sold.",
        "solution": "SELECT product_id, year AS first_year, quantity, price\nFROM Sales\nWHERE (product_id, year) IN (\n    SELECT product_id, MIN(year)\n    FROM Sales\n    GROUP BY product_id\n);",
        "notes": "Pair (product_id, year) with subquery of MIN(year). Can also use RANK() OVER (PARTITION BY product_id ORDER BY year)."
    },
    {
        "id": 596,
        "title": "596. Classes More Than 5 Students",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "HAVING Clause",
        "status": "Todo",
        "question": "Courses (student, class)\nReport all classes that have at least five students.",
        "solution": "SELECT class\nFROM Courses\nGROUP BY class\nHAVING COUNT(student) >= 5;",
        "notes": "Group by class and filter aggregate count using HAVING."
    },
    {
        "id": 1729,
        "title": "1729. Find Followers Count",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Aggregation / ORDER BY",
        "status": "Todo",
        "question": "Followers (user_id, follower_id)\nReturn the number of followers for each user, ordered by user_id ASC.",
        "solution": "SELECT user_id, COUNT(follower_id) AS followers_count\nFROM Followers\nGROUP BY user_id\nORDER BY user_id ASC;",
        "notes": "Standard aggregation with ORDER BY."
    },
    {
        "id": 619,
        "title": "619. Biggest Single Number",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Subquery / Aggregation",
        "status": "Todo",
        "question": "MyNumbers (num)\nA single number is that which appeared only once. Find the largest single number. If none, return null.",
        "solution": "SELECT MAX(num) AS num\nFROM (\n    SELECT num\n    FROM MyNumbers\n    GROUP BY num\n    HAVING COUNT(num) = 1\n) t;",
        "notes": "MAX() over the inner subquery returns NULL if the inner query produces 0 rows."
    },
    {
        "id": 1045,
        "title": "1045. Customers Who Bought All Products",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "HAVING COUNT(DISTINCT) = Total",
        "status": "Todo",
        "question": "Customer (customer_id, product_key), Product (product_key)\nReport customer ids who bought all the products in the Product table.",
        "solution": "SELECT customer_id\nFROM Customer\nGROUP BY customer_id\nHAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);",
        "notes": "Relational division: match COUNT(DISTINCT product_key) with total count in Product table."
    },

    # --- ADVANCED SELECT AND JOINS ---
    {
        "id": 1731,
        "title": "1731. The Number of Employees Which Report to Each Employee",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Self Join / Aggregation",
        "status": "Todo",
        "question": "Employees (employee_id, name, reports_to, age)\nReport employee_id, name, reports_count, and average_age rounded to nearest whole number, ordered by employee_id.",
        "solution": "SELECT \n    m.employee_id,\n    m.name,\n    COUNT(e.employee_id) AS reports_count,\n    ROUND(AVG(e.age)) AS average_age\nFROM Employees m\nJOIN Employees e ON m.employee_id = e.reports_to\nGROUP BY m.employee_id, m.name\nORDER BY m.employee_id;",
        "notes": "Self-join manager m on m.employee_id = e.reports_to. ROUND() with zero decimals rounds to whole integer."
    },
    {
        "id": 1789,
        "title": "1789. Primary Department for Each Employee",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "UNION / Filtering",
        "status": "Todo",
        "question": "Employee (employee_id, department_id, primary_flag)\nFind employee_id with their primary department flag 'Y', or if they belong to only 1 department, that department.",
        "solution": "SELECT employee_id, department_id\nFROM Employee\nWHERE primary_flag = 'Y'\nUNION\nSELECT employee_id, department_id\nFROM Employee\nGROUP BY employee_id\nHAVING COUNT(department_id) = 1;",
        "notes": "UNION eliminates duplicates automatically and combines both scenarios."
    },
    {
        "id": 610,
        "title": "610. Triangle Judgement",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "CASE WHEN / Conditional",
        "status": "Todo",
        "question": "Triangle (x, y, z)\nReport for every three line segments whether they can form a triangle ('Yes' or 'No').",
        "solution": "SELECT x, y, z,\n    CASE \n        WHEN x + y > z AND x + z > y AND y + z > x THEN 'Yes'\n        ELSE 'No'\n    END AS triangle\nFROM Triangle;",
        "notes": "Triangle inequality theorem: sum of any 2 sides must be strictly greater than the 3rd side."
    },
    {
        "id": 180,
        "title": "180. Consecutive Numbers",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Window Functions / LEAD",
        "status": "Todo",
        "question": "Logs (id, num)\nFind all numbers that appear at least three times consecutively.",
        "solution": "WITH RankedLogs AS (\n    SELECT \n        num,\n        LEAD(num, 1) OVER (ORDER BY id) AS next_1,\n        LEAD(num, 2) OVER (ORDER BY id) AS next_2\n    FROM Logs\n)\nSELECT DISTINCT num AS ConsecutiveNums\nFROM RankedLogs\nWHERE num = next_1 AND num = next_2;",
        "notes": "LEAD(num, 1) and LEAD(num, 2) over ORDER BY id. Use DISTINCT for duplicates."
    },
    {
        "id": 1164,
        "title": "1164. Product Price at a Given Date",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Window / UNION / Subquery",
        "status": "Todo",
        "question": "Products (product_id, new_price, change_date)\nFind the prices of all products on 2019-08-16. Initial price is 10.",
        "solution": "SELECT product_id, new_price AS price\nFROM Products\nWHERE (product_id, change_date) IN (\n    SELECT product_id, MAX(change_date)\n    FROM Products\n    WHERE change_date <= '2019-08-16'\n    GROUP BY product_id\n)\nUNION\nSELECT product_id, 10 AS price\nFROM Products\nGROUP BY product_id\nHAVING MIN(change_date) > '2019-08-16';",
        "notes": "Split into products with changes on/before 2019-08-16 and products whose first change was after (default 10)."
    },
    {
        "id": 1204,
        "title": "1204. Last Person to Fit in the Bus",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Cumulative SUM / Window Function",
        "status": "Todo",
        "question": "Queue (person_id, person_name, weight, turn)\nBus weight limit is 1000 kg. Find the person_name of the last person that can fit without exceeding limit.",
        "solution": "WITH RunningWeight AS (\n    SELECT \n        person_name,\n        SUM(weight) OVER (ORDER BY turn) AS total_weight\n    FROM Queue\n)\nSELECT person_name\nFROM RunningWeight\nWHERE total_weight <= 1000\nORDER BY total_weight DESC\nLIMIT 1;",
        "notes": "Running total: SUM(weight) OVER (ORDER BY turn). Filter <= 1000 and pick highest turn/weight."
    },
    {
        "id": 1907,
        "title": "1907. Count Salary Categories",
        "platform": "LeetCode (SQL 50 & OA)",
        "difficulty": "Medium",
        "topic": "UNION / CASE WHEN Categorization",
        "status": "Todo",
        "question": "Accounts (account_id, income)\nCategorize into: 'Low Salary' (< 20000), 'Average Salary' (20000 to 50000), 'High Salary' (> 50000). Show all categories even if count is 0.",
        "solution": "SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count\nFROM Accounts\nWHERE income < 20000\nUNION\nSELECT 'Average Salary' AS category, COUNT(*)\nFROM Accounts\nWHERE income BETWEEN 20000 AND 50000\nUNION\nSELECT 'High Salary' AS category, COUNT(*)\nFROM Accounts\nWHERE income > 50000;",
        "notes": "Must use UNION of 3 explicit SELECTs so categories with 0 bank accounts still appear in the final table."
    },

    # --- SUBQUERIES ---
    {
        "id": 1978,
        "title": "1978. Employees Whose Manager Left the Company",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Subquery / NOT IN",
        "status": "Todo",
        "question": "Employees (employee_id, name, manager_id, salary)\nFind IDs of employees whose salary < 30000 and whose manager left the company (manager_id not in table). Sort by employee_id.",
        "solution": "SELECT employee_id\nFROM Employees\nWHERE salary < 30000\n  AND manager_id IS NOT NULL\n  AND manager_id NOT IN (SELECT employee_id FROM Employees)\nORDER BY employee_id;",
        "notes": "Must check 'manager_id IS NOT NULL' because 'NOT IN' with NULLs in subquery fails to evaluate."
    },
    {
        "id": 626,
        "title": "626. Exchange Seats",
        "platform": "LeetCode (SQL 50 & OA)",
        "difficulty": "Medium",
        "topic": "Conditional Logic & Row Shuffling",
        "status": "Todo",
        "question": "Seat (id, student)\nSwap consecutive student seats (1 with 2, 3 with 4). If total students is odd, last seat id stays unchanged.",
        "solution": "SELECT \n    CASE \n        WHEN id % 2 = 1 AND id = (SELECT COUNT(*) FROM Seat) THEN id\n        WHEN id % 2 = 1 THEN id + 1\n        ELSE id - 1\n    END AS id,\n    student\nFROM Seat\nORDER BY id ASC;",
        "notes": "Swap logic using CASE: if odd & last -> stay; if odd -> id + 1; if even -> id - 1. Then ORDER BY id."
    },
    {
        "id": 1341,
        "title": "1341. Movie Rating",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "UNION ALL / Multiple Subqueries",
        "status": "Todo",
        "question": "Find user who rated greatest number of movies (tie: lexicographically smaller name). Find movie with highest avg rating in Feb 2020 (tie: smaller title).",
        "solution": "(SELECT u.name AS results\n FROM MovieRating mr\n JOIN Users u ON mr.user_id = u.user_id\n GROUP BY mr.user_id\n ORDER BY COUNT(mr.movie_id) DESC, u.name ASC\n LIMIT 1)\nUNION ALL\n(SELECT m.title AS results\n FROM MovieRating mr\n JOIN Movies m ON mr.movie_id = m.movie_id\n WHERE mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'\n GROUP BY mr.movie_id\n ORDER BY AVG(mr.rating) DESC, m.title ASC\n LIMIT 1);",
        "notes": "Must use UNION ALL with parentheses around each sub-query so LIMIT applies to each individual part."
    },
    {
        "id": 1321,
        "title": "1321. Restaurant Growth",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Window Function / 7-Day Moving Sum",
        "status": "Todo",
        "question": "Customer (customer_id, name, visited_on, amount)\nCompute 7-day moving average of how much the customer paid in a window of 7 days (current day + 6 prior).",
        "solution": "WITH DailySum AS (\n    SELECT visited_on, SUM(amount) AS amount\n    FROM Customer\n    GROUP BY visited_on\n)\nSELECT \n    visited_on,\n    SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,\n    ROUND(AVG(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount\nFROM DailySum\nORDER BY visited_on\nOFFSET 6;",
        "notes": "Group by date first to consolidate daily amounts, then use ROWS BETWEEN 6 PRECEDING AND CURRENT ROW, skip first 6 rows via OFFSET 6."
    },
    {
        "id": 602,
        "title": "602. Friend Requests II: Who Has the Most Friends",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "UNION ALL / Grouping",
        "status": "Todo",
        "question": "RequestAccepted (requester_id, accepter_id, accept_date)\nFind the person who has the most friends and the most friends number.",
        "solution": "WITH AllFriends AS (\n    SELECT requester_id AS id FROM RequestAccepted\n    UNION ALL\n    SELECT accepter_id AS id FROM RequestAccepted\n)\nSELECT id, COUNT(*) AS num\nFROM AllFriends\nGROUP BY id\nORDER BY num DESC\nLIMIT 1;",
        "notes": "A friendship is bidirectional: combine requester_id and accepter_id using UNION ALL, then group by id."
    },
    {
        "id": 585,
        "title": "585. Investments in 2016",
        "platform": "LeetCode (SQL 50 & OA)",
        "difficulty": "Medium",
        "topic": "Multi-Condition Window Aggregates",
        "status": "Todo",
        "question": "Insurance (pid, tiv_2015, tiv_2016, lat, lon)\nSum tiv_2016 for policyholders who: 1) have same tiv_2015 as >= 1 other policyholder, 2) unique (lat, lon). Round to 2 decimals.",
        "solution": "SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016\nFROM (\n    SELECT \n        tiv_2016,\n        COUNT(*) OVER (PARTITION BY tiv_2015) AS count_2015,\n        COUNT(*) OVER (PARTITION BY lat, lon) AS count_loc\n    FROM Insurance\n) t\nWHERE count_2015 > 1 AND count_loc = 1;",
        "notes": "COUNT(*) OVER (PARTITION BY ...) avoids multiple subqueries and self-joins for duplicate/unique criteria."
    },
    {
        "id": 185,
        "title": "185. Department Top Three Salaries",
        "platform": "LeetCode (SQL 50 & OA)",
        "difficulty": "Hard",
        "topic": "DENSE_RANK() Top-N per Group",
        "status": "Todo",
        "question": "Employee (id, name, salary, departmentId), Department (id, name)\nFind employees who are high earners in each department (top 3 unique salaries in department).",
        "solution": "WITH RankedSalaries AS (\n    SELECT \n        d.name AS Department,\n        e.name AS Employee,\n        e.salary AS Salary,\n        DENSE_RANK() OVER (\n            PARTITION BY e.departmentId \n            ORDER BY e.salary DESC\n        ) AS rnk\n    FROM Employee e\n    JOIN Department d ON e.departmentId = d.id\n)\nSELECT Department, Employee, Salary\nFROM RankedSalaries\nWHERE rnk <= 3;",
        "notes": "Use DENSE_RANK() because problem requires top 3 'unique' salaries, allowing ties to share ranks."
    },

    # --- ADVANCED STRING / REGEX / CLAUSES ---
    {
        "id": 1667,
        "title": "1667. Fix Names in a Table",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "String Manipulation",
        "status": "Todo",
        "question": "Users (user_id, name)\nFix names so only first character is uppercase and rest are lowercase. Order by user_id.",
        "solution": "SELECT \n    user_id,\n    CONCAT(UPPER(SUBSTRING(name, 1, 1)), LOWER(SUBSTRING(name, 2))) AS name\nFROM Users\nORDER BY user_id;",
        "notes": "CONCAT + UPPER(SUBSTRING(name, 1, 1)) + LOWER(SUBSTRING(name, 2))."
    },
    {
        "id": 1527,
        "title": "1527. Patients With a Condition",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "String Pattern Matching / REGEXP",
        "status": "Todo",
        "question": "Patients (patient_id, patient_name, conditions)\nFind patient_id, patient_name, and conditions of patients who have Type I Diabetes (code starting with DIAB1).",
        "solution": "SELECT patient_id, patient_name, conditions\nFROM Patients\nWHERE conditions LIKE 'DIAB1%' OR conditions LIKE '% DIAB1%';",
        "notes": "Beware: conditions can have space-separated codes like 'SNDI10 DIAB100'. Match beginning or preceded by space."
    },
    {
        "id": 196,
        "title": "196. Delete Duplicate Emails",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "DELETE Statement / Self Join",
        "status": "Todo",
        "question": "Person (id, email)\nDelete all duplicate emails, keeping only one unique email with the smallest id.",
        "solution": "DELETE p1\nFROM Person p1\nJOIN Person p2\nWHERE p1.email = p2.email AND p1.id > p2.id;",
        "notes": "DELETE p1 using a self-join where p1.id > p2.id keeps the lowest id."
    },
    {
        "id": 176,
        "title": "176. Second Highest Salary",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Medium",
        "topic": "Subquery / Aggregation",
        "status": "Todo",
        "question": "Employee (id, salary)\nFind second highest distinct salary. If no second highest salary exists, return null.",
        "solution": "SELECT MAX(salary) AS SecondHighestSalary\nFROM Employee\nWHERE salary < (SELECT MAX(salary) FROM Employee);",
        "notes": "Subquery with MAX automatically returns NULL when there is no matching record."
    },
    {
        "id": 1484,
        "title": "1484. Group Sold Products By The Date",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "GROUP_CONCAT",
        "status": "Todo",
        "question": "Activities (sell_date, product)\nFind for each date the number of different products sold and their names sorted lexicographically, comma separated.",
        "solution": "SELECT \n    sell_date,\n    COUNT(DISTINCT product) AS num_sold,\n    GROUP_CONCAT(DISTINCT product ORDER BY product ASC SEPARATOR ',') AS products\nFROM Activities\nGROUP BY sell_date\nORDER BY sell_date;",
        "notes": "GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',') in MySQL."
    },
    {
        "id": 1327,
        "title": "1327. List the Products Ordered in a Period",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "HAVING / Date Filter",
        "status": "Todo",
        "question": "Products (product_id, product_name, category), Orders (product_id, order_date, unit)\nGet names of products that have >= 100 units ordered in February 2020.",
        "solution": "SELECT p.product_name, SUM(o.unit) AS unit\nFROM Products p\nJOIN Orders o ON p.product_id = o.product_id\nWHERE o.order_date BETWEEN '2020-02-01' AND '2020-02-29'\nGROUP BY p.product_id, p.product_name\nHAVING unit >= 100;",
        "notes": "Filter dates to 2020-02, group by product, check SUM(unit) >= 100."
    },
    {
        "id": 1517,
        "title": "1517. Find Users With Valid E-Mails",
        "platform": "LeetCode (SQL 50)",
        "difficulty": "Easy",
        "topic": "Regex Matching",
        "status": "Todo",
        "question": "Users (user_id, name, mail)\nValid mail has prefix name starting with letter, followed by letters/digits/underscore/dash/period, domain '@leetcode.com'.",
        "solution": "SELECT user_id, name, mail\nFROM Users\nWHERE mail REGEXP '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode[.]com$';",
        "notes": "In regex: escape period `[.]` or `\\\\.` so it doesn't match any character."
    },

    # ==================== 12 CURATED OA PROBLEMS ====================
    {
        "id": 178,
        "title": "178. Rank Scores",
        "platform": "LeetCode (OA Tracker #1)",
        "difficulty": "Medium",
        "topic": "Window Functions (DENSE_RANK)",
        "status": "Todo",
        "question": "Scores (id, score)\nRank the scores. If there is a tie, both should have same rank. Next rank number should be next consecutive integer (no holes). Order by score DESC.",
        "solution": "SELECT \n    score,\n    DENSE_RANK() OVER (ORDER BY score DESC) AS `rank`\nFROM Scores;",
        "notes": "Use DENSE_RANK() rather than RANK() to ensure consecutive numbers with no gaps."
    },
    {
        "id": 184,
        "title": "184. Department Highest Salary",
        "platform": "LeetCode (OA Tracker #2)",
        "difficulty": "Medium",
        "topic": "Partition By + Filtering Top-1",
        "status": "Todo",
        "question": "Employee (id, name, salary, departmentId), Department (id, name)\nFind employees who have the highest salary in each department.",
        "solution": "WITH Ranked AS (\n    SELECT \n        d.name AS Department,\n        e.name AS Employee,\n        e.salary AS Salary,\n        DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC) AS rnk\n    FROM Employee e\n    JOIN Department d ON e.departmentId = d.id\n)\nSELECT Department, Employee, Salary\nFROM Ranked\nWHERE rnk = 1;",
        "notes": "DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) handles ties for #1 spot cleanly."
    },
    {
        "id": 601,
        "title": "601. Human Traffic of Stadium",
        "platform": "LeetCode (OA Tracker #4)",
        "difficulty": "Hard",
        "topic": "Gaps & Islands / Consecutive Row Logic",
        "status": "Todo",
        "question": "Stadium (id, visit_date, people)\nDisplay records with three or more consecutive rows with people >= 100, ordered by visit_date ASC.",
        "solution": "WITH Filtered AS (\n    SELECT \n        id, visit_date, people,\n        id - ROW_NUMBER() OVER (ORDER BY id) AS grp\n    FROM Stadium\n    WHERE people >= 100\n),\nGroupCounts AS (\n    SELECT *, COUNT(*) OVER (PARTITION BY grp) AS cnt\n    FROM Filtered\n)\nSELECT id, visit_date, people\nFROM GroupCounts\nWHERE cnt >= 3\nORDER BY visit_date;",
        "notes": "Classic Gaps & Islands pattern: `id - ROW_NUMBER()` produces identical group keys for consecutive integers!"
    },
    {
        "id": 1709,
        "title": "1709. Biggest Window Between Visits",
        "platform": "LeetCode (OA Tracker #5)",
        "difficulty": "Medium",
        "topic": "Date Arithmetic + LEAD()",
        "status": "Todo",
        "question": "UserVisits (user_id, visit_date)\nFind the biggest window in days between consecutive visits for each user. Assume today is '2021-1-1'.",
        "solution": "WITH NextVisits AS (\n    SELECT \n        user_id,\n        visit_date,\n        LEAD(visit_date, 1, '2021-01-01') OVER (\n            PARTITION BY user_id ORDER BY visit_date\n        ) AS next_visit\n    FROM UserVisits\n)\nSELECT \n    user_id,\n    MAX(DATEDIFF(next_visit, visit_date)) AS biggest_window\nFROM NextVisits\nGROUP BY user_id\nORDER BY user_id;",
        "notes": "LEAD(visit_date, 1, '2021-01-01') allows specifying a default fallback date for the last visit."
    },
    {
        "id": 1308,
        "title": "1308. Running Total for Different Genders",
        "platform": "LeetCode (OA Tracker #7)",
        "difficulty": "Medium",
        "topic": "Cumulative Sum (SUM() OVER (PARTITION BY ... ORDER BY ...))",
        "status": "Todo",
        "question": "Scores (player_name, gender, day, score_points)\nFind the cumulative sum of score_points for each gender on each day, ordered by gender ASC, day ASC.",
        "solution": "SELECT \n    gender,\n    day,\n    SUM(score_points) OVER (\n        PARTITION BY gender \n        ORDER BY day\n    ) AS total_score\nFROM Scores\nORDER BY gender, day;",
        "notes": "SUM() OVER (PARTITION BY gender ORDER BY day) calculates running sum independently for each gender."
    },
    {
        "id": 1158,
        "title": "1158. Market Analysis I",
        "platform": "LeetCode (OA Tracker #9)",
        "difficulty": "Medium",
        "topic": "Date Extraction & Conditional Aggregation",
        "status": "Todo",
        "question": "Users (user_id, join_date, favorite_brand), Orders (order_id, order_date, item_id, buyer_id, seller_id)\nFind for each user their join date and the number of orders they made as a buyer in 2019.",
        "solution": "SELECT \n    u.user_id AS buyer_id,\n    u.join_date,\n    COUNT(o.order_id) AS orders_in_2019\nFROM Users u\nLEFT JOIN Orders o \n  ON u.user_id = o.buyer_id \n AND YEAR(o.order_date) = 2019\nGROUP BY u.user_id, u.join_date;",
        "notes": "CRUCIAL: Put `YEAR(o.order_date) = 2019` in the LEFT JOIN condition, NOT in the WHERE clause, so users with 0 orders remain!"
    },
    {
        "id": 9991,
        "title": "DataLemur: Highest-Grossing Items",
        "platform": "DataLemur (OA Tracker #11)",
        "difficulty": "Medium",
        "topic": "Multi-Level Grouping + RANK()",
        "status": "Todo",
        "question": "product_spend (category, product, user_id, spend, transaction_date)\nIdentify top 2 highest-grossing products within each category in the year 2022. Output category, product, total_spend.",
        "solution": "WITH TotalSpend AS (\n    SELECT \n        category,\n        product,\n        SUM(spend) AS total_spend,\n        RANK() OVER (\n            PARTITION BY category \n            ORDER BY SUM(spend) DESC\n        ) AS ranking\n    FROM product_spend\n    WHERE EXTRACT(YEAR FROM transaction_date) = 2022\n    GROUP BY category, product\n)\nSELECT category, product, total_spend\nFROM TotalSpend\nWHERE ranking <= 2\nORDER BY category, ranking;",
        "notes": "Group by category and product first, compute total spend, and partition RANK() by category."
    },
    {
        "id": 262,
        "title": "262. Trips and Users",
        "platform": "LeetCode (OA Tracker #12)",
        "difficulty": "Hard",
        "topic": "Complex Date Filters & Cancellation Ratios",
        "status": "Todo",
        "question": "Trips (id, client_id, driver_id, city_id, status, request_at), Users (users_id, banned, role)\nCancellation rate = unbanned cancelled trips / unbanned total requests between '2013-10-01' and '2013-10-03'. Round to 2 decimals.",
        "solution": "SELECT \n    t.request_at AS Day,\n    ROUND(\n        SUM(t.status IN ('cancelled_by_driver', 'cancelled_by_client')) / COUNT(*), \n        2\n    ) AS `Cancellation Rate`\nFROM Trips t\nJOIN Users c ON t.client_id = c.users_id AND c.banned = 'No'\nJOIN Users d ON t.driver_id = d.users_id AND d.banned = 'No'\nWHERE t.request_at BETWEEN '2013-10-01' AND '2013-10-03'\nGROUP BY t.request_at\nORDER BY Day;",
        "notes": "Both client and driver must NOT be banned (join Users twice on banned = 'No'). Then group by request_at."
    }
]

# Write to questions.json
out_file = "C:/Users/mohit/Desktop/finalprep/SQL/questions.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(DATA, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(DATA)} questions into {out_file}")
