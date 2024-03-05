from tkinter import *
from tkinter import filedialog
import zipfile
import os
import sys
import glob
import pandas as pd
from unzipUtils import UnzipUtils

THEME_COLOR = "#444953"

class FolderInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("test")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.opened_dir = None
        self.zip_files = None

        self.folder_name_label = Label(text="Select Folder: ", bg=THEME_COLOR, fg="cyan")
        self.folder_name_label.grid(row=0, column=1)

        #Open BUTTON
        self.open_btn_image = PhotoImage(file="images/open1.png")
        self.openDir_btn = Button(bg=THEME_COLOR, image=self.open_btn_image, bd=0, highlightbackground=THEME_COLOR, highlightthickness=0, command=self.openDirectory)
        self.openDir_btn.grid(row=1, column=1)

        #Central canvas
        self.central_canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
        self.central_text = self.central_canvas.create_text(150, 75, width=200, text="", fill="#000000", font=("Arial", 20, "italic"))
        self.central_canvas.grid(row=2, column=0, columnspan=3, pady=50)

        #TO-DO add commands
        #unzip buttons
        self.unzip_btn_image = PhotoImage(file="images/zip1.png")
        self.unzip_btn = Button(image=self.unzip_btn_image, bd=0, highlightthickness=0, bg=THEME_COLOR, command=self.unzipAllBtn)
        self.unzip_btn.grid(row=5, column=1)

        #csv exporter
        self.csv_btn_image = PhotoImage(file="images/csv_button.png")
        self.csv_btn = Button(image=self.csv_btn_image, bd=0, highlightthickness=0, bg=THEME_COLOR, command=self.exportCsv)
        self.csv_btn.grid(row=6, column=1)

        #delete button
        self.delete_btn_image = PhotoImage(file="images/delete_button.png")
        self.delete_btn = Button(image=self.delete_btn_image, bd=0, highlightthickness=0, bg=THEME_COLOR, command=self.deleteZipFiles)
        self.delete_btn.grid(row=7, column=1)


        self.window.mainloop()

    #open dir function
    def openDirectory(self):
        #print("BUTTON working")
        self.opened_dir = filedialog.askdirectory()
        self.zip_files = [file for file in os.listdir(self.opened_dir) if file .endswith(".zip")]
        self.central_canvas.itemconfig(self.central_text, text=f"{len(self.zip_files)} zip files found in: {self.opened_dir}")
     
    def unzipAllBtn(self):
        zip1 = UnzipUtils(self.opened_dir)
        zip1.unzipAll()

    def deleteZipFiles(self):
        for zfile in self.zip_files:
            os.remove(self.opened_dir + "/" + zfile)
            print("Done removing files")

    def exportCsv(self):
        dirpath = self.opened_dir
        fbx_files = []

        for x in os.walk(dirpath):
            for y in glob.glob(os.path.join(x[0], "*.stl")):
                #y = y.replace("\\", "/")
                fbx_files.append(y)
            for z in glob.glob(os.path.join(x[0], "*.obj")):
                #z = z.replace("\\", "/")
                fbx_files.append(z)

        h = {"fbx_files": fbx_files}

        df = pd.DataFrame(h)
        df.to_csv("file_list.csv")

        data = pd.read_csv("file_list.csv")
        print(data)

if __name__ == "__main__":
    ui = FolderInterface()
