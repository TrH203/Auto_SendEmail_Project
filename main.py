import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
from chuyen_hoa_noi_dung import noidung



def import_value(source) -> int:
    try:
        file = open(source, "r")
        savepoint = file.read()
        savepoint =int(savepoint)
        print(savepoint)
        file.close()
    except FileNotFoundError:
        savepoint = 1000
    return savepoint

def update_value(source, value):
    file = open(source, "w")
    file.write(str(value))
    file.close()


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="dbtestaisolfast"
)


sp = import_value(r"D:/Team Dev\2-HienWorkSpace/savepoint.txt")


 
cursor = connection.cursor()


cursor.execute("SELECT id,name,email FROM users Where id > %s", sp)
    
new_users = cursor.fetchall()
print(new_users)
try:
    update_value(r"D:/Team Dev\2-HienWorkSpace/savepoint.txt", new_users[-1][0])
except:
    pass
    

if new_users:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("sp.aisolfast@gmail.com", "mật khẩu ứng dụng")
    for user in new_users:
        email = user[2] 
        html = noidung.replace("%%", user[1])
        message = MIMEMultipart('html')
        message['From'] = "sp.aisolfast@gmail.com"
        message['To'] = email
        message['Subject'] = "Chào mừng bạn đến với AIsolfast"
        message.attach(MIMEText(html, 'html', 'utf-8'))
        server.sendmail("sp.aisolfast@gmail.com", email, message.as_string())
    server.quit()

connection.close()