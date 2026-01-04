use student_db;

create table students (
  sid    INT, 
  name   VARCHAR(15), 
  login  VARCHAR(25),
  age    INT, 
  gpa    DOUBLE,
  
  PRIMARY KEY (sid)
);

insert into students (sid, name, login, age, gpa) values
(50000, 'Dave', 'dave@cs.org', 19, 3.3),
(53666, 'Jones', 'jones@cs.com', 18, 3.4),
(53688, 'Smith', 'smith@ee.org', 18, 3.2),
(53650, 'Smith', 'smith@math.com', 19, 3.8),
(53831, 'Madayan', 'madayan@music.com', 11, 1.8),
(53832, 'Guldu', 'guldu@music', 12, 2.0),
(54000, 'Taylor', 'taylor@cnn.com', 28, 2.2),
(55000, 'Macain', 'mac@cbs.com', 29, 3.8),
(56000, 'Rafaei', 'rafa@tennis.com', 37, 4.0),
(57000, 'Newton', 'new@news.com', 12, 2.0);

create table courses (
  cid VARCHAR(25), 
  instructor VARCHAR(25), 
  quarter VARCHAR(15), 
  dept VARCHAR(15),
  
  PRIMARY KEY (cid)
);

insert into courses(cid, instructor, quarter, dept) values
('Carnatic101', 'Jane', 'Fall 06', 'Music'),
('Reggae203', 'Bob', 'Summer 06', 'Music'),
('Topology101', 'Mary', 'Spring 06', 'Math'),
('History105', 'Alice', 'Fall 06', 'History'),
('BigData24', 'Rafael', 'Spring 06', 'CS'),
('Java12', 'Rafael', 'Spring 06', 'CS');


create table enrolled (
  cid VARCHAR(25),
  grade VARCHAR(2),
  studid INT,
  
  FOREIGN KEY (cid) REFERENCES courses(cid),
  FOREIGN KEY (studid) REFERENCES students(sid)
);

insert into  enrolled(cid, grade, studid) values
('Carnatic101', 'C', 53831),
('Reggae203', 'B', 53832),
('Topology101', 'A', 53650),
('History105', 'B', 53666),
('BigData24', 'B', 54000),
('Java12', 'A', 54000),
('BigData24', 'C', 57000),
('Java12', 'C', 57000),
('Carnatic101', 'A', 56000),
('Reggae203', 'B', 56000);

-- join:
-- S is an alias for students table
-- E is an alias for enrolled table
select S.sid, S.name, S.gpa, E.cid, E.grade, E.studid
   from students S,
        enrolled E
    where S.sid = E.studid;
    
   