--1 , to get user id --> SELECT id FROM users ORDER BY RANDOM() LIMIT 1;
SELECT * FROM tasks WHERE user_id = <user_id>;

--2, for status id --> SELECT id FROM status ORDER BY RANDOM() LIMIT 1;
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');

--3 for task id--> SELECT id FROM tasks ORDER BY RANDOM() LIMIT 1;
UPDATE tasks SET status_id = <new_status_id> WHERE id = <task_id>;

--4
SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

--5
INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task', 'Task Description', <status_id>, <user_id>);

--6
SELECT * FROM tasks WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');

--7
DELETE FROM tasks WHERE id = <task_id>;

--8 for email--> SELECT email FROM users ORDER BY RANDOM() LIMIT 1;
SELECT * FROM users WHERE email LIKE '%@example.com';

--9
UPDATE users SET fullname = '<new_fullname>' WHERE id = <user_id>;


--10
SELECT status.name, COUNT(tasks.id) AS task_count
FROM tasks
INNER JOIN status ON tasks.status_id = status.id
GROUP BY status.name;


SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com';

SELECT * FROM tasks WHERE description IS NULL OR description = '';

SELECT users.fullname, tasks.title
FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';


SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.fullname;


