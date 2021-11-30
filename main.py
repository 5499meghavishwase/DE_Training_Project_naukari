
###Refined code after handling some time changes
import csv
#from flask import Flask
import time
import datetime
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
#import chromedriver_binary
from google.cloud import storage
#app = Flask(__name__)
#chrome_options= webdriver.ChromeOptions
#chrome_options.add_argument("--incognito")
chrome_options = webdriver.ChromeOptions()
"""chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")"""
path="C:\\Users\\Shubham Yadav\\dataEngineering\\chromedriver.exe"
driver=webdriver.Chrome(executable_path=path, options=chrome_options)
#driver=webdriver.Chrome(ChromeDriverManager.install)
#driver.implicitly_wait(5)
#@app.route("/")

def task_scrape() : 
    jobs={"roles":[],
        "companies":[],
        "locations":[],
        "experience":[],
        "skills":[],
        "jd_url":[]
        }
    #This outer loop is for number of pages to be scraped
    for i in range(1,11):
        driver.get("https://www.naukri.com/data-engineering-jobs-{}".format(i))
        time.sleep(3)
        job_container = driver.find_elements(By.CSS_SELECTOR,".jobTuple.bgWhite.br4.mb-8")
        # scraping the details from webpage
        for job in job_container:
            driver.implicitly_wait(11)
            role=job.find_element(By.CSS_SELECTOR,"a.title.fw500.ellipsis").text
            company=job.find_element(By.CSS_SELECTOR,"a.subTitle.ellipsis.fleft").text
            location=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.location").text
            exp=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.experience").text
            skills=job.find_element(By.CSS_SELECTOR,".tags.has-description").text
            jd=driver.find_element(By.TAG_NAME,"a").get_attribute("href")
            #category=job.find_element(By.CSS_SELECTOR,"jobType type fleft br2 mr-8")
            jobs["roles"].append(role)
            jobs["companies"].append(company)
            jobs["locations"].append(location)
            jobs["experience"].append(exp)
            jobs["skills"].append(skills)
            jobs["jd_url"].append(jd)
    driver.close
    #creating CSV file by appending rows        
    df=pd.DataFrame.from_dict(jobs) #Creating DataFrame
    df.head(10)
    df=df.apply(lambda x: x.astype(str).str.lower()) #converting into lowercase to remove redundancy
    df.head()    
    df.skills=[skill.split("\n") for skill in df.skills]
    df.locations=[location.split(" ") for location in df.locations]
    #df[15:25]
    df.info()
    df.isnull().sum()
    df=df.dropna()
    return df.to_csv()


#Method to upload csv file to Bucket
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    #bucket_name = "jobfilecsv"
    # The path to your file to upload
    #source_file_name = "devopsjob.csv"
    # The ID of your GCS object
    #destination_blob_name = "devopsjob.csv"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    x=datetime.datetime.now().replace(microsecond=0)

    print(
        "File {} uploaded to {} at {}.".format(
            source_file_name,destination_blob_name,str(x)
        )
    )

try:
    job_csv=task_scrape()
    upload_blob("jobfilecsv",job_csv,"data_engineer_job.csv")
except Exception as e:
    t=datetime.datetime.now().replace(microsecond=0)
    print(str(t))
    print(e)

    

