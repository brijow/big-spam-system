import sys
import re, uuid
import nltk, nltk.stem.porter
from simplified_scrapy.simplified_doc import SimplifiedDoc 
from pyspark.sql import SparkSession, functions as f, types

sender_regex = r'From:[^<]+<([^\n]+)>'
receiver_regex = r'To: ([^\n]+)'
subject_regex = r'Subject: ([^\n]+)'
body_regex = r'\n\n([\H\n\s]*)'
date_regex = r'Date: +([^\n]+)'
cassandra_host = 'localhost'

def simplify_doc_udf(html_text):
	doc = SimplifiedDoc(html_text)
	return doc.text

def process_email_body(email_body):
    
    email_body = email_body.split("--", 1)
    
    #Removing non-ASCII characters results in a string that only contains ASCII characters.
    encoded_string = email_body[0].encode("ascii", "ignore")
    decode_string = encoded_string.decode()
    
    lower_string = decode_string.lower()
    #Looks for any expression that starts with < and ends with > and replace and does not have any < or > in the tag it with a space
    lower_string = re.sub('<[^<>]+>', ' ', lower_string)

    # Any numbers get replaced with the string 'number'
    lower_string = re.sub('[0-9]+', 'number', lower_string)

    # Anything starting with http or https:// replaced with 'httpaddr'
    lower_string = re.sub('(http|https)://[^\s]*', 'httpaddr', lower_string)

    # Strings with "@" in the middle are considered emails --> 'emailaddr'
    lower_string = re.sub('[^\s]+@[^\s]+', 'emailaddr', lower_string)

    # The '$' sign gets replaced with 'dollar'
    lower_string = re.sub('[$]+', 'dollar', lower_string)
    
    # Word list of email body
    word_list = re.split('[^\w-]+',lower_string.strip())
    
    stemmer = nltk.stem.porter.PorterStemmer()
    
    result_list = []
    for word in word_list:
        if len(word) >= 1:
            word = re.sub('[^a-zA-Z0-9]', '', word)
            word = stemmer.stem(word)
            result_list.append(word)
    return(result_list)
    #print(result_list)
        
    
def main(inputs, output):
	html_to_plain_udf = f.udf(simplify_doc_udf, types.StringType())
	process_body_udf = f.udf(process_email_body, types.ArrayType(types.StringType()))
	raw_email = spark.read.text(inputs, wholetext = True)
	send_to_cassandra = raw_email.select(\
		f.regexp_extract('value', sender_regex, 1).alias('sender'), \
		f.regexp_extract('value', receiver_regex, 1).alias('receiver'), \
		f.regexp_extract('value', subject_regex, 1).alias('subject'), \
		f.regexp_extract('value', date_regex, 1).alias('receive_date'), \
		f.regexp_extract('value', body_regex, 1).alias('html_body'))\
	.withColumn('id', uuid.uuid1())\
    .withColumn('current_date', toDate(toUnixTimestamp(now()))\
	.withColumn('body', html_to_plain_udf('html_body'))\
	.withColumn('word_tokens', process_body_udf('body'))
    
    
    #CREATE TABLE IF NOT EXISTS emails (current_date DATE, id UUID, sender TEXT, receiver TEXT, receive_date TEXT, subject TEXT, body TEXT, label TEXT, PRIMARY KEY (current_date, id));
    
    #INSERT INTO emails (current_date, id, sender, receiver, receive_date, subject, body, label) VALUES (toDate(toUnixTimestamp(now())), 50554d6e-29bb-11e5-b345-feff819cdc9f, 'John', 'john@example.com', '12-11-30', 'money', '[a,b,c]', 'spam');
	
	send_to_cassandra.select('current_date', 'id', 'sender', 'receiver', 'receive_date', 'subject', 'word_tokens').write.json(output, mode='overwrite')
	
	#send_to_cassandra.write.format("org.apache.spark.sql.cassandra")\
	#	.options(table = 'email', keyspace = 'email_database').save()
	
	
	
	
	
	
	
	
	
if __name__ == '__main__':
	inputs = sys.argv[1]
	output = sys.argv[2]
	spark = SparkSession.builder.appName('email ETL')\
		.config('spark.cassandra.connection.host', cassandra_host).getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	main(inputs, output)
