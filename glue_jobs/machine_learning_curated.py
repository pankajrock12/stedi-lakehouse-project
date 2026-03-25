import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

acc = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_trusted"
).toDF()

step = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="step_trainer_trusted"
).toDF()

# Join on timestamp
df_ml = acc.join(step, acc["timestamp"] == step["sensorreadingtime"], "inner")

glueContext.write_dynamic_frame.from_options(
    frame=glueContext.create_dynamic_frame.from_df(df_ml, glueContext, "df_ml"),
    connection_type="s3",
    connection_options={
        "path": "s3://YOUR_BUCKET/machine_learning_curated/",
        "partitionKeys": []
    },
    format="json"
)

job.commit()