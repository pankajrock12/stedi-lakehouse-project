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

cust = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_trusted"
).toDF()

acc = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_trusted"
).toDF()

# Keep only customers who have accelerometer data
df_curated = cust.join(acc, cust["email"] == acc["user"], "inner").select(cust["*"]).dropDuplicates()

glueContext.write_dynamic_frame.from_options(
    frame=glueContext.create_dynamic_frame.from_df(df_curated, glueContext, "df_curated"),
    connection_type="s3",
    connection_options={
        "path": "s3://YOUR_BUCKET/customer_curated/",
        "partitionKeys": []
    },
    format="json"
)

job.commit()