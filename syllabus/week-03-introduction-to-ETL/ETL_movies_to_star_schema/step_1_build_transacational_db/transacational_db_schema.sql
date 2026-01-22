-- --------------------------------
-- Transactional Database Schema
-- --------------------------------

create database movies_db;

drop table movies;
drop table users;
drop table ratings;


USE movies_db;

-- #### Table: `movies`
CREATE TABLE movies (
    imdm_title_id VARCHAR(255),
    title VARCHAR(255),
    original_title VARCHAR(255),
    year int,
    date_published VARCHAR(255),
    genre VARCHAR(255),
    duration INT,
    country  VARCHAR(255),
    language_1  VARCHAR(255),
    language_2  VARCHAR(255),
    language_3  VARCHAR(255),
    director  VARCHAR(255),
    writer  VARCHAR(255),
    actors  VARCHAR(955),
    actors_1  VARCHAR(955),
    actors_f2  VARCHAR(955),
    description  VARCHAR(255),
    desc35  VARCHAR(255),
    avg_vote DOUBLE,
    votes INT,
    budget INT,
    usa_gross_income INT,
    worlwide_gross_income INT,
    reviews_from_users INT
) CHARACTER SET utf8 COLLATE utf8_general_ci;


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
