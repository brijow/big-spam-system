import sys
from pyspark.sql import SparkSession, functions as f
from pyspark.ml import Pipeline
from pyspark.ml.feature import HashingTF
from pyspark.ml.classification import LinearSVC
from pyspark.ml.evaluation import BinaryClassificationEvaluator
cassandra_host = 'localhost'


def main(model_name):
    raw = spark.read.format("org.apache.spark.sql.cassandra") \
		.options(table="emails", keyspace="email_database").load()
    #raw = spark.read.json("DontCommit/MLsamples")
    hashingtransformer = HashingTF(inputCol='word_tokens', outputCol='features')
    hashingtransformer.setNumFeatures(5000)
    svc = LinearSVC(featuresCol='features', labelCol='label', predictionCol='prediction')
    svc_pipeline = Pipeline(stages=[hashingtransformer, svc])
    evaluator = BinaryClassificationEvaluator(labelCol='label', rawPredictionCol='rawPrediction', metricName='areaUnderROC')
    
    train, validation = raw.randomSplit([0.75, 0.25])
    train = train.cache()
    validation = validation.cache()
    svc_model = svc_pipeline.fit(train)
    svc_model.write().overwrite().save(model_name)
    prediction = svc_model.transform(validation)
    accuracy = evaluator.evaluate(prediction)
    print('Validation score: %g' % (accuracy, ))


if __name__ == '__main__':
    model_name = sys.argv[1]
    spark = SparkSession.builder.appName('emailml')\
        .config('spark.cassandra.connection.host', cassandra_host).getOrCreate()
    spark.sparkContext.setLogLevel('warn')
    main(model_name)
