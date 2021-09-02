-- SQLite
-- delete from jobs where job_id = 11;
-- SELECT job_id, user_id, file_count, time
-- FROM jobs;

-- .tables

-- SELECT name FROM sqlite_master WHERE type='table'
-- .fullschema
-- SELECT name FROM sqlite_master WHERE type ='table'

-- DELETE from users;
-- DELETE FROM profile;
-- DELETE FROM jobs;

-- DROP TABLE jobs;
-- DROP TABLE profile;
-- DROP TABLE users;

-- CREATE TABLE 'users' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' text NOT NULL UNIQUE, 'email' text NOT NULL UNIQUE, 'hash' text NOT NULL, 'time' text NOT NULL);
-- CREATE TABLE 'profile' ('id' integer PRIMARY KEY NOT NULL, 'fname' text NOT NULL, 'lname' text NOT NULL);
-- CREATE TABLE 'jobs' ('job_id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' integer NOT NULL, 'file_count' integer NOT NULL, 'time' text NOT NULL);


-- CREATE TABLE 'users' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' text NOT NULL UNIQUE, 'email' text NOT NULL UNIQUE, 'hash' text NOT NULL, 'time' text NOT NULL);
-- CREATE TABLE 'profile' ('id' integer PRIMARY KEY NOT NULL REFERENCES users(id), 'fname' text NOT NULL, 'lname' text NOT NULL);
-- CREATE TABLE 'jobs' ('job_id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' integer NOT NULL REFERENCES users(id), 'task_type' text NOT NULL, 'file_count' integer NOT NULL, 'status' text DEFAULT ('NA'), 'time' text NOT NULL, 'completion_time' text NOT NULL);

-- CREATE TABLE 'users' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' text NOT NULL UNIQUE, 'email' text NOT NULL UNIQUE, 'hash' text NOT NULL, 'time' text NOT NULL);
-- CREATE TABLE 'profile' ('id' integer PRIMARY KEY NOT NULL REFERENCES users(id), 'fname' text NOT NULL, 'lname' text NOT NULL);
-- CREATE TABLE 'jobs' ('job_id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' integer NOT NULL REFERENCES users(id), 'task_type' text NOT NULL, 'file_count' integer NOT NULL, 'status' text DEFAULT ('NA'), 'time' text NOT NULL, 'completion_time' text NOT NULL);

DROP TABLE jobs;
DROP TABLE profile;
DROP TABLE users;

CREATE TABLE 'users' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' text NOT NULL UNIQUE, 'email' text NOT NULL UNIQUE, 'hash' text NOT NULL, 'time' text NOT NULL);
CREATE TABLE 'profile' ('id' integer PRIMARY KEY NOT NULL REFERENCES users(id), 'fname' text NOT NULL, 'lname' text NOT NULL);
CREATE TABLE 'jobs' ('job_id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' integer NOT NULL REFERENCES users(id), 'task_type' text NOT NULL, 'file_count' integer NOT NULL, 'status' text DEFAULT ('NA'), 'creation_time' text NOT NULL, 'completion_time' text NOT NULL);

.quit

-- DROP TABLE jobs;
-- DROP TABLE profile;
-- DROP TABLE users;
