from tkinter import *
from tkinter import filedialog, messagebox
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request 

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.folder_path = os.environ["HOMEPATH"]+"\\desktop\\"
        self.create_widgets()
    def create_widgets(self):
        self.user_et_lb = Label(self, text="Instagram Username")
        self.user_et_lb.grid(row=0, column=0)
        self.user_et_lb.config(font=("Arial", 10))
        self.user_et = Entry(self)
        self.user_et.grid(row=0, column=1)
        self.user_et.config(font=("Arial", 10))

        self.folder_lb = Label(self, text="Output Folder")
        self.folder_lb.grid(row=1, column=0)
        self.folder_lb.config(font=("Arial", 10))
        self.folder_bt = Button(self, text="Selecionar", command=self.set_folder)
        self.folder_bt.grid(row=1, column=1, sticky=NSEW)
        self.folder_bt.config(font=("Arial", 10))

        self.download_bt = Button(self, text="Download", command=self.download)
        self.download_bt.grid(row=2, columnspan=2, sticky=NSEW)
        self.download_bt.config(font=("Arial", 12))
    def set_folder(self):
        self.folder_path = filedialog.askdirectory(title="Output Folder")
        if len(self.folder_path) > 60:
            self.folder_bt["text"] = self.folder_path[0:10]+"..."+self.folder_path[-1:-30]
        else:
            self.folder_bt["text"] = self.folder_path
    def download(self):
        if self.user_et.get() == '':
            messagebox.showerror("Empty Username", "The Username Field must not be empty.")
            return None
        try:
            chrome_options = Options()  
            chrome_options.add_argument("--headless") 
            driver = webdriver.Chrome('./chromedriver', options=chrome_options)
            driver.get('https://instagram.com/{}'.format(self.user_et.get()));
            time.sleep(5)
            imgs = driver.find_elements_by_css_selector("img.FFVAD")
            i = 1
            while True:
                if os.path.isdir(self.folder_path+self.user_et.get()+'_'+str(i)):
                    i+=1
                else:
                    break
            os.mkdir(self.folder_path+self.user_et.get()+'_'+str(i))
            n = 0
            for img in imgs:
                urllib.request.urlretrieve(img.get_attribute("src"), self.folder_path+self.user_et.get()+'_'+str(i)+"\\img_{}.jpg".format(n))
                n+=1
            driver.quit()
            os.system("explorer {}".format(self.folder_path+self.user_et.get()+'_'+str(i)))
            messagebox.showinfo("Download Completed", "All the images were successfully downloaded.")
        except:
            messagebox.showerror("Error", "Something unexpected has happened.")
        
app = App()
app.master.title("InstaDown")
app.mainloop()