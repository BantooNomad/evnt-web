CREATE SEQUENCE task_id_seq START WITH 1 MINVALUE 1 INCREMENT BY 1;

/*  Drop if table exists
	$ psql -h hostname -U synod -d LinkUs -f psql.sql
*/

DROP TABLE Tasks;
DROP TABLE Admin;
DROP TABLE Payments;
DROP TABLE UsersInfo;
DROP TABLE NewsLetter;


CREATE TABLE Tasks(task_id INTEGER DEFAULT nextval('task_id_seq') PRIMARY KEY NOT NULL, task_title varchar(200) NOT NULL, 
	task_desc TEXT NOT NULL, due_date DATE NOT NULL, task_status varchar(100) NOT NULL, 
	username varchar(200) NOT NULL, task_category varchar(100) NOT NULL);


CREATE TABLE UsersInfo(email varchar(200) NOT NULL UNIQUE, mobileNo varchar(100) NOT NULL, 
	dob DATE NOT NULL, password TEXT NOT NULL, smscode DOUBLE PRECISION, 
	state varchar(100) NOT NULL, username VARCHAR(200) NOT NULL PRIMARY KEY);


CREATE TABLE Payments(credit_available INTEGER NOT NULL, username VARCHAR(200) NOT NULL PRIMARY KEY);


CREATE TABLE Admin(username VARCHAR(200) NOT NULL PRIMARY KEY, password VARCHAR(200) NOT NULL);

CREATE TABLE NewsLetter(username VARCHAR(200) NOT NULL PRIMARY KEY, email VARCHAR(200) UNIQUE NOT NULL);