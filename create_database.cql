CREATE KEYSPACE IF NOT EXISTS email_database WITH REPLICATION = {
	'class': 'SimpleStrategy', 'replication_factor': 1 };
	
USE email_database;

CREATE TABLE IF NOT EXISTS emails (sender TEXT, id UUID, timestamp TIMESTAMP, receiver TEXT, datetime TEXT, subject TEXT, body TEXT, label TEXT, PRIMARY KEY (sender, id));



/* CREATE KEYSPACE IF NOT EXISTS email_database WITH replication = {'class': 'SingleRegionStrategy'};
CREATE TABLE IF NOT EXISTS email_database.emails (sender text, id uuid, timestamp timestamp, receiver text, datetime text, subject text, body text, label text, PRIMARY KEY (sender, id));
USE email_database;
CONSISTENCY LOCAL_QUORUM;
INSERT INTO emails (sender, id, timestamp, receiver, datetime, subject, body, label) VALUES ('John', 50554d6e-29bb-11e5-b345-feff819cdc9f, toUnixTimestamp(now()), 'john@example.com', 'money', '12-11-30', '[a,b,c]', 'spam');
SELECT * FROM emails;
 */ -- AWS