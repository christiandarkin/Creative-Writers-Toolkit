# -*- coding: utf-8 -*-
"""
Created on Wed May 25 08:40:09 2022

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

if __name__ == '__main__':
    #load the scene list
    print("This code takes a scene list and splits it into individual files by scene number.")
    print("You'll need a txt file containing a synopsis of each scene, numbered SCENE001, SCENE002, SCENE003, etc.  Capitals and numbering matter!!")
    getcha= input("choose a scene list to split(y/n):")
    if getcha != "n":
        root = Tk()
        root.filename =  askopenfilename(initialdir = "/",title = "Select scene file",filetypes = (("text files","*.txt"),("all files","*.*")))
        #print (root.filename)
        completion7=""
        with open(root.filename, "r") as f:
            completion7 = f.read()
            root.destroy()
    else:
                completion7=""  
    
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
    textu = completion7
    #textu="SCENE001 Doctor Who arrives on galifrey.  he exits the TARDIS SCENE002 The Master is watching via a hidden camera.  He is happy the doctor has arrived.  His plans are going to be fulfilled. SCENE003 Doctor Who has a conversation with the President.  The president has news about dark rumours about a threat to the whole universe.  This is why Doctor Who has been summoned.  Doctor Who is initially angry at having been summoned, but, when he hears the news, he agrees to help the Time Lords."
    textu = textu.replace('\r', '').replace('\n', '')
    textu=textu+"END"
    print(textu)
    scenes = re.findall("SCENE\d\d\d", textu)
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
 

       
       
       
       
       