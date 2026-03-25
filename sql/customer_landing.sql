CREATE EXTERNAL TABLE IF NOT EXISTS customer_landing (
    serialnumber STRING,
    sharewithpublicasofdate STRING,
    birthday STRING,
    registrationdate STRING,
    sharewithresearchasofdate STRING,
    customername STRING,
    email STRING,
    lastupdatedate STRING,
    phone STRING,
    sharewithfriendsasofdate STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://YOUR_BUCKET/customer_landing/';