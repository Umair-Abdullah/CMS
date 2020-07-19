import cv2
import os
from tkinter import *

label = "Default"
#Name Dialouge Gui
gui = Tk()

def center_window(w=300, h=200):
    # get screen width and height
    ws = gui.winfo_screenwidth()
    hs = gui.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    gui.geometry('%dx%d+%d+%d' % (w, h, x, y))

gui.title("Enter Name")
center_window(240,80)

L = Label(gui, text="Enter Name")
L.grid(column=5, row=0)

name = StringVar()
nameEntered = Entry(gui, width=40, textvariable=name)
nameEntered.grid(column=5, row=1)
nameEntered.focus()

def done_clicked():
    global label
    label = name.get()
    if label == "": label = "Default"
    gui.destroy()


B = Button(gui, text="Done", command=done_clicked)
B.grid(column=5, row=2)
gui.mainloop()

label1=os.path.join(os.getcwd(), "images", "train")
label2=os.path.join(os.getcwd(), "images", "test")

#train test directory
try:
    os.mkdir(label1)
    os.mkdir(label2)
except:
    print("")

label_test=os.path.join(label2, label)
label=os.path.join(label1, label)


# creating folder for data of person
try:
    os.mkdir(label)
    os.mkdir(label_test)
except:
    print(" ")

print(label,"   ",label_test)
#End of name dialog



# face Detection
face_cascade = cv2.CascadeClassifier(cv2.haarcascades + 'haarcascade_frontalface_default.xml')

# Capturing video from camera
r=0
def test(val):
    global r
    r=val
    print(val)

cap = cv2.VideoCapture(0)
# GUI
save = 0
pic=""
while True:
    # reading frame from captured video
    ret, frame = cap.read()

    # convert to grayscale
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detection of Faces
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)

    # draw box on faces
    for (x, y, w, h) in faces:
        crop_face = frame[y:y + h, x:x + w]
        #crop_face = cv2.blur(crop_face,(2,2))
        crop_face=cv2.resize(crop_face, (256,256), interpolation=cv2.INTER_AREA)
        save = save + 1
        if save <= 200:
            pic=os.path.join(label, "face"+str(save)+".jpg")
            print(pic)
            cv2.imwrite(pic, crop_face)
        if save>200 and save<=300:
            pic = os.path.join(label_test, "face" + str(save) + ".jpg")
            print(pic)
            cv2.imwrite(pic, crop_face)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 155, 55), 2)


    # Show inside a window
    cv2.imshow('Camera', frame)
    #cv2.createTrackbar("Pictures", "Camera", r, 255, test)


    # End when Enter is Pressed
    if cv2.waitKey(1) == 13: break
cap.release()
cv2.destroyAllWindows()
