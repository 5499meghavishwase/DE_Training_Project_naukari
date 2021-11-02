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
driver.get("https://www.naukri.com/data-scientist-jobs")
time.sleep(3)
lst=driver.find_elements_by_css_selector(".jobTuple.bgWhite.br4.mb-8") 
# scrape the data from website
for job in lst:
    driver.implicitly_wait(10)
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
 
df=pd.DataFrame.from_dict(jobs)
df.head(10)
df=df.apply(lambda x: x.astype(str).str.lower())
df.head()    
df.skills=[skill.split("\n") for skill in df.skills]
df.locations=[location.split(",") for location in df.locations]
df[15:25]
df.info()
df.isnull().sum()
df=df.dropna()
df.to_csv('naukri.csv')