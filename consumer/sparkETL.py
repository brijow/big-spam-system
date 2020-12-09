import sys
import re, uuid
import nltk, nltk.stem.porter
from simplified_scrapy.simplified_doc import SimplifiedDoc 
from pyspark.sql import SparkSession, functions as f, types

receiver_regex = r'To: ([^\n]+)'
sender_regex = r'From:[^<]+<([^\n]+)>'
subject_regex = r'Subject: ([^\n]+)'
body_regex = r'\n\n([\H\n\s]*)'
date_regex = r'Date: +([^\n]+)'
cassandra_host = 'localhost'

def simplify_doc_udf(html_text):
    doc = SimplifiedDoc(html_text)
    return doc.text

def process_email_body(email_body):
    
    if email_body is None:
        print("There is a none object")
        email_body = ""
    #Removing non-ASCII characters results in a string that only contains ASCII characters.
    encoded_string = email_body.encode("ascii", "ignore")
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

def uuid ():
    return (str(uuid.uuid4()))
    
def main(inputs, output):
    html_to_plain_udf = f.udf(simplify_doc_udf, types.StringType())
    process_body_udf = f.udf(process_email_body, types.ArrayType(types.StringType()))
    
	###########For testing #delete afterwards#########
    spam = spark.read.text("DontCommit/samplemail/spam", wholetext = True).withColumn('label', f.lit(1))
    ham = spark.read.text("DontCommit/samplemail/ham", wholetext = True).withColumn('label', f.lit(0))
    raw_email = spam.union(ham)
    ###########raw_email = spark.read.text(inputs, wholetext = True)#################
    send_to_cassandra = raw_email.select(\
        'label', \
        f.regexp_extract('value', sender_regex, 1).alias('sender'), \
        f.regexp_extract('value', receiver_regex, 1).alias('receiver'), \
        f.regexp_extract('value', subject_regex, 1).alias('subject'), \
        f.regexp_extract('value', date_regex, 1).alias('receive_date'), \
        f.regexp_extract('value', body_regex, 1).alias('html_body'))\
    .withColumn('id', row_number())\
    .withColumn('body', html_to_plain_udf('html_body'))\
    .withColumn('word_tokens', process_body_udf('body'))\
    .withColumn('current_date', f.current_date())
    
    
    send_to_cassandra.select('current_date', 'id', 'sender', 'label', 'receiver', 'receive_date', 'subject', 'word_tokens')\
    .filter(f.size('word_tokens') != 0)\
    .write.json(output, mode='overwrite')
    #send_to_cassandra.write.format("org.apache.spark.sql.cassandra")\
    #   .options(table = 'email', keyspace = 'email_database').save()


if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('email ETL')\
        .config('spark.cassandra.connection.host', cassandra_host).getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    main(inputs, output)