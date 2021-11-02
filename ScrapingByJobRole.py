
###Refined code after handling some time changes
import csv
import time
from selenium import webdriver
import pandas as pd

driver=webdriver.Chrome()
jobs={"roles":[],
     "companies":[],
     "locations":[],
     "experience":[],
     "skills":[]
     }
#This outer loop is for number of pages to be scraped
for i in range(1,10):
    driver.get("https://www.naukri.com/data-scientist-jobs-{}".format(i))
    time.sleep(3)
    lst=driver.find_elements_by_css_selector(".jobTuple.bgWhite.br4.mb-8")
    
    # scraping the details from webpage
    for job in lst:
        driver.implicitly_wait(20)
        role=job.find_element_by_css_selector("a.title.fw500.ellipsis").text
        company=job.find_element_by_css_selector("a.subTitle.ellipsis.fleft").text
        location=job.find_element_by_css_selector(".fleft.grey-text.br2.placeHolderLi.location").text
        exp=job.find_element_by_css_selector(".fleft.grey-text.br2.placeHolderLi.experience").text
        skills=job.find_element_by_css_selector(".tags.has-description").text
        jobs["roles"].append(role)
        jobs["companies"].append(company)
        jobs["locations"].append(location)
        jobs["experience"].append(exp)
        jobs["skills"].append(skills)
        print(jobs)
df=pd.DataFrame.from_dict(jobs) #Creating DataFrame
df.head(10)
df=df.apply(lambda x: x.astype(str).str.lower()) #converting into lowercase to remove redundancy
df.head()    
df.skills=[skill.split("\n") for skill in df.skills]
df.locations=[location.split(",") for location in df.locations]
df[15:25]
df.info()
df.isnull().sum()
df=df.dropna()
df.to_csv('naukri.csv')