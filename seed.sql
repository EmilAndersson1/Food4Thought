/*SQL kod med insert satser till databasen*/

/*user inserts*/
insert into user(email, firstname, lastname, user_password, username, biography)
values
    (samuel_ahlberg@hotmail.com, Samuel, Ahlberg, 123, samuelahlberg, cool kille);


/*recipe inserts*/
insert into recipe(recipe_ID, headline, preamble, instructions, published)
values();

/*ingridient inserts*/
insert into ingridient(ingredient_name)
values
    (paprika),
    (gurka),
    (kyckling),
    (ris),
    (spenat);

/*comment inserts*/
insert into comment(comment_ID, comment, curr_time)
values();
