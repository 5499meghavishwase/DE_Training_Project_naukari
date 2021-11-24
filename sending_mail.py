import smtplib
from datetime import datetime
from email.message import EmailMessage

from datetime import datetime


def send_email(to,subject):
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']='Prateek'
    msg['To']=to
   # msg['Subj']=sub
    #msg['Time']=time
    #print(msg['Time'])

    #msg.set_content("Test Email from Prateek")

    with open('intro.txt')as myfile:
        data =myfile.read()
        msg.set_content(data)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server=smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.login("krpatrick2017@gmail.com","Ansh@2010")
            server.send_message(msg)
            #server.send_message()
        #print("Email Send Successfully")
    except Exception as e:
        print(e)
        print('Error Occurred')
"""
x=datetime.now()
y=str(x)
print(y,'hello')

send_email('sarojchhotu2020@gmail.com','alert',y)
"""




