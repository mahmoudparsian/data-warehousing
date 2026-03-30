-- --------------------------------
-- Transactional Database Schema
-- --------------------------------

create database movies_db;

drop table movies;
drop table users;
drop table ratings;


-- #### Table: `movies`
create table movies(
    movie_id INT,
    movie_title VARCHAR(60),       
    genre  VARCHAR(20),
    release_year INT
);

-- #### Table: `users`
create table users(
    user_id INT,
    user_name VARCHAR(60)      
);

-- #### Table: `ratings`
create table ratings(
    rating_id INT,
    movie_id INT,     
    user_id INT,
    rating INT, -- 1, 2, 3, ..., 10
    rating_date Date
);
