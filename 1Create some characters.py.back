# -*- coding: utf-8 -*-
"""
Created on Thu May 26 09:00:55 2022

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
    
def remove_linebreaks(s):
    return re.sub(r'[\r\n]+', '', s)

def remove_nonprintable(s):
    return re.sub(r'[^\x00-\x7F]+','', s)

def remove_spaces(s):
        #remove_chars = '<  > : " / \ | ? *.!@#$%^&*(){}[].,-?`;:'
        #s = s.translate({ ord(c): None for c in remove_chars })
        #return s
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)

if __name__ == '__main__':
    print("This code creates characters for your stories")
    print("You can start from scratch, or use other text files (such as story synopses, series information, or other characters)")
    print("to spark the ideas")
    print("You can create multiple characters at a time")
    print("This code will create two files per character: a detailed character breakdown, and a precis")
    
    #ask for genre
    storytype=input("Genre or type of story your character will appear in (leave blank if you like):")
    #ask for supporting files
    print("For supporting files, you can bring in a synopsis, and brainstorm a main, or supporting character")
    print("or you can import another character and brainstorm their husband, or enemy, etc. ")
    print("alternatively you could create a text file describing an alien race, and brainstorm a member of that species")
    print("in fact any text file will do - keep it short though.  Less is more")
    supporting=input("Load supporting files(y/n)?")
    supportingfiles=""
    if supporting=="y":
      while True:
        ftext=""
        root = Tk()
        root.filename =  askopenfilename(initialdir = "/",title = "Select supporting file",filetypes = (("text files","*.txt"),("all files","*.*")))
        #print (root.filename)
        scenename=os.path.basename(root.filename)
        folderpath=os. path. dirname(root.filename)
        print(folderpath)
        ftext=""
        with open(root.filename, "r") as f:
            ftext = f.read()
        root.destroy()
        #load file
        supportingfiles=supportingfiles+ftext+"\n"
        an=input("Load Another(y/n)?")
        if an=="n":
            break
        
    #ask for tweaks
    print("Now you can add any additional info.  This can be a short description")
    print("eg.  'a character you'd find in a murder mystery'")
    print("or 'the antagonist in the above story (if you've loaded in a supporting synopsis)")
    print("or 'someone with a grudge against the character above' - again, any note will work!")
    tweak=""
    tweak=input("Additional character information?")
    if tweak !="":
        tweak="Make the character "+tweak
  
    #ask for folder
    nul=input("choose a folder to save the characters (hit return to continue)")
    root = Tk()
    root.attributes("-topmost", True)
    folder_location = tk.filedialog.askdirectory()
    root.destroy()
    print ("Folder chosen: "+folder_location)
    
    #ask how many characters
    chars=1
    ch=input("How many characters shall we brainstorm?")
    chars=int(ch)
   
    #load in prompt and assemble
    folder = "planprompts/"
    filename = "prompt01.txt"
    filepath = os.path.join(folder, filename)
    with open(filepath, "r") as f:
         prompt = f.read() 
    prompt = prompt.replace('<<STORYTYPE>>', storytype).replace('<<SUPPORTINGFILES>>', supportingfiles).replace('<<TWEAK>>', tweak)
    
    #call gpt3
    for char in range (1,chars+1):
     print("Querying GPT3..........................................")   
     completion1 = gpt3_completion(prompt)
     #get character name
     completion1="1)"+completion1
     completion1 = completion1.replace(r'\n', '\n\n')
     name="000"
     name = completion1[completion1.find("Name:")+len("Name:"):completion1.find("2)")]
     name = remove_linebreaks(name)
     name = remove_nonprintable(name)
     name = remove_spaces(name)
     if name == None:
         name=""
     name=name+str(char)+".txt"
     print("character name:"+name)
     print(completion1)
     #create precis
     print("Querying GPT3..........................................")   
     completion2 = gpt3_completion("Create a brief, 1 pargagraph summary of the following character"+"\n"+ completion1+"\n"+name+"\nSUMMARY:")
     print (completion2)
     #save files
     filepath = os.path.join(folder_location, name)
     with open(filepath,"w",encoding="utf-8") as f:
         f.write(completion1)
     filepath = os.path.join(folder_location, "Precis_"+name)
     with open(filepath,"w",encoding="utf-8") as f:
         f.write(completion2)   
    
    #find character name and save detailed character
    #call gpt3 again to create precis and save
    