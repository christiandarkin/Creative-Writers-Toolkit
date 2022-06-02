# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:12:02 2022

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
import glob

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

if __name__ == '__main__':
    #load the scene list
    print("This code assembles a script from numbered script files.")
    print("You'll need a series of files labeled SCRIPT_SCENE0001. SCRIPT_SCENE0002, etc)")
    getcha= input("choose an initial SCRIPT_SCENE0001 file (y/n):")
    if getcha== "y":
        root = Tk()
        root.filename =  askopenfilename(initialdir = "/",title = "Select Script file",filetypes = (("text files","*.txt"),("all files","*.*")))
        #print (root.filename)
        folderpath=os. path. dirname(root.filename)
        completion7=""
        with open(root.filename, "r") as f:
            completion7 = f.read()
            root.destroy()
    else:
                completion7=""  
    #scenenum= input ("how many scenes are there?")
    #scn=int(scenenum)
    print(folderpath)
    scenes = glob.glob(folderpath+"/SCRIPT_SCENE*")

    scenes.sort()
    print (scenes)

    with open(folderpath+"/full_script.txt", "w") as outfile:
        for f in scenes:
            with open(f) as infile:
                outfile.write(infile.read())
                outfile.write("\n\n\n\n")