drop database music;

create database music;

use music;

-- users table
-- This table defines users of the music streaming service
--
--	user_id: The unique identifier of the user
--	user_name: The name of the user
--	email: The email address of the user
--	country: The country where the user is located
--	plan: The subscription plan of the user, either ‘free’ or ‘premium’
--
DROP TABLE IF EXISTS users;
--
create table users(
	user_id int,
	user_name text,
	email text,
	country text,
	plan text
);

insert into users(user_id, user_name, email, country, plan)
values
(100, 'alex',   'alex@apple.com',    'USA',    'premium'),
(150, 'bob',    'bob@cnn.com',       'USA',    'premium'),
(200, 'jane',   'jane@cbs.com',      'USA',    'premium'),
(300, 'betty',  'bet@fb.com',        'USA',    'free'),
(400, 'rafa',   'rafa@tennis.com',   'USA',    'free'),
(500, 'ted',    'ted@tennis.com',    'CANADA', 'premium'),
(600, 'jeff',   'jeff@tennis.com',   'CANADA', 'premium'),
(700, 'max',    'max@tennis.com',    'CANADA', 'free'),
(750, 'terry',  'terry@tennis.com',  'CANADA', 'free'),
(800, 'al',     'al@gmail.com',      'SPAIN',  'premium'),
(900, 'david',  'david@tennis.com',  'SPAIN',  'premium'),
(800, 'carlos', 'carlos@tennis.com', 'SPAIN',  'free'),
(900, 'fiona',  'fiona@gmail.com',   'SPAIN',  'free'),
(500, 'albert', 'albert@pbs.com',    'FRANCE', 'premium'),
(550, 'suzie',  'suzie@tennis.com',  'FRANCE', 'premium'),
(570, 'ted',    'ted@tennis.com',    'FRANCE', 'free'),
(610, 'vera',   'vera@tennis.com',   'BRAZIL', null),
(611, 'maz',    'ted@tennis.com',    'BRAZIL', null),
(612, 'hamid',  'hamid@tennis.com',  'BRAZIL', null),
(711, 'dammer', 'dam@tennis.com',    'BRAZIL', 'premium'),
(712, 'hamid',  'hamid@tennis.com',  'BRAZIL', 'free');

-- songs table
-- This table hits the right notes with details on 
-- the service’s song library. It includes:
--
--	song_id: The unique identifier of the song
--  title: The title of the song
--	artist: The name of the artist who performed the song
--	genre: The genre of the song
--	duration: The duration of the song in seconds
--
DROP TABLE IF EXISTS songs;
--
create table songs (
 song_id int,
 title text,
 artist text,
 genre text,
 duration int
);

insert into songs (song_id, title, artist, genre, duration)
values
(1, 'The 1',               'Taylor Swift', 'country', 195),
(2, 'Afterglow',           'Taylor Swift', 'country', 191),
(3, 'All Too Well',        'Taylor Swift', 'country', 182),
(4, 'Please Please Me',    'Beatles',      'rock', 175),
(5, 'With the Beatles',    'Beatles',      'rock', 181),
(6, 'Beatles for Sale',    'Beatles',      'rock', 189),
(7, '1000 Nights',         'Ed Sheeran',      'pop', 125),
(8, '2step',               'Ed Sheeran',      'pop', 181),
(9, 'The A Team',          'Ed Sheeran',      'pop', 199),
(10, 'Clarinet Quintet',   'Mozart',      'classic', 302),
(11, 'Requiem In D Minor', 'Mozart',      'classic', 290),
(12, 'Piano Concerto',     'Mozart',      'classic', 249),
(13, 'Symphony No. 3',        'Beethoven',      'classic', 302),
(14, 'Symphony No. 9',        'Beethoven',      'classic', 290),
(15, 'String Quartet No. 14', 'Beethoven',      'classic', 249),
(16, 'Ocean Eyes',        'Billie Eilish',      'pop', 260),
(17, 'Six Feet Under',    'Billie Eilish',      'pop', 270),
(18, 'Bored',             'Billie Eilish',      'pop', 280),
(19, 'Bad Guy',           'Billie Eilish',      'pop', 230),
(20, 'My Future',         'Billie Eilish',      'pop', 240),
(21, 'Good, bad, Ugly',   'Joe Franklin',      'pop', 200),
(22, 'My Journey to',     'Bob Taylor',        'pop', 240),
(23, 'Top Gun',           'Joe Pancho',      'country', 210),
(24, 'Long Road',         'Bob YoYo',        'country', 240);

-- dates table 
-- This table stores all required dates
--
-- date_id: as PK
-- play_date: play date of a song
-- year: the year of play_date
-- month: the month of play_date
-- day: the day of play_date
-- quarter: the quarter of play_date as {1, 2, 3, 4} 
--
CREATE TABLE dates (
    date_id INT PRIMARY KEY,
    play_date DATE,
    year INT,
    month INT,  -- {1, 2, ..., 12}
    day INT,    -- {1, 2, ..., 31}
    quarter INT -- {1, 2, 3, 4}
);

insert into dates(date_id, play_date, year, month, day, quarter)
values
(1,  '2020-01-01', 2020, 1, 1, 1),
(2,  '2020-01-02', 2020, 1, 2, 1),
(3,  '2020-01-03', 2020, 1, 3, 1),
(4,  '2020-01-04', 2020, 1, 4, 1),
(5,  '2020-04-01', 2020, 4, 1, 2),
(6,  '2020-04-02', 2020, 4, 2, 2),
(7,  '2020-04-03', 2020, 4, 3, 2),
(8,  '2020-04-04', 2020, 4, 4, 2),
(9,  '2020-07-01', 2020, 7, 1, 3),
(10, '2020-07-02', 2020, 7, 2, 3),
(11, '2020-07-03', 2020, 7, 3, 3),
(12, '2020-07-04', 2020, 7, 4, 3),
(13, '2020-11-01', 2020, 11, 1, 4),
(14, '2020-11-02', 2020, 11, 2, 4),
(15, '2020-11-03', 2020, 11, 3, 4),
(16, '2020-11-04', 2020, 11, 4, 4),
(17, '2021-10-01', 2021, 10, 1, 4),
(18, '2021-10-02', 2021, 10, 2, 4),
(19, '2021-10-03', 2021, 10, 3, 4),
(20, '2021-10-04', 2021, 10, 4, 4),
(21, '2022-10-01', 2022, 10, 1, 4),
(22, '2022-10-02', 2022, 10, 2, 4),
(23, '2022-10-03', 2022, 10, 3, 4),
(24, '2022-10-04', 2022, 10, 4, 4);

-- devices table
-- this table store various user devices, which played the song
-- device_id: as PK
-- device: name of the device such as 'mobile', 'desktop', 'ipad', or 'watch'
create table devices (
   device_id int,
   device text      
);

insert into devices(device_id, device)
values
(1, 'mobile'),
(2, 'desktop'),
(3, 'ipad'),
(4, 'watch'),
(5, 'glasses');

   
-- plays table
-- 
-- And here, we track every time a user plays a song. 
-- It’s filled with information on:
--
--	play_id:   The unique identifier of the play
--	user_id:   The user who played the song
--	song_id:   The song that was played
--	date_id:   The date when the song was played
--	device_id: The device used to play the song, either ‘mobile’ or ‘desktop’, ...
--
DROP TABLE IF EXISTS plays;
--
create table plays (
  play_id int,
  user_id int,
  song_id int,
  date_id int, 
  device_id int      -- 'mobile' or 'desktop' or 'ipad', 'watch'
);

insert into plays (play_id, user_id, song_id, date_id, device_id)
values
(1,  100, 1, 1, 1),
(2,  100, 1, 1, 1),
(3,  100, 1, 1, 1),
(4,  100, 2, 2, 2),
(5,  100, 2, 2, 2),
(6,  100, 9, 2, 2),
(7,  100, 9, 3, 2),
(8,  100, 4, 3, 1),
(9,  100, 4, 3, 3),
(10, 100, 4, 3, 3),
(11,  200, 1, 5, 1),
(12,  200, 1, 5, 1),
(13,  200, 1, 5, 2),
(14,  200, 3, 5, 2),
(15,  200, 3, 6, 2),
(16,  200, 3, 6, 3),
(17,  200, 7, 6, 3),
(18,  200, 7, 6, 4),
(19,  200, 7, 7, 4),
(20,  200, 8, 7, 4),
(21,  300, 14, 10, 1),
(22,  300, 15, 10, 1),
(23,  300, 16, 10, 1),
(24,  300, 3,  10, 2),
(25,  300, 3,  10, 2),
(26,  400, 10, 11, 1),
(27,  400, 10, 11, 1),
(28,  400, 11, 11, 2),
(29,  400, 11, 11, 2),
(30,  400, 12, 11, 2),
(31,  500, 1, 12, 3),
(32,  500, 1, 12, 3),
(33,  500, 7, 12, 3),
(34,  500, 7, 12, 1),
(35,  500, 7, 12, 1),
(36,  600, 10, 13, 1),
(37,  600, 10, 13, 1),
(38,  600, 14, 13, 1),
(39,  600, 14, 13, 2),
(40,  600, 14, 13, 2),
(41,  700, 14, 14, 1),
(42,  700, 14, 14, 1),
(43,  700, 17, 14, 3),
(44,  700, 17, 14, 3),
(45,  700, 17, 14, 3),
(46,  800, 8, 8, 1),
(47,  800, 8, 8, 1),
(48,  800, 9, 8, 2),
(49,  800, 9, 8, 2),
(50,  800, 9, 8, 1),
(51,  900, 1, 9, 2),
(52,  900, 1, 9, 2),
(53,  900, 1, 9, 1),
(54,  900, 5, 9, 1),
(55,  900, 5, 9, 1),
(56,  900, 6, 9, 1),
(57,  900, 6, 9, 1),
(58,  900, 8, 9, 2),
(59,  900, 8, 9, 2),
(60,  900, 8, 9, 1),
(61,  100, 11, 13, 2),
(62,  100, 11, 13, 2),
(63,  100, 12, 13, 1),
(64,  100, 12, 13, 1),
(65,  100, 12, 14, 1),
(66,  100, 4,  14, 1),
(67,  100, 4,  14, 1),
(68,  100, 8,  14, 2),
(69,  100, 8,  14, 2),
(70,  100, 8,  14, 1),
(71,  300, 1,  6, 2),
(72,  300, 1,  6, 2),
(73,  300, 3,  6, 1),
(74,  300, 3,  6, 1),
(75,  300, 7,  6, 1),
(76,  300, 7,  6, 1),
(77,  300, 9,  6, 1),
(78,  300, 9,  16, 2),
(79,  300, 14, 16, 2),
(80,  300, 14, 16, 1),
(81,  400, 8,  20, 2),
(82,  400, 8,  20, 2),
(83,  400, 9,  20, 1),
(84,  400, 9,  20, 1),
(85,  400, 7,  21, 1),
(86,  400, 7,  21, 1),
(87,  400, 1,  21, 1),
(88,  400, 1,  21, 2),
(89,  400, 14, 22, 2),
(90,  400, 14, 22, 1),
(91,  600, 10, 23, 2),
(92,  600, 10, 23, 2),
(93,  600, 11, 23, 1),
(94,  600, 11, 23, 1),
(95,  600, 14, 24, 1),
(96,  600, 14, 24, 1),
(97,  600, 16, 24, 1),
(98,  600, 16, 24, 2),
(99,  600, 4,  24, 2),
(100, 600, 4,  24, 1),
(101, 610, 3, 4, 1),
(102, 610, 4, 4, 1),
(103, 610, 5, 6, 2),
(104, 610, 6, 6, 2),
(105, 610, 7, 9, 1),
(106, 610, 7, 9, 1),
(107, 610, 8, 5, 1),
(108, 610, 8, 5, 1),
(109, 610, 18, 9, 1),
(110, 610, 19, 9, 1),
(111, 610, 18, 15, 3),
(112, 610, 19, 15, 3),
(113, 400, 1, 7, 1),
(114, 400, 2, 8, 1),
(115, 400, 3, 9, 3),
(116, 500, 4, 11, 4),
(117, 500, 5, 12, 1),
(118, 500, 1, 13, 2),
(119, 600, 2, 14, 3),
(120, 600, 13, 15, 4);

