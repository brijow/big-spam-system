USE email_database;

/* SELECT * from emails WHERE current_date = '2020-12-08'; -- allow select based on timestamp */

DELETE FROM emails WHERE current_date = '2020-12-09'; -- clean the old records based on date

TRUNCATE emails; -- clean the entire table 

/* DROP TABLE IF EXISTS "email_database".emails; */ -- AWS do not have TRUNCATE
