import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Chrome()
job_roles=["Data Scientist","Data Engineer","Devops","Cloud Engineer","Java Developer","Node JS Developer"]
jobs={"roles":[],
     "companies":[],
     "locations":[],
     "experience":[],
     "skills":[]
     }
#React Developer","PHP Developer","Angular Developer","Android Developer","IOS Developer"
#locatn=driver.find_element(By.NAME,"location")

#Opening Naukri.com for each job role
for role in range(len(job_roles)):             
    driver.get("http://www.naukri.com")
    #driver.implicitly_wait(5)
    designation=driver.find_element(By.NAME,"keyword")
    designation.clear()
    designation.send_keys(job_roles[role])
    driver.find_element(By.CLASS_NAME,"search-btn").click()
    #driver.implicitly_wait(10)
    time.sleep(3)
    job_container = driver.find_elements(By.CSS_SELECTOR,".jobTuple.bgWhite.br4.mb-8")

    #Scraping Of Data
    for page in range(2):
        for job in job_container:                       
            driver.implicitly_wait(20)
            role=job.find_element(By.CSS_SELECTOR,"a.title.fw500.ellipsis").text
            company=job.find_element(By.CSS_SELECTOR,"a.subTitle.ellipsis.fleft").text
            location=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.location").text
            exp=job.find_element(By.CSS_SELECTOR,".fleft.grey-text.br2.placeHolderLi.experience").text
            skills=job.find_element(By.CSS_SELECTOR,".tags.has-description").text
            #category=job.find_element(By.CSS_SELECTOR,"jobType type fleft br2 mr-8")
            jobs["roles"].append(role)
            jobs["companies"].append(company)
            jobs["locations"].append(location)
            jobs["experience"].append(exp)
            jobs["skills"].append(skills)
            #time.sleep(5)
        #element = WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fright.fs14.btn-secondary.br2")))
        next_page=driver.find_element(By.CSS_SELECTOR,"a.fright.fs14.btn-secondary.br2")
        print(next_page)
        next_page.click()
        time.sleep(5)
        #driver.implicitly_wait(10)
        
        #driver.find_element(By.XPATH,'//*[@id="_qmutud2pkNavbar"]/div').click() 
        #driver.find_element(By.CSS_SELECTOR,"a.fright.fs14.btn-secondary.br2")

#Creating DataFrame        
df=pd.DataFrame.from_dict(jobs) 
df.head(10)
df=df.apply(lambda x: x.astype(str).str.lower())  #converting into lowercase to remove redundancy
df.head()    
df.skills=[skill.split("\n") for skill in df.skills]
df.locations=[location.split(",") for location in df.locations]
df.info()
df.isnull().sum()
df=df.dropna()
df.to_csv('naukri.csv')     