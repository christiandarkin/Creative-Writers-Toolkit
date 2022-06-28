# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:35:51 2022

@author: user
"""
# Importing Required libraries & Modules
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import openai
from time import time,sleep
import re
from tkinter.filedialog import askopenfilename

global prompt
global filename
prompt="hello"
datastore=""




def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def isFileExists(filename):
    return os.path.isfile(filename)

def four_digit_string(num):
    num_str = str(num)
    if len(num_str) == 1:
        num_str = "000" + num_str
    elif len(num_str) == 2:
        num_str = "00" + num_str
    elif len(num_str) == 3:
        num_str = "0"+num_str
    return num_str

def gpt3_completion(prompt,suffix, engine='text-davinci-002', temp=1.0, top_p=1.0, tokens=1000, freq_pen=0.5, pres_pen=0.0, stop=['asdfasdf']):
    max_retry = 5
    retry = 0
    if suffix !="":
        tokens=1500
        temp=1.1
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,         # use this for standard models
                #model=engine,           # use this for finetuned model
                prompt=prompt,
                suffix=suffix,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            #save_gpt3_log(prompt, text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return None
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def find_number(s):
    for i in range(len(s)):
        if s[i].isdigit():
            return s[i:]
        return None






# Defining TextEditor Class
class TextEditor:
  # Defining Constructor
  def __init__(self,root):
    # Assigning root
    self.root = root
    # Title of the window
    self.root.title("TEXT EDITOR")
    # Window Geometry
    self.root.geometry("1200x700+200+150")
    # Initializing filename
    self.filename = None
    # Declaring Title variable
    self.title = StringVar()
    # Declaring Status variable
    self.status = StringVar()
    # Creating Titlebar
    self.titlebar = Label(self.root,textvariable=self.title,font=("times new roman",15,"bold"),bd=2,relief=GROOVE)
       
    # Packing Titlebar to root window
    self.titlebar.pack(side=TOP,fill=BOTH)
    # Calling Settitle Function
    self.settitle()
    # Creating Statusbar
    self.statusbar = Label(self.root,textvariable=self.status,font=("times new roman",15,"bold"),bd=2,relief=GROOVE)
    # Packing status bar to root window
    self.statusbar.pack(side=BOTTOM,fill=BOTH)
    # Initializing Status
    self.status.set("Welcome To Text Editor")
    # Creating Statusbar
   
    self.buttonbar = Frame(self.root, height=58, bg="grey")
    # Packing status bar to root window
    self.buttonbar.pack(side=BOTTOM,fill=BOTH)
    # Initializing Status
    #self.status.set("Welcome To Text Editor")
    
    
    
    
    # Creating Menubar
    self.menubar = Menu(self.root,font=("times new roman",15,"bold"),activebackground="skyblue")
    # Configuring menubar on root window
    self.root.config(menu=self.menubar)
    # Creating File Menu
    self.filemenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding New file Command
    self.filemenu.add_command(label="New",accelerator="Ctrl+N",command=self.newfile)
    # Adding Open file Command
    self.filemenu.add_command(label="Open",accelerator="Ctrl+O",command=self.openfile)
    # Adding Save File Command
    #self.filemenu.add_command(label="Save",accelerator="Ctrl+S",command=self.savefile)
    # Adding Save As file Command
    
    
    
    
    
    # Adding Seprator
    self.filemenu.add_separator()
    # Adding Exit window Command
    self.filemenu.add_command(label="Exit",accelerator="Ctrl+E",command=self.exit)
    # Cascading filemenu to menubar
    self.menubar.add_cascade(label="File", menu=self.filemenu)
    # Creating Edit Menu
    self.editmenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding Cut text Command
    self.editmenu.add_command(label="Cut",accelerator="Ctrl+X",command=self.cut)
    # Adding Copy text Command
    self.editmenu.add_command(label="Copy",accelerator="Ctrl+C",command=self.copy)
    # Adding Paste text command
    self.editmenu.add_command(label="Paste",accelerator="Ctrl+V",command=self.paste)
    # Adding Seprator
    self.editmenu.add_separator()
    # Adding Undo text Command
    self.editmenu.add_command(label="Undo",accelerator="Ctrl+U",command=self.undo)
    # Cascading editmenu to menubar
    self.menubar.add_cascade(label="Edit", menu=self.editmenu)
    
    
    
    # Creating autoedit Menu
    self.autoeditmenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding New file Command
    #self.autoeditmenu.add_command(label="Autowrite",accelerator="",command=self.gpt3)
    prompt_skeleton=""
    global filepath
    global prompt
    global style
    style="verbose style, lots of description.  show don't tell."
    prompt="test"
    #global x
    filepath=os.path.abspath("scratchpad_tools")
    filepath="scratchpad_tools"
    
       
    
    
    
    for foldername in os.listdir("scratchpad_tools"):
       sub_menu = Menu(self.autoeditmenu, tearoff=0)
       self.autoeditmenu.add_cascade(label=foldername,menu=sub_menu)
       for filename in os.listdir("scratchpad_tools/"+foldername):
           
           sub_menu.add_command(label=filename,accelerator="",command=lambda x=filename,y=foldername:
                                self.tool_open(x,y))
       
    # Cascading helpmenu to menubar
    self.menubar.add_cascade(label="Autowrite", menu=self.autoeditmenu)
    
    
    # Creating style Menu
    #self.stylemenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding New file Command
    #self.stylemenu.add_command(label="Hardboiled",accelerator="",command=lambda style="Hardboiled detective story with short sentenses and active verbs.  In the style of Lee Childs": self.restyle(style))
    #self.menubar.add_cascade(label="Style", menu=self.stylemenu)
    
    
    #button
    button1=Button(self.buttonbar,text='Colaborate',command=self.gpt3)
    button1.pack(side='bottom')
    
    self.filemenu.add_command(label="Save As",accelerator="Ctrl+A",command=self.saveasfile)
    
   
    
    # Creating Help Menu
    self.helpmenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding About Command
    self.helpmenu.add_command(label="About",command=self.infoabout)
    # Cascading helpmenu to menubar
    self.menubar.add_cascade(label="Help", menu=self.helpmenu)
    # Creating Scrollbar
    scrol_y = Scrollbar(self.root,orient=VERTICAL)
    # Creating Text Area
    self.txtarea = Text(self.root,yscrollcommand=scrol_y.set,font=("times new roman",15,"bold"),state="normal",relief=GROOVE)
    # Packing scrollbar to root window
    scrol_y.pack(side=RIGHT,fill=Y)
    # Adding Scrollbar to text area
    scrol_y.config(command=self.txtarea.yview)
    # Packing Text Area to root window
    self.txtarea.pack(fill=BOTH,expand=1)
    # Calling shortcuts funtion
    self.shortcuts()
  # Defining settitle function
  def settitle(self):
    # Checking if Filename is not None
    if self.filename:
      # Updating Title as filename
      self.title.set(self.filename)
    else:
      # Updating Title as Untitled
      self.title.set("Untitled")
  # Defining New file Function
  def newfile(self,*args):
    # Clearing the Text Area
    facts="FACTS:"
    self.txtarea.delete("1.0",END)
    # Updating filename as None
    self.filename = None
    # Calling settitle funtion
    self.settitle()
    # updating status
    self.status.set("New File Created")
  # Defining Open File Funtion
  def openfile(self,*args):
    # Exception handling
    try:
      # Asking for file to open
      self.filename = filedialog.askopenfilename(title = "Select file",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      # checking if filename not none
      if self.filename:
        # opening file in readmode
        infile = open(self.filename,"r")
        # Clearing text area
        self.txtarea.delete("1.0",END)
        # Inserting data Line by line into text area
        for line in infile:
          self.txtarea.insert(END,line)
        # Closing the file  
        infile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Opened Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Save File Funtion
  def savefile(self,*args):
    # Exception handling
    
    try:
      # checking if filename not none
      if self.filename:
        # Reading the data from text area
        data = self.txtarea.get("1.0",END)
        # opening File in write mode
        outfile = open(self.filename,"w")
        # Writing Data into file
        outfile.write(data)
        # Closing File
        outfile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Saved Successfully")
      else:
        self.saveasfile()
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Save As File Funtion
  
  
  
  
  
  
  def gpt3(self,*args):
      global prompt
      #grab data from text screen
      text2=""
      data = self.txtarea.get("1.0",END)
      if "[2]" in data:
          text2=data.split("[2]",1)[1]
          data=data[:data.find("[2]")]
          #prompt=prompt+" USE 1000 WORDS, 10 PARAGRAPHS:"
      else:
          suffix=""
      
      #print (data)
      #get prompt as everything up to 2NDPROMPT
      #get prompt3 as everything after 2ndprompt
      #prompt3=prompt.split("2NDPROMPT",1)[1]
      #prompt=prompt.split(1,"2NDPROMPT")[1]
      prompt2="WRITING STYLE:"+style+ prompt.replace('<<TEXT>>', data).replace('[2]',text2)
      
      if "[insert]" in prompt2:
          suffix=prompt2.split("[insert]",1)[1]
          prompt2=prompt2[:prompt2.find("[insert]")]
          #prompt=prompt+" USE 1000 WORDS, 10 PARAGRAPHS:"
      else: 
          suffix=""
          
      #print ("*************************\n"+prompt2)
      #print("PROMPT:"+prompt)
      #print("propt2:"+prompt3)
      print("QUERYING GPT3------------------------------------------------------------")
      completion="frogspawn"
      
      completion=gpt3_completion(prompt2,suffix)
      newstuff=data+"\n\n\n"+completion
      print(prompt2+"\n\n\n"+suffix)
 
      self.txtarea.delete("1.0",END)
      for line in newstuff:
        self.txtarea.insert(END,line)
      # Closing File
    
      # Calling Set title
      self.settitle()
      

  
      
  def tool_open(self,x,y):
  
       print("***********************"+filepath+"/"+y+"/"+x)
       print(x)
       tool_file=filepath+"/"+y+"/"+x
       infile = open(tool_file,"r")
       my_file = infile.read()
       left = "DESCRIPTION:"
       right = "END"
       #prompt= the rest after END
       global prompt
       prompt=my_file.split("END",1)[1]
        
       explanation=my_file.split(left)[1].split(right)[0]
       
       self.txtarea.delete("1.0",END)
       # Inserting data Line by line into text area
       for line in explanation:
             self.txtarea.insert(END,line)
           # Closing the file  
       infile.close()
           # Calling Set title
       self.settitle()
      
       self.status.set("Opened Successfully")

     
      
      
  def restyle(self,style):
    print("style")   
      
      
  def saveasfile(self,*args):
    # Exception handling
    try:
      # Asking for file name and type to save
      untitledfile = filedialog.asksaveasfilename(title = "Save file As",defaultextension=".txt",initialfile = "Untitled.txt",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      # Reading the data from text area
      data = self.txtarea.get("1.0",END)
      # opening File in write mode
      outfile = open(untitledfile,"w")
      # Writing Data into file
      outfile.write(data)
      # Closing File
      outfile.close()
      # Updating filename as Untitled
      self.filename = untitledfile
      # Calling Set title
      self.settitle()
      # Updating Status
      self.status.set("Saved Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Exit Funtion
  def exit(self,*args):
    op = messagebox.askyesno("WARNING","Your Unsaved Data May be Lost!!")
    if op>0:
      self.root.destroy()
    else:
      return
  # Defining Cut Funtion
  def cut(self,*args):
    self.txtarea.event_generate("<<Cut>>")
  # Defining Copy Funtion
  def copy(self,*args):
          self.txtarea.event_generate("<<Copy>>")
  # Defining Paste Funtion
  def paste(self,*args):
    self.txtarea.event_generate("<<Paste>>")
  # Defining Undo Funtion
  def undo(self,*args):
    # Exception handling
    try:
      # checking if filename not none
      if self.filename:
        # Clearing Text Area
        self.txtarea.delete("1.0",END)
        # opening File in read mode
        infile = open(self.filename,"r")
        # Inserting data Line by line into text area
        for line in infile:
          self.txtarea.insert(END,line)
        # Closing File
        infile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Undone Successfully")
      else:
        # Clearing Text Area
        self.txtarea.delete("1.0",END)
        # Updating filename as None
        self.filename = None
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Undone Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining About Funtion
  def infoabout(self):
    messagebox.showinfo("About Text Editor","A Simple Text Editor\nCreated using Python.")
  # Defining shortcuts Funtion
  def shortcuts(self):
    # Binding Ctrl+n to newfile funtion
    self.txtarea.bind("<Control-n>",self.newfile)
    # Binding Ctrl+o to openfile funtion
    self.txtarea.bind("<Control-o>",self.openfile)
    # Binding Ctrl+s to savefile funtion
    self.txtarea.bind("<Control-s>",self.savefile)
    # Binding Ctrl+a to saveasfile funtion
    #self.txtarea.bind("<Control-a>",self.saveasfile)
    # Binding Ctrl+e to exit funtion
    self.txtarea.bind("<Control-e>",self.exit)
    # Binding Ctrl+x to cut funtion
    self.txtarea.bind("<Control-x>",self.cut)
    # Binding Ctrl+c to copy funtion
    self.txtarea.bind("<Control-c>",self.copy)
    # Binding Ctrl+v to paste funtion
    #self.txtarea.bind("<Control-v>",self.paste)
    # Binding Ctrl+u to undo funtion
    self.txtarea.bind("<Control-u>",self.undo)
# Creating TK Container
root = Tk()
# Passing Root to TextEditor Class

(root)
# Root Window Looping

TextEditor(root)

root.mainloop()