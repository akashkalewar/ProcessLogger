import os
import time
import psutil
import urllib.request
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

#To check whether connection is established or not
def is_connected():
    try:
        urllib.request.urlopen('http://216.58.192.142',timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

#For Sending Mail
def MailSender(filename,time):
    try:
        fromaddr = "abc@gmail.com" #senders mail id
        toaddr = "xyz@gmail.com" #recievers mail id

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        body = """
        Hello %s, 
        Please find attached document which contains Log of Running Process
        Log file is created at: %s
        
        This is auto generated mail.
        
        Thanks & Regards,
        Your_Name
            """%(toaddr,time)
            
        
        Subject = """Log Generated at: %s"""%(time)
        
        msg['Subject']=Subject
        msg.attach(MIMEText(body,'plain'))
        attachment = open(filename,"rb")
        p = MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition',"attachment;filename=%s"%filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(fromaddr,"**************")#Put the Password
        text = msg.as_string()
        s.sendmail(fromaddr,toaddr,text)
        s.quit()

        print("Log file successfully sent through mail")
    except Exception as E:
        print("Unable to send mail ",E)

def ProcessLog(log_dir='Logger'):
    listprocess=[]

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    seperator="-" * 80
    log_path = os.path.join(log_dir,'LogFile.log')
    f = open(log_path,'w')
    f.write(seperator+"\n")
    f.write("Process Logger: "+time.ctime()+"\n")
    f.write(seperator + "\n")
    f.write("\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid','name','username'])
            vms = proc.memory_info().vms/(1024*1024)
            pinfo['vms'] = vms
            listprocess.append(pinfo)
        except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

        for element in listprocess:
            f.write("%s\n"%element)

        print("Log File Successfully Generated at location %s"%(log_path))

        connected = is_connected()

        if connected:
              startTime = time.time()
              MailSender(log_path,time.ctime())
              endTime = time.time()

              print("Took %s seconds to send mail" %(endTime-startTime))
        else:
              print("There is no internet connection")


def main():
    print("----Process Logger----")
    print("Application Name: "+argv[0])
    if(len(argv)>3):
        print("Error: Invalid Number of Arguments")
        exit()
    
    #Help
    if(argv[1] == '-h') or (argv[1] == '-H'):
        print("The Script is used to log record of running processess and mail it")
        exit()

    # Usage
    if (argv[1] == '-u') or (argv[1] == '-U'):
        print("Usage: Filename Time_Interval DirName")
        print("Filename: Script File")    
        print("Time_Interval: Script to be executed after how many minutes")
        print("DirName: Name of directory")
        exit()
    
    try:
          schedule.every(int(argv[1])).minutes.do(ProcessLog(argv[2]))
          while True:
              schedule.run_pending()
              time.sleep(1)
    except ValueError:
        print("Error: Invalid Datatype of input")

    except Exception as E:
        print("Error:Invalid input",E)


                  
if __name__ == "__main__":
    main()
              
               
