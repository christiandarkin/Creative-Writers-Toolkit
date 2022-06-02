# -*- coding: utf-8 -*-
"""
Created on Wed May 25 19:24:59 2022

@author: user
"""


import os
import openai
from time import time,sleep
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def isFileExists(filename):
    return os.path.isfile(filename)

def gpt3_completion(prompt, engine='text-davinci-002', temp=1.0, top_p=1.0, tokens=1000, freq_pen=0.5, pres_pen=0.0, stop=['asdfasdf']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,         # use this for standard models
                #model=engine,           # use this for finetuned model
                prompt=prompt,
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

if __name__ == '__main__':
    #1pick a synopsis
    inputy = input("Hit any key to load a synopsis:")     
    root = Tk()
    root.filename =  askopenfilename(initialdir = "/",title = "Select synopsis",filetypes = (("text files","*.txt"),("all files","*.*")))
    #print (root.filename)
    scenename=os.path.basename(root.filename)
    folderpath=os. path. dirname(root.filename)
    print(folderpath)
    completion7=""
    with open(root.filename, "r", encoding='utf-8') as f:
        completion7 = f.read()
    root.destroy()
    extrainfo=""
    inputy = input("load extra background info y/n:")     
    if inputy =="y":
      root = Tk()
      root.filename =  askopenfilename(initialdir = "/",title = "Select synopsis",filetypes = (("text files","*.txt"),("all files","*.*")))
      #print (root.filename)
      scenename2=os.path.basename(root.filename)
      folderpath2=os. path. dirname(root.filename)
      print(folderpath2)
      extrainfo=""
      with open(root.filename, "r", encoding='utf-8') as f:
        extrainfo = f.read()
      root.destroy()
     
    print('It"s usually best to start by dividing into a small number of scenes (less than 10) then dividing those scenes as appropriate)')  
    numb=input('How many scenes (roughly) do you want?')
    numberofscenes='10'
    numberofscenes=numb
     
    
    #2load in the prompt file
   
    folder = "planprompts/"
    filepath = os.path.join(folder, "synopsistoscenelist.txt")
    with open(filepath, "r", encoding='utf-8') as f:
       prompt8 = f.read() 
       
    folder = "planprompts/"
    filepath = os.path.join(folder, "breakdownexample.txt")
    with open(filepath, "r", encoding='utf-8') as f:
        breakdownexample = f.read() 
    
    #3 run the prompt
    scriptprompt= prompt8.replace('<<SYNOPSIS>>', completion7).replace('<<BREAKDOWNEXAMPLE>>',breakdownexample).replace('<<EXTRAINFO>>',extrainfo).replace('<<NUMSCENES>>',numberofscenes)
    print(scriptprompt)
    while True:
    
     print("QUERYING GPT3_____________________________________")
     completion8="frogspawn"
     #print(scriptprompt)
     completion8 = gpt3_completion(scriptprompt)
     completion9=completion8
     completion8 = completion8.replace(r'\n', '\n')
     #completion8="SCENE001: "+completion8
     completion8="SCENE0001:"+completion8
     print(completion8)
     print("1 Accept and save")
     print("2 This is crap.  Redo")
     print("3 quit")
     goy=input("1,2, or 3:")
     if goy=="2":
         continue
     elif goy=="3":
         quit()
     elif goy=="1":
         #root = Tk()
         #root.filename =  asksaveasfilename(initialdir = "/",title = "Save Scene list",filetypes = (("text files","*.txt"),("all files","*.*")))
         #print (root.filename)
        
         #scenename=os.path.basename(root.filename)
         #folderpath=os. path. dirname(root.filename)
         #print(folderpath)
         ##completion8="SCENE01"+completion8
         #completion7=""
         #with open(root.filename+".TXT", "w", encoding='utf-8') as f:
         #    f.write(completion8)  # write some data to the file
                         
         #    root.mainloop()
         #root.destroy()
        
         
         #get folder for storing scenes
         bg=input("pick a folder to store your scenes:")
         if bg !="4535":
            root = Tk()
            root.withdraw()
            folder = filedialog.askdirectory()
                     
         
         print('Primer file (this is a file to include in each scene which gives basic info on character/world, etc.')
         print('You don"t need it and you can add additional files to fine-tune each scene before writing.')
         print('However, it can help add detail (for example, about the world of the story, or the way characters behave)')
         primerfile=input('Primer (y/n)')
         primer=""
         if primerfile=="y":
             root = Tk()
             root.filename =  askopenfilename(initialdir = "/",title = "Select scene file",filetypes = (("text files","*.txt"),("all files","*.*")))
             #print (root.filename)
             primer=""
             with open(root.filename, "r",encoding="utf8") as f:
                 primer = f.read()
                 scenename=os.path.basename(root.filename)
                 folderpath=os. path. dirname(root.filename)
                 root.destroy()
         
         #divide scene list into files
         textu = completion8
         #textu="SCENE001 Doctor Who arrives on galifrey.  he exits the TARDIS SCENE002 The Master is watching via a hidden camera.  He is happy the doctor has arrived.  His plans are going to be fulfilled. SCENE003 Doctor Who has a conversation with the President.  The president has news about dark rumours about a threat to the whole universe.  This is why Doctor Who has been summoned.  Doctor Who is initially angry at having been summoned, but, when he hears the news, he agrees to help the Time Lords."
         textu = textu.replace('\r', '').replace('\n', '')
         textu=textu+"END"
         print(textu)
         scenes = re.findall("SCENE\d\d\d\d", textu)
         #folder="scenes/"
         print(scenes)
         full_script=""
         for scene in scenes:
              print(scene)
              scene_text = re.search(scene + "(.*?)" + "(?=SCENE|END)", textu).group(1)
              print(scene_text)
          
              filepath = os.path.join(folder, scene)
              with open(filepath + ".txt","w") as f:
                  f.write(scene_text)
         #save primer file
         if primer !="":
             filepath = os.path.join(folder, "primer.txt")
             with open(filepath,"w") as f:
                 f.write(primer)
         quit()
         
     
    #4 do you want to accept or rerun?
    