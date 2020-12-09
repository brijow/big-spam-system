CREATE KEYSPACE IF NOT EXISTS email_database WITH REPLICATION = {
	'class': 'SimpleStrategy', 'replication_factor': 1 };
	
USE email_database;

CREATE TABLE IF NOT EXISTS emails (current_date DATE, id UUID, sender TEXT, receiver TEXT, receive_date TEXT, subject TEXT, body TEXT, label TEXT, PRIMARY KEY (current_date, id));



/* CREATE KEYSPACE IF NOT EXISTS email_database WITH replication = {'class': 'SingleRegionStrategy'};
USE email_database;
CREATE TABLE IF NOT EXISTS email_database.emails (current_date DATE, id UUID, sender TEXT, receiver TEXT, receive_date TEXT, subject TEXT, body TEXT, label TEXT, PRIMARY KEY (current_date, id));
CONSISTENCY LOCAL_QUORUM;
INSERT INTO emails (current_date, id, sender, receiver, receive_date, subject, body, label) VALUES (toDate(toUnixTimestamp(now())), 50554d6e-29bb-11e5-b345-feff819cdc9f, 'John', 'john@example.com', '12-11-30', 'money', '[a,b,c]', 'spam');
SELECT * FROM emails;
 */ -- AWS