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
    recipe_ID serial,
    username varchar(255) REFERENCES users(email),
    headline varchar(255), 
    preamble text, 
    instructions text, 
    published varchar(255),
    PRIMARY KEY(recipe_ID)
);

create table ingredient_in_recipe(
    ingredient_name varchar(255),
    recipe_ID integer REFERENCES recipe(recipe_ID),
    volume integer,
    measurement varchar(255),
    PRIMARY KEY(ingredient_name)
);

create table ingredient(
    ingredient_name varchar(255),
    PRIMARY KEY(ingredient_name)
);

create table comment(
    comment_ID serial,
    recipe_ID integer REFERENCES recipe(recipe_ID), 
    username varchar(255) REFERENCES users(email), 
    comment text, 
    curr_time varchar(255), 
    PRIMARY KEY (comment_ID)
);

create table images(
    image_ID serial,
    image_filename varchar(255),
    alt_text varchar(255),
    PRIMARY KEY(image_ID)
);

create table images_in_recipe(
    image_ID integer REFERENCES images(image_ID), 
    recipe_ID integer REFERENCES recipe(recipe_ID), 
    image_text text, 
    CONSTRAINT images_in_recipe_ID PRIMARY KEY(image_ID, recipe_ID)
);

create table images_in_profile(
    image_ID integer REFERENCES images(image_ID), 
    username varchar(255) REFERENCES users(email), 
    image_text text, 
    CONSTRAINT images_in_profile_ID PRIMARY KEY(image_ID, username)
);

