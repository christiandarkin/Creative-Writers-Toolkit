# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Importing Required libraries & Modules
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import openai
global selected_text1
global selected_background
global selected_synopsis
import re

selected_text1=""
selected_background=""
selected_synopsis=""




def autosave():
    # do something you want
    writing.savefile
    print("autosave")
    root.after(60000 * 5, autosave) # time in milliseconds
    
    
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def isFileExists(filename):
    return os.path.isfile(filename)

def gpt3_completion(prompt, suffix,stop, engine='text-davinci-002', temp=1.1, top_p=1.0, tokens=250, freq_pen=0.8, pres_pen=0.0):
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









# Defining TextEditor Class
class TextEditor:
  # Defining Constructor
 
  def __init__(self,root,title,position,selected):
    self.selected="NONE"
   
    # Assigning root
    self.root = root
    # Title of the window
    global windowtitle
    
    global selected_background
    global selected_synopsis  
    windowtitle=title
    self.root.title(title)
    # Window Geometry
    self.root.geometry(position)
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
    self.filemenu.add_command(label="Save",accelerator="Ctrl+S",command=self.savefile)
    # Adding Save As file Command
    self.filemenu.add_command(label="Save As",accelerator="Ctrl+A",command=self.saveasfile)
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
    # Creating Help Menu
    self.helpmenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding About Command
    self.helpmenu.add_command(label="About",command=self.infoabout)
    # Cascading helpmenu to menubar
    self.menubar.add_cascade(label="Help", menu=self.helpmenu)
    
    #button
    if windowtitle=="CONVERSATION EDITOR":
      button1=Button(self.buttonbar,text='CHARACTER1',command=self.gpt3_1)
      button1.pack(side=LEFT)
      button1=Button(self.buttonbar,text='CHARACTER2',command=self.gpt3_2)
      button1.pack(side=RIGHT)
      button1=Button(self.buttonbar,text='DESCRIPTION',command=self.describe)
      button1.pack()
    if windowtitle=="DESCRIPTION NOTES":
      button1=Button(self.buttonbar,text='DESCRIBE',command=self.gpt3_3)
      button1.pack()
    #button
    #button1=Button(self.buttonbar,text='Hilight',command=self.Hilight)
    #button1.pack(side=LEFT)
    
    
    
    
    
    
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
    
    #get selected stuff
    ranges = self.txtarea.tag_ranges(SEL)
    if ranges:
        context_writing=self.txtarea.get(*ranges)
    
  
    
  
    
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
    
  
  def accept(self,*args):
    
    for line in self.txtarea.get("1.0",END):
      writing.txtarea.insert(END,line)
    # Calling Set title
    writing.settitle() 
    self.root.destroy()
      
      
  def describe(self,*args):
      new_text_window=TextEditor(Tk(),"DESCRIPTION NOTES","600x300+1200+150",selected_new_text)
      #for line in newstuff:
      #  new_text_window.txtarea.insert(END,line)
      # Calling Set title
      new_text_window.settitle()
  
  def gpt3_3(self,*args):
     
     global selected_text1
     global selected_background
     global selected_synopsis
     global sel1
     global selected_new_text  
     suffix=""
     #Get the prompt material
     print("...............................")
                
     folder = "planprompts/"
     filename = "descriptionprompt.txt"
     
     filepath = os.path.join(folder, filename)
     with open(filepath, "r") as f:
          prompt = f.read() 
            
     prompt = prompt.replace('<<NOTES>>', self.txtarea.get("1.0","end"))
     #if prompt contains INSERT then prompt_a= everything before insert and suffix=everything after
     if "[insert]" in prompt:
         suffix=prompt.split("[insert]",1)[1]
         prompt=prompt[:prompt.find("[insert]")]
         prompt=prompt+" USE 1000 WORDS, 10 PARAGRAPHS:"
     else:
         suffix=""
        
     
     print(prompt)  
     print("------------------querying gpt3")
     print(suffix)
     stop="CHARACTER2:"
     completion1 = gpt3_completion(prompt,suffix,stop)
     #completion1="lkjlkfjaslkdfjsadlkfjsa dklfsadj kfskld fklsdf kl!"
     completion1 = completion1.replace(r'\n', '\n\n')
    
       
     #add newstuff to the end of the text window    
     newstuff=completion1
     #self.txtarea.delete("1.0",END)
    
     
     #REPLACEMENT CODE FOR ABOVE:  OPEN A NEW WINDOW AND SHOW COMPLETION
     
     for line in newstuff:
       writing.txtarea.insert(END,line)
     # Calling Set title
     #new_text_window.settitle()  
  
    
  
  def gpt3_1(self,*args):
      
      global selected_text1
      global selected_background
      global selected_synopsis
      global sel1
      global selected_new_text  
      suffix=""
      #Get the prompt material
      print("...............................")
      
      selected_text1= writing.txtarea.get("end-5l","end")
      selected_background=background.txtarea.get("1.0","end")
      selected_synopsis=synopsis.txtarea.get("1.0","end")
      #selected_new_text=new_text_window.selected
      
      folder = "planprompts/"
      filename = "conversationch1prompt.txt"
      
      filepath = os.path.join(folder, filename)
      with open(filepath, "r") as f:
           prompt = f.read() 
      filename = "novellayout.txt" 
      filepath = os.path.join(folder, filename)
      with open(filepath, "r") as f:
           example = f.read() 
        
      prompt = prompt.replace('<<CHARACTER1>>', selected_background).replace('<<CHARACTER2>>', selected_synopsis).replace('<<CONVERSATION>>', selected_text1).replace('<<EXAMPLE>>', example)
      #if prompt contains INSERT then prompt_a= everything before insert and suffix=everything after
      if "[insert]" in prompt:
          suffix=prompt.split("[insert]",1)[1]
          prompt=prompt[:prompt.find("[insert]")]
          prompt=prompt+" USE 1000 WORDS, 10 PARAGRAPHS:"
      else:
          suffix=""
         
      
      print(prompt)  
      print("------------------querying gpt3")
      print(suffix)
      stop="CHARACTER2:"
      completion1 = gpt3_completion(prompt,suffix,stop)
      #completion1="lkjlkfjaslkdfjsadlkfjsa dklfsadj kfskld fklsdf kl!"
      completion1 = completion1.replace(r'\n', '\n\n')
     
        
      #add newstuff to the end of the text window    
      newstuff="\n\nCHARACTER1:"+completion1
      #self.txtarea.delete("1.0",END)
     
      
      #REPLACEMENT CODE FOR ABOVE:  OPEN A NEW WINDOW AND SHOW COMPLETION
      
      for line in newstuff:
        writing.txtarea.insert(END,line)
      # Calling Set title
      #new_text_window.settitle()
      
      
  def gpt3_2(self,*args):
          
          global selected_text1
          global selected_background
          global selected_synopsis
          global sel1
          global selected_new_text  
          suffix=""
          #Get the prompt material
          print("...............................")
          
          selected_text1= writing.txtarea.get("end-5l","end")
          selected_background=background.txtarea.get("1.0","end")
          selected_synopsis=synopsis.txtarea.get("1.0","end")
          #selected_new_text=new_text_window.selected
          
          folder = "planprompts/"
          filename = "conversationch2prompt.txt"
          
          filepath = os.path.join(folder, filename)
          with open(filepath, "r") as f:
               prompt = f.read() 
          filename = "novellayout.txt" 
          filepath = os.path.join(folder, filename)
          with open(filepath, "r") as f:
               example = f.read() 
          prompt = prompt.replace('<<CHARACTER1>>', selected_background).replace('<<CHARACTER2>>', selected_synopsis).replace('<<CONVERSATION>>', selected_text1).replace('<<EXAMPLE>>', example)
          #if prompt contains INSERT then prompt_a= everything before insert and suffix=everything after
          if "[insert]" in prompt:
              suffix=prompt.split("[insert]",1)[1]
              prompt=prompt[:prompt.find("[insert]")]
              prompt=prompt+" USE 1000 WORDS, 10 PARAGRAPHS:"
          else:
              suffix=""
             
          
          print(prompt)  
          print("------------------querying gpt3")
          print(suffix)
          stop="CHARACTER1:"
          completion1 = gpt3_completion(prompt,suffix,stop)
          #completion1="lkjlkfjaslkdfjsadlkfjsa dklfsadj kfskld fklsdf kl!"
          completion1 = completion1.replace(r'\n', '\n\n')
         
            
          #add newstuff to the end of the text window    
          newstuff="\n\nCHARACTER2:"+completion1
          #self.txtarea.delete("1.0",END)
         
          
          #REPLACEMENT CODE FOR ABOVE:  OPEN A NEW WINDOW AND SHOW COMPLETION
          
          for line in newstuff:
            writing.txtarea.insert(END,line)
          # Calling Set title
          #new_text_window.settitle()
  
  
  
  
  def Hilight(self,*args):
      global selected_text1
      global selected_background
      global selected_synopsis
      global windowtitle
      global selected_new_text     
      ranges = self.txtarea.tag_ranges(SEL)
      
      if ranges:
          context_writing=self.txtarea.get(*ranges)
          self.txtarea.tag_delete ("start","end")
          self.txtarea.tag_add("start",*ranges)
          self.txtarea.tag_config("start", background= "", foreground= "red")
          print('SELECTED Text is %r' % context_writing)
          selected=context_writing
          self.selected=selected
          #windowtitle=label["title"]
          print(__name__)
          print(windowtitle)
                  
         
      else:
          print('NO Selected Text')
          selected=""
      
     
      
     
selected_text="frog"
selected_background="newt"
selected_synopsis="toad"
selected_new_text="egg"
selected=""
# Creating TK Container
root = Tk()
#synops=Tk()
# Passing Root to TextEditor Class

writing=TextEditor(root,"CONVERSATION EDITOR","750x700+400+0",selected_text)
background=TextEditor(Tk(),"FIRST CHARACTER","350x700+00+0",selected_background)
synopsis=TextEditor(Tk(),"SECOND CHARACTER","350x700+1250+000",selected_synopsis)


print(writing.selected)
print(background.selected)
# Root Window Looping
autosave()
root.mainloop()