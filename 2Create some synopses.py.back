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
            text = re.sub('\s+', ' ', text)
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
    return s.replace(' ', '')

def remove_speechmarks(s):
    remove_chars = '<  > : " / \ | ? *.!@#$%^&*(){}[].,-?`;:'
    s = s.translate({ ord(c): None for c in remove_chars })
    return s

if __name__ == '__main__':
    print("This code creates synopses")
    print("You can start from scratch, or use other text files (such as story backgrounds, series information, or characters)")
    print("to spark the ideas")
    print("You can create multiple stories at a time")
    #print("This code will create two files per story: a detailed breakdown, and a short summary")
    
    #ask for genre
    storytype=input("Genre or type of story (leave blank if you like):")
    #ask for supporting files
    print("For supporting files, you can bring in characters who will appear in the story")
    print("or you can import background info like desciptions of themes, or ideas you want to explore ")
    print("alternatively you could create a text file giving the backstory, or details of the world of the story")
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
    if supportingfiles=="":
        supportingfiles=="Intelligent, original storyline with large amounts of colour and detail."
        
    #ask for tweaks
    print("Now you can add any additional info.  This can be a short description")
    print("eg.  'a kids story about robots'")
    print("or 'A story in which the above character is the hero (if you've loaded in a protagonist character)")
    print("or 'a story set in the world described above - again, any note will work!")
    tweak=""
    tweak=input("Additional Story information?")
    if tweak !="":
        tweak="Make the story "+tweak
  
    #ask for folder
    nul=input("choose a folder to save the storylines (hit return to continue)")
    root = Tk()
    root.attributes("-topmost", True)
    folder_location = tk.filedialog.askdirectory()
    root.destroy()
    print ("Folder chosen: "+folder_location)
    
    #ask how many characters
    chars=1
    ch=input("How many stories shall we brainstorm?")
    chars=int(ch)
    
    #ask for a title
    title=input("Story Title:")
   
    #load in prompt and assemble
    folder = "planprompts/"
    filename = "synopsisprompt.txt"
    filepath = os.path.join(folder, filename)
    with open(filepath, "r") as f:
         prompt = f.read() 
    prompt = prompt.replace('<<STORYTYPE>>', storytype).replace('<<SUPPORTINGFILES>>', supportingfiles).replace('<<TWEAK>>', tweak)
    
    #call gpt3
    for char in range (1,chars+1):
     print("Querying GPT3..........................................")   
     completion1 = gpt3_completion(prompt)
     #get story name
     completion1="The story begins "+completion1
     completion1 = completion1.replace(r'\n', '\n\n')
     name=title+str(char)+".txt"
     print("File title:"+name)
     print(completion1)
     #create scene breakdown
     #folder = "planprompts/"
     #filepath = os.path.join(folder, "synopsistoscenelist_multi.txt")
     #with open(filepath, "r") as f:
     #  prompt8 = f.read() 
     
     #3 run the prompt
     #scriptprompt= prompt8.replace('<<STORYTYPE>>', storytype).replace('<<SUPPORTINGFILES>>', supportingfiles).replace('<<TWEAK>>', tweak).replace('<<SYNOPSIS>>', completion1)
     #print("QUERYING GPT3_____________________________________")
     #completion8="frogspawn"
     #completion8 = gpt3_completion(scriptprompt)
     #completion8 = completion8.replace(r'\n', '\n')
     #completion8="SCENE001:"+completion8
     #print(completion8)
       
     #save files
     filepath = os.path.join(folder_location, "synopsis_"+name)
     with open(filepath,"w",encoding="utf-8") as f:
         f.write(completion1)
     #filepath = os.path.join(folder_location, "story_breakdown_"+name)
     #with open(filepath,"w",encoding="utf-8") as f:
     #    f.write(completion8)   
    
    #find character name and save detailed character
    #call gpt3 again to create precis and save
    
