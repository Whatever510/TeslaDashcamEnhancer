import os
import time
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import cv2
import numpy as np
from PIL import Image
from pillow_lut import load_cube_file


class App:
    def __init__(self, root):
        #setting title
        self.root = root
        self.root.title("Tesla Dashcam Enhancer")
        #setting window size
        width=250
        height=720
        self.filenameOpen = ""
        self.filenameClose = ""
        self.interval = 300
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)


        #Get all the available filters
        self.filter_list = os.listdir("cube_files")

        #Create GUI Elements
        self.GButton_select_vid=tk.Button(self.root)
        self.GButton_select_vid["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_select_vid["font"] = ft
        self.GButton_select_vid["fg"] = "#000000"
        self.GButton_select_vid["justify"] = "center"
        self.GButton_select_vid["text"] = "Select Video"
        self.GButton_select_vid.place(x=75,y=30,width=125,height=45)
        self.GButton_select_vid["command"] = self.GButton_select_vid_command

        self.GButton_select_save=tk.Button(self.root)
        self.GButton_select_save["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_select_save["font"] = ft
        self.GButton_select_save["fg"] = "#000000"
        self.GButton_select_save["justify"] = "center"
        self.GButton_select_save["text"] = "Select Save Location"
        self.GButton_select_save.place(x=75,y=130,width=125,height=45)
        self.GButton_select_save["command"] = self.GButton_select_save_command

        self.GListBox_select_filter = tk.Listbox(self.root)
        self.GListBox_select_filter["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GListBox_select_filter["font"] = ft
        self.GListBox_select_filter["fg"] = "#333333"
        self.GListBox_select_filter["justify"] = "center"
        height_box = min(5,len(self.filter_list))
        self.GListBox_select_filter.place(x=75,y=235,width=125,height=17*height_box)
        for item in self.filter_list:
            self.GListBox_select_filter.insert("end",item)
        self.GListBox_select_filter["selectmode"] = "browse"

        self.GButton_preview=tk.Button(self.root)
        self.GButton_preview["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_preview["font"] = ft
        self.GButton_preview["fg"] = "#000000"
        self.GButton_preview["justify"] = "center"
        self.GButton_preview["text"] = "Preview"
        self.GButton_preview.place(x=75,y=450,width=125,height=45)
        self.GButton_preview["command"] = self.GButton_preview_command

        self.Label_time = tk.Label(self.root)
        self.Label_time["text"] = "Set preview duration \ndefault 10s"
        self.Label_time.place(x=75, y=350, width=125, height=45)

        self.GEntry_time = tk.Entry(self.root)
        self.GEntry_time["bg"] = "#FFFFFF"
        self.GEntry_time.insert(0,str(10))
        self.GEntry_time.place(x=75, y=400, width=125, height=45)

        self.GButton_start_enhancement=tk.Button(self.root)
        self.GButton_start_enhancement["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_start_enhancement["font"] = ft
        self.GButton_start_enhancement["fg"] = "#000000"
        self.GButton_start_enhancement["justify"] = "center"
        self.GButton_start_enhancement["text"] = "Enhance"
        self.GButton_start_enhancement.place(x=75,y=530,width=125,height=45)
        self.GButton_start_enhancement["command"] = self.GButton_start_enhancement_command

        self.GProgressbar = ttk.Progressbar(root)
        self.GProgressbar["orient"] = HORIZONTAL
        self.GProgressbar["length"] = 100
        self.GProgressbar["mode"] = 'determinate'
        self.GProgressbar.place(x=75,y=600,width=125,height=45)

        self.GButton_exit=tk.Button(self.root)
        self.GButton_exit["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_exit["font"] = ft
        self.GButton_exit["fg"] = "#000000"
        self.GButton_exit["justify"] = "center"
        self.GButton_exit["text"] = "Exit"
        self.GButton_exit.place(x=75,y=650,width=125,height=45)
        self.GButton_exit["command"] = exit
        self.frame_no = 0



    def GButton_select_vid_command(self):
        """ Select the videofile to be opened """
        self.filenameOpen = filedialog.askopenfilename(initialdir="/",
                                                       title="Bitte Videodatei auswählen",
                                                       filetypes=(("Videodatein", "*.mp4"), ("alle Datein", "*.*")))



    def GButton_select_save_command(self):
        """ Select the location where the new videofile should be saved """
        files = [('Videodatei', '*.mp4'), ('All Files', '*.*')]

        self.filenameClose = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
        print(self.filenameClose)


    def checkPrecondistions(self,selection,vidIn,vidOut,preview = False):
        """ Checks if a cube file and a video is selected
        If not in preview mode check if a save location was specified """
        if preview:
            if len(selection)==0:
                raise FileNotFoundError ("No Filter selected")
            if vidIn == "" or not os.path.exists(vidIn):
                raise FileNotFoundError ("No Videofile selected or file does not exists")
        else:
            if len(selection)==0:
                raise FileNotFoundError ("No Filter selected")
            if vidIn == "" or not os.path.exists(vidIn):
                raise FileNotFoundError ("No Videofile selected or file does not exists")
            if vidOut == "":
                raise FileNotFoundError ("No Save Location selected")


    def GButton_preview_command(self):
        """ Starts the preview of the selected filter side by side with the original """
        selection = []
        self.frame_no = 0
        for i in self.GListBox_select_filter.curselection():

            index = int(i)  # i ist ein String

            selection.append(self.filter_list[index])

        self.checkPrecondistions(selection,self.filenameOpen,self.filenameClose,True)

        cube = load_cube_file("cube_files/"+selection[0])

        cap = cv2.VideoCapture(self.filenameOpen)

        ret,frame = cap.read()
        h,w,_ = frame.shape
        h = 3*h//4
        w=3*w//4
        max_duration = self.GEntry_time.get()
        if max_duration.isdecimal():
            max_duration = int(max_duration)
        else:
            raise ValueError("Time must be an Integer Value")
        start = time.time()

        while(ret):
            frame = cv2.resize(frame,(w,h))
            pil_frame = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            trans_frame = pil_frame.filter(cube)
            trans_frame = cv2.cvtColor(np.asarray(trans_frame), cv2.COLOR_RGB2BGR)
            result = frame.copy()
            result[:,w//2:] = trans_frame[:,w//2:]
            cv2.putText(result,"TeslaCam",(50,30),fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,color = (0,255,0),thickness=1)
            cv2.putText(result, "Enhanced Version", (w//2+50, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0),
                        thickness=1)
            cv2.imshow("PREVIEW",result)
            cv2.waitKey(30)
            ret,frame = cap.read()
            end = time.time()
            if end - start >= max_duration:
                break
        cv2.destroyAllWindows()



    def GButton_start_enhancement_command(self):
        """ Starts the enhancement of the video by applying the selected LUT """
        selection = []

        for i in self.GListBox_select_filter.curselection():
            index = int(i)  # i ist ein String

            selection.append(self.filter_list[index])


        self.checkPrecondistions(selection,self.filenameOpen,self.filenameClose)

        cube = load_cube_file("cube_files/" + selection[0])

        cap = cv2.VideoCapture(self.filenameOpen)

        ret, frame = cap.read()
        h, w, _ = frame.shape
        fps = cap.get(cv2.CAP_PROP_FPS)

        max_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        counter = 0
        out = cv2.VideoWriter(self.filenameClose, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

        while (ret):
            frame = cv2.resize(frame, (w, h))
            pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            trans_frame = pil_frame.filter(cube)
            trans_frame = cv2.cvtColor(np.asarray(trans_frame), cv2.COLOR_RGB2BGR)
            self.GProgressbar["value"] = int((counter/max_frames)*100)
            self.GProgressbar.update()
            #print(int((counter/max_frames)*100))
            counter += 1
            out.write(trans_frame)

            ret, frame = cap.read()

        self.GProgressbar["value"] = 100
        self.GProgressbar.update()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()