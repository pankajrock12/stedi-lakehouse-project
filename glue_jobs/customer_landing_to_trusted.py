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

# Read from Glue Catalog
df = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_landing"
).toDF()

# Filter only customers who agreed to share with research
df_trusted = df.filter(F.col("sharewithresearchasofdate").isNotNull())

# Write to S3 and update catalog
glueContext.write_dynamic_frame.from_options(
    frame=glueContext.create_dynamic_frame.from_df(df_trusted, glueContext, "df_trusted"),
    connection_type="s3",
    connection_options={
        "path": "s3://YOUR_BUCKET/customer_trusted/",
        "partitionKeys": []
    },
    format="json"
)

job.commit()