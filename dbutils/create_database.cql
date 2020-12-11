CREATE KEYSPACE IF NOT EXISTS email_database WITH REPLICATION = {
	'class': 'SimpleStrategy', 'replication_factor': 1 };
	
USE email_database;

CREATE TABLE IF NOT EXISTS emails (current_date DATE, id INT, sender TEXT, receiver TEXT, receive_date TEXT, subject TEXT, word_tokens list<TEXT>, label TEXT, PRIMARY KEY (current_date, id));