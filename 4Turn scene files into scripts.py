# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:49:33 2022

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

def four_digit_string(num):
    num_str = str(num)
    if len(num_str) == 1:
        num_str = "000" + num_str
    elif len(num_str) == 2:
        num_str = "00" + num_str
    elif len(num_str) == 3:
        num_str = "0"+num_str
    return num_str

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
  bk=""
  scriptprompt=""
  supportingfiles=""
  storysofar=""
  tobewritten=""
  lastscript=""
    
  print("This code turns a SCENE000x file into a movie script scene.")
  #ask for a scene file
  
  
  
  getcha= input("choose a scene file(y/n):")
  if getcha != "n":
        root = Tk()
        root.filename =  askopenfilename(initialdir = "/",title = "Select scene file",filetypes = (("text files","*.txt"),("all files","*.*")))
        #print (root.filename)
        scenefile=""
        with open(root.filename, "r",encoding="utf8") as f:
            scenefile = f.read()
            scenename=os.path.basename(root.filename)
            folderpath=os. path. dirname(root.filename)
            root.destroy()
  else:
       quit()
       
       
  
  
  #get thenumber of the file
  print("scene name"+scenename)
  #print(scenename[-4:-7])
  scenenumber=int(scenename[-8:-4])
  while True:  #start a new scene
         
          
    # load in script from previous scene if it exists as lastscript
    lastscript=""
    
    previousscenenumber=four_digit_string(scenenumber-1)
    filename = "SCRIPT_SCENE"+previousscenenumber+".txt"
    print("script we're looking for:"+filename)
    filepath = os.path.join(folderpath, filename)
    if isFileExists(filepath):
        with open(filepath, "r", encoding='utf-8') as f:
            lastscript = f.read() 
   
    #add scriptexample
   
    folder = "planprompts/"
    filepath = os.path.join(folder, "scriptexample.txt")
    with open(filepath, "r", encoding='utf-8') as f:
        scriptexample = f.read()
    
    
    #create a string, storysofar from the preceding 6 scene files(not including last preceding file)
    storysofar=""
    storysofarscenes=scenenumber-1
    if storysofarscenes>6:
            pastsc=storysofarscenes-6
    else:
            pastsc=1
    if storysofarscenes >0:
        for s in range (pastsc,storysofarscenes):
            snum= four_digit_string(s)
            filename="SCENE"+snum+".txt"
            filepath = os.path.join(folderpath, filename)
            if isFileExists(filepath):
                with open(filepath, "r", encoding='utf-8') as f:
                    storysofar=storysofar+"\n"+ f.read()
    print ("The Story So Far..."+"\n"+storysofar)
        
    #create a string, tobewritten from preceding 1 file+current file
    tobewritten=""
    tobewrittenscenes=scenenumber-1
    if tobewrittenscenes >0:
        tbw=four_digit_string(tobewrittenscenes)
        filename="SCENE"+tbw+".txt"
        filepath = os.path.join(folderpath, filename)
        if isFileExists(filepath):
            with open(filepath, "r", encoding='utf-8') as f:
                tobewritten=f.read() 
    elif tobewrittenscenes==0:
        tobewritten=scenefile
    
    print ("Writing now..."+"\n"+tobewritten)
    print("+"+scenefile)
    
    folderpath1=folderpath
    #begin supporting file loop   
    while True:
        #ask for background file
        supporting=input("Load supporting files(for this scene)(y/n)?")
        supportingfiles=""
        #load primer file
        filename="primer.txt"
        filepath = os.path.join(folderpath1, filename)
        if isFileExists(filepath):
            with open(filepath, "r", encoding='utf-8') as f:
                supportingfiles=f.read()+"\n\n"
        
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
                with open(root.filename, "r", encoding='utf-8') as f:
                    ftext = f.read()
                    root.destroy()
                    #load file
                    supportingfiles=supportingfiles+ftext+"\n"
                    bk=0
                    an=input("Load Another(y/n)?")
                    if an=="n":
                        bk=1
                        break
        if bk==1:
            break
        elif supporting=="n":
            break
        
    #ask for tweaks
    tweak=input("Any additional notes for this scene (eg: atmosphere, moods, etc.):")
    
    #load prompts
    folder = "planprompts/"
    filepath = os.path.join(folder, "scriptscene.txt")
    with open(filepath, "r", encoding='utf-8') as f:
         prompt = f.read()
    
    
    #clear extras
    extras=""
    #begin scene picking loop
    while True:
                
                #create a prompt with everything + a request to script scene_"scene"
                scriptprompt= prompt.replace('<<BACKGROUND>>', supportingfiles).replace('<<STORYSOFAR>>', storysofar).replace('<<SCENESYNOPSIS>>', tobewritten).replace('<<SCENESYNOPSIS2>>',scenefile+"\n\n"+extras).replace('<<NOTES>>', tweak).replace('<<PREVIOUSSCENE>>',lastscript).replace('<<SCRIPTEXAMPLE>>', scriptexample)
                print("here's the prompt"+"\n"+scriptprompt)
                print("QUERYING GPT3_____________________________________")
                completion="frogspawn"
                #print(scriptprompt)
                completion = gpt3_completion(scriptprompt)
               
                completion = completion.replace(r'\n', '\n')
                #completion8="SCENE001: "+completion8
                print(completion)
                filepath = os.path.join(folderpath, "SCRIPT_"+scenename)
                with open(filepath,"w",encoding="utf-8") as f:
                    f.write(extras+completion)
                
                print("1 Accept and move on to next scene")
                print("2 This scene is crap.  Redo")
                print("3 This scene is unfinished.  Add more to the end...")
                bk=0
                goy=input("1,2, or 3:")
               
                if goy=="1":
                    bk=1
                    break
                elif goy=="3":
                    print("you've chosen to add more..")
                    extras=extras+completion
                    #lastscript=lastscript+extras
                    continue
                elif goy=="2":
                    extras=""
                    continue
    #if bk==1:
        #break
    nxt=input("continue to next scene?")
    if nxt !="n":
      scenenumber=scenenumber+1
      snum= four_digit_string(scenenumber)
      filename = "SCENE"+snum+".txt"
      print(filename)
      filepath = os.path.join(folderpath, filename)
      if isFileExists(filepath):
          with open(filepath, "r", encoding='utf-8') as f:
              scenefile = f.read()  
              scenename=filename
      else:
          quit()
    elif nxt =="n":
        quit()
          
          
            
          #query gpt3
            
            #completionsave=extras+completion
            #save completionsave as SCRIPT_SCENE
    
            #ask for accept, add to  or redo
    
            #if redo then 2nd loop
            
            #if add to then, lastscript=lastscript+extras  extras=extras+completion then 2nd loop
            
    
            #if accept, then break 2nd loop
            