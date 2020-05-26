/*SQL kod för att skapa alla tabeller som används i programmet*/

create table users(
    email varchar(255), 
    firstname varchar(255),
    lastname varchar(255),
    user_password varchar(255),
    username varchar (255),
    biography text,
    PRIMARY KEY(email)
);

create table recipe(
    recipe_id serial,
    username varchar(255) REFERENCES users(email),
    title varchar(255), 
    recipe_description text, 
    instructions text,
    time_published varchar(255),
    PRIMARY KEY(recipe_ID)
);

create table ingredient(
    ingredient_id serial,
    ingredient_name varchar(255),
    volume integer,
    measurement varchar(255),
    PRIMARY KEY(ingredient_id)
);

create table ingredient_in_recipe(
    ingredient_id integer REFERENCES ingredient(ingredient_id),
    recipe_ID integer REFERENCES recipe(recipe_ID),
    CONSTRAINT ingredient_in_recipe_id PRIMARY KEY(ingredient_id, recipe_id)
);

create table comment(
    comment_id serial,
    recipe_id integer REFERENCES recipe(recipe_ID), 
    username varchar(255) REFERENCES users(email), 
    comment text, 
    curr_time varchar(255), 
    PRIMARY KEY (comment_id)
);

create table images(
    image_id serial,
    image_filename bytea,
    PRIMARY KEY(image_id)
);

create table images_in_recipe(
    image_id integer REFERENCES images(image_id), 
    recipe_id integer REFERENCES recipe(recipe_id), 
    image_text text, 
    CONSTRAINT images_in_recipe_id PRIMARY KEY(image_id, recipe_id)
);

create table images_in_profile(
    image_id integer REFERENCES images(image_id), 
    username varchar(255) REFERENCES users(email), 
    image_text text, 
    CONSTRAINT images_in_profile_id PRIMARY KEY(image_id, username)
);

