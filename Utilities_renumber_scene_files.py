# -*- coding: utf-8 -*-
"""
Created on Mon May 30 08:26:00 2022

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
    print("Once you start breaking down your scene files into subscenes, you can end up with a lot of files that aren't numbered correctly")
    print("This code creates a new series of SCENE00001, SCENE0002, etc. files which make sense to the scene scripting and novelisation code")
    print("NOTE: You'll need to delete or rename old SCENE**** files which you've split into other scenes before you run this code")
    
    getcha=input("Hit return to select your first SCENE file (the one you want to become SCENE0001")
    #load scene 0001 file
    nextscenetoloadfile="SCENE0001.txt"
    nextscenetoloadnum=1
    text_nextscenetoload="frogspawn"
    if getcha != "n":
          root = Tk()
          root.filename =  askopenfilename(initialdir = "/",title = "Select scene file",filetypes = (("text files","*.txt"),("all files","*.*")))
          #print (root.filename)
          scenefile=""
          with open(root.filename, "r",encoding="utf8") as f:
              text_nextscenetoload = f.read()
              nextscenetoloadfile=os.path.basename(root.filename)
              if nextscenetoloadfile[-8:-4].isdigit():
                  nextscenetoloadnum=int(nextscenetoloadfile[-8:-4])
                  
              scenesfolderpath=os. path. dirname(root.filename)
              root.destroy()
    else:
         quit()
    
    
    
    fs=input("Hit return to select a folder to save your renumbered files(choose a new, empty folder)")
    #choose folder
    if fs !="4535":
       root = Tk()
       root.withdraw()
       savefolder = filedialog.askdirectory()
       root.destroy()
    nextscenetosavenum=1
    
    
    
    #start a loop
    
    
    while True:
        #save text of currently loaded scene to the save folder
        currentsc=four_digit_string(nextscenetosavenum)
        nextscenetosave = "SCENE"+currentsc+".txt"
        savefilepath = os.path.join(savefolder, nextscenetosave)
        with open(savefilepath, "w", encoding='utf-8') as f:
            f.write(text_nextscenetoload)
        
        # if nextscenetoloadfile exists then
            #load in scene file  as 
        nextscenetoloadnum=nextscenetoloadnum+1
        currentld=four_digit_string(nextscenetoloadnum)
        nextscenetoloadfile="SCENE"+currentld+".txt"   
        filepath = os.path.join(scenesfolderpath, nextscenetoloadfile)
        if isFileExists(filepath)== True :            
            with open(filepath, "r", encoding='utf-8') as f:
                text_nextscenetoload = f.read()
            
            
            #save the scene in selected folder as currentscenetosavefile 
        elif  isFileExists(filepath) ==False : 
        # if nextscenetoload doesn't exist then
        #load in the scene file
        #grab the filename as nextscenetoloadfile 
        #strip the numbers out of it and convert for nextscenetoloadnum
            nex=input("Locate next scene after"+nextscenetoloadfile +"?")
            root = Tk()
            root.filename =  askopenfilename(initialdir = "/",title = "Select scene file",filetypes = (("text files","*.txt"),("all files","*.*")))
            #print (root.filename)
            scenefile=""
            nextscenetoloadnum=1
            with open(root.filename, "r",encoding="utf8") as f:
                text_nextscenetoload = f.read()
                nextscenetoloadfile=os.path.basename(root.filename)
                if nextscenetoloadfile[-8:-4].isdigit()==True:
                    nextscenetoloadnum=int(nextscenetoloadfile[-8:-4])
                
                scenesfolderpath=os. path. dirname(root.filename)
            root.destroy()
               
            
            
        
        
        nextscenetosavenum=nextscenetosavenum+1
        continue
    