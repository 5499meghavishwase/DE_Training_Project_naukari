import os

from google.cloud import bigquery, client
import datetime
# Construct a BigQuery client object.
#client = bigquery.Client()
#from myfolder.csv_to_bq import uri
#from google.rpc import context
from myfolder.sending_mail import send_email

def csv_loader(event):
    client = bigquery.Client.from_service_account_json("C:\\Users\\prateek\\Downloads\\de-training-project-3fb8c9f7d834.json")

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("serial_no", "INTEGER"),
        bigquery.SchemaField("roles", "STRING"),
        bigquery.SchemaField("companies", "STRING"),
        bigquery.SchemaField("locations", "STRING"),
        bigquery.SchemaField("experience", "STRING"),
        bigquery.SchemaField("skills", "STRING"),
    ],
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
)
# get this from event
    #uri = "gs://training-demo-project/naukri2.csv"
    #uri =os.path.join("gs://",event['bucket'], event["name"])
    uri="gs://"+event['bucket']+"/"+event['name']
    print(uri)
    #uri="gs://training-demo-project/JavaDeveloperjobs.csv"
#hello_gcs("gs://training-demo-project/naukri2.csv")

# static load it from later
    try:
        table_id="de-training-project.jobs_info_naukri.jobs"

        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)  # Make an API request.


#mport dat time and str(datetime.now())

        load_job.result()  # Waits for the job to complete.
        destination_table = client.get_table(table_id)  # Make an API request.
        print("Loaded {} rows.".format(destination_table.num_rows))
        x=datetime.datetime.now().replace(microsecond=0)
        #print(x+"Ptr")
        #send_email(["sarojprateekkumar@gmail.com","megha.vishwase@mediaagility.com ","mayuresh.bharmoria@mediaagility.com"],'successfull loaded the file '+str(uri)+' to bigquery')
        sub = 'successfully loaded the file ' + str(uri) + ' to bigquery at ' + str(x)
        send_email(
       ["sarojprateekkumar@gmail.com","megha.vishwase@mediaagility.com ","shubham.yadav@mediaagility.com "
           ,"mayuresh.bharmoria@mediaagility.com","monika.dubey@mediaagility.com "],sub)
    except Exception as e:
        print(e)
    #send_email(["sarojprateekkumar@gmail.com","megha.vishwase@mediaagility.com ","mayuresh.bharmoria@mediaagility.com"],'')
        x=datetime.datetime.now().replace(microsecond=0)
        sub='File ' +str(uri) +'is not loaded successfully to bigquery at'+ str(x)
        send_email(
        ["sarojprateekkumar@gmail.com","megha.vishwase@mediaagility.com ","shubham.yadav@mediaagility.com "
           ,"mayuresh.bharmoria@mediaagility.com","monika.dubey@mediaagility.com "], sub)
        print('Error Occured while loading data')

event={'bucket': 'training-demo-project', 'contentType': 'application/vnd.ms-excel', 'crc32c': '6zFgOA==',
        'etag': 'COKM74nHrvQCEAE=', 'generation': '1637672929707618',
        'id': 'training-demo-project/JavaDeveloperjobs.csv/1637672929707618', 'kind': 'storage#object',
        'md5Hash': '7Phk3bod2e0qGECGi+2QRA==',
        'mediaLink': 'https://www.googleapis.com/download/storage/v1/b/training-demo-project/o/JavaDeveloperjobs.csv?generation=1637672929707618&alt=media',
        'metageneration': '1', 'name': 'JavaDeveloperjobs.csv',
        'selfLink': 'https://www.googleapis.com/storage/v1/b/training-demo-project/o/JavaDeveloperjobs.csv', 'size': '28922',
        'storageClass': 'STANDARD', 'timeCreated': '2021-11-23T13:08:49.859Z',
        'timeStorageClassUpdated': '2021-11-23T13:08:49.859Z', 'updated': '2021-11-23T13:08:49.859Z'}

csv_loader(event)
