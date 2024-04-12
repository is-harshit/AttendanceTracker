
import glob
import cv2
import pandas as pd
import pathlib
import sqlite3 as lite
from playsound import playsound
from time import sleep
import os
import tkinter as tk
from tkinter import simpledialog
import datetime

# url = 'https://192.168.1.2:8080/video'

# webcam = cv2.VideoCapture(url)

webcam=cv2.VideoCapture(0)
# resized=cv2.resize("Frame",(600,400))

lis=[]
con=lite.connect("Attend.sqlite")

# date=datetime.datetime.now().strftime("%x")
# date=date.replace("/","-")

# file="Attendence_script_FinTech.xlsx"
# file="Attendence_script_C_Section.xlsx"

# course="Test"

course="FinTech_A_Section"
# course="C_Section"

file="Attendence_script_"+course+".xlsx"
date="11_4_24"
mode=1

#  0:create new; 1:append

# def add_manual(usn):
#     if usn not in lis and usn in uni:
#         con.execute(f"UPDATE Attendence_{date} SET Attendence=1 where USN='{usn}';")
#         con.commit()
#         print(usn, u'\u2714', ' Done')
#         playsound(os.path.dirname(__file__) + "\ping.wav")
#         sleep(1)
#     else:
#         if usn not in uni:
#             print(usn, u'\u274c', " Out of list")
#             playsound(os.path.dirname(__file__) + '\ebeep.wav')
#             sleep(1)
#         else:
#             print(usn, u'\u274c', " Repeated")
#             playsound(os.path.dirname(__file__) + '\error.wav')

root = tk.Tk()
root.withdraw()

# add_manual("1RVU22CSE047")

if mode==0:
  with lite.connect("Attend.sqlite") as con:
    # con.execute(f"Create table Attendence{data} (USN text, Attendance int)")
    df=pd.read_excel(file)

    uni=list(df['USN'])
    print(uni)
    df.to_sql(f"Attendence_{course}_{date}",con,if_exists='replace',index=False)


if mode==1:
  with lite.connect("Attend.sqlite") as con:
      try:
          df = pd.read_sql(f"Select * from Attendence_{course}_{date}", con)

      except:
          df = pd.read_excel(file)
          df.to_sql(f"Attendence_{course}_{date}", con, if_exists='replace', index=False)

      uni = list(df['USN'])
      liss=pd.read_sql(f"Select USN from Attendence_{course}_{date} where attendence=1",con)

      lis=list(liss['USN'])
print("Attendence Marked for:",lis)

def read_qr_code(filename,mode):
     detect = cv2.QRCodeDetector()
     if mode==0:
       try:
          img = cv2.imread(filename)
          # print("\n\n\n\n\n\n\n\n\======\n\n\n\n",img)
          value, points, straight_qrcode = detect.detectAndDecode(img)
          return value
       except:
          return
     elif mode==1:
         try:
             value, points, straight_qrcode = detect.detectAndDecode(filename)
             return value
         except:
             return

def attend(ini_list,backup_list):
    while True:
        ret,frame=webcam.read()
        if ret==True:
           cv2.imshow("Attendence",frame)
        # print(frame)
           usn=(read_qr_code(frame,1))
           if len(usn)!=0 and (usn in ini_list) :
            print(usn)
            backup_list.append(usn)
           key=cv2.waitKey(1)
           if key==ord('q'):
              break
              return backup_list


def mark(usn):
    if usn not in lis and usn in uni:
        lis.append(usn)
        with lite.connect("Attend.sqlite") as con:
           con.execute(f"UPDATE Attendence_{course}_{date} set Attendence=1 where usn='{usn}'")
           con.commit()
        print(usn,u'\u2714',' Done')
        playsound(os.path.dirname(__file__)+"\ping.wav")
        sleep(1)
    else:
        if usn not in uni:
            print(usn,u'\u274c'," Out of list")
            playsound(os.path.dirname(__file__)+'\ebeep.wav')
            sleep(1)
        else:
            print(usn, u'\u274c', " Repeated")
            playsound(os.path.dirname(__file__) + '\error.wav')


while True:
    ret,frame=webcam.read()
    if ret==True:
        cv2.imshow("Attendence",frame)
        # print(frame)
        usn=(read_qr_code(frame,1))
        try:
            if len(usn)!=0:
            # print(len(usn))
            # print(usn)
              mark(usn)
        except TypeError:
            continue

        key=cv2.waitKey(1)
        if key==ord('q'):
            break
        elif key==ord('m'):
            print("Enter USN!")
            # mann=input()
            mann= simpledialog.askstring(title="Attendence",
                                  prompt="Ente the USN:")
            mark(mann)

print("Attendence Marked for:",lis)
df=pd.read_sql(f"Select * from Attendence_{course}_{date}",con)
df.to_csv(f"Attendence_{course}_{date}.csv")
df.to_excel(f"Attendence_{course}_{date}.xlsx")

con.close()
# file="Attendence-Test.xlsx"
# date='28-08-2004'
# final=[]
#
# #%%
# df=pd.read_excel(file)
# df.dropna(inplace=True)
#
# stu=list(df['USN'])
#
# final=attend(stu,final)
# backup.append(final)
#
# df[date]=backup
#
# df.to_sql("test",con,if_exists='replace')
# con.close()

# print(read_qr_code("test2.jpg",0))

