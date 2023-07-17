#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 17:49:48 2023

@author: jawad
"""

import tkinter as tk
import cv2
from datetime import date
from PIL import Image, ImageTk
import numpy as np
import face_recognition
import os
from datetime import datetime

root = tk.Tk()
root.geometry("600x700")
root.configure(background="#222222")


def update_title():
    current_date = date.today()
    root.title(str(current_date))


update_title()


frame = tk.Frame(root, bg="white")
frame.configure(background="#333333")
frame.pack(fill="both", expand=False)


welcome_label = tk.Label(frame, text="AI-based Face recognition attendance system", width=50, height=2)
welcome_label.configure(highlightbackground="red")
welcome_label.pack(pady=20)


image_path = "logo.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

label = tk.Label(frame, image=photo)
label.pack(pady=10)

# 3


instructions_label = tk.Label(
    root, text="Please select an option:", font=("Latha", 12), width=50, height=2)
instructions_label.pack(pady=10)


def capture_video():
    new_window = tk.Toplevel(root)
    new_window.geometry("700x800")
    new_window.configure(background="#222222")

    label = tk.Label(
        new_window, text="Stand still infront of the Camera", width=40, height=2)
    label.pack(pady=10)

    # label1 =tk.Label(new_window)
    # label1.pack()

    def press():

        ########################################################
        #                                                      #

        path = 'Training_images'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodings(images):
            with open("Attendance.csv", 'r+') as file:
                current_date = date.today()
                file.write(str(current_date))
                file.close()

            encodeList = []

            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                try:
                    encode = face_recognition.face_encodings(img)[0]
                    encodeList.append(encode)
                except IndexError as e:
                    print(f"Error encoding image: {e}")

            return encodeList

        def markAttendance(name):
            with open('Attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
        
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:    
                    f.writelines(f'\n{name},Present')

        encodeListKnown = findEncodings(images)
        print('Encoding Complete')

        ###########################################################
        cap = cv2.VideoCapture(1)

        def show_frames():
            success, img = cap.read()
            if not success:
                print("Failed to read from webcam.")
                

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

            
            img = Image.fromarray(img)

            imgtk = ImageTk.PhotoImage(image = img)
            label1.imgtk = imgtk
            label1.configure(image=imgtk)
            # Repeat after an interval to capture continiously
            label1.after(20, show_frames)

        show_frames()
        
        
        ##############################################
        def close_webcam():
            cap.release()
            new_window.destroy()

   
        close_button = tk.Button(new_window, text="Close Webcam", command=close_webcam, background="#6D6D6D", foreground="#FFFFFF")
        close_button.pack(pady=10)
        ##########################################################
  
    press_button = tk.Button(new_window, text="Capture Video", command=press, background="#6D6D6D", foreground="#FFFFFF")
    press_button.pack(pady=10)
    
    label1 =tk.Label(new_window)
    label1.pack()

    
capture_button = tk.Button(root, text="Capture Video", command=capture_video, background="#6D6D6D", foreground="#FFFFFF")
capture_button.pack(pady=10)

def open_excel_file():
    new_window = tk.Toplevel(root)  
    new_window.title("New Window")
    new_window.geometry("500x500")

   
    label = tk.Label(new_window, text="This is a new window!")
    label.pack()

open_file_button = tk.Button(root, text="Open Excel File", command=open_excel_file, background="#6D6D6D", foreground="#FFFFFF")
open_file_button.pack(pady=10)

def mark_attendance_manually():
    new_window = tk.Toplevel(root)  
    new_window.title("New Window")
    new_window.geometry("500x500")

   
    label = tk.Label(new_window, text="This is a new window!")
    label.pack()

mark_attendance_button = tk.Button(root, text="Mark Attendance Manually", command=mark_attendance_manually, background="#6D6D6D", foreground="#FFFFFF")
mark_attendance_button.pack(pady=10)


def Add_new_student():
    new_window = tk.Toplevel(root)  
    new_window.title("New Window")
    new_window.geometry("500x500")

   
    label = tk.Label(new_window, text="This is a new window!")
    label.pack()
    
new_student_button = tk.Button(root, text="Add New student", command=mark_attendance_manually, background="#6D6D6D", foreground="#FFFFFF")
new_student_button.pack(pady=10)



root.mainloop()








