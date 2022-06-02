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
    print("This code creates story structures from synopses")
    print("in several common forms")
    print("\n\n")
    print("1 Break story down as 'Hero's Journey'")
    print( "2 Break story down as 'Save The Cat' beatsheet")
    print( "3 Break story down as '3 act structure'")
    
    which=input("select 1,2 or 3: ")
    if which=="1":
        prompt="Break the above synopsis down using the 'Hero's Journey' method \nORDINARY WORLD:"
    if which=="2":    
        prompt="Break the above synopsis down as a 'Save The Cat' beatsheet \nOPENING IMAGE:"  
    if which=="3":   
        prompt="Break the above synopsis down using the 'Three act Structure' method \nACT I \nSETUP:"
        
        
    root = Tk()
    root.filename =  askopenfilename(initialdir = "/",title = "Select synopsis file",filetypes = (("text files","*.txt"),("all files","*.*")))
    #print (root.filename)
    voicestyle=""
    with open(root.filename, "r",encoding="utf8") as f:
              synopsis = f.read()
              name=os.path.basename(root.filename)
              folderpath=os. path. dirname(root.filename)
              root.destroy()
    #get thenumber of the file
    print("synopsis name"+name)
    #print(scenename[-4:-7])
    


    scriptprompt="SYNOPSIS:\n"+synopsis+prompt    
    print("QUERYING GPT3_____________________________________")
    completion="frogspawn"
    #print(scriptprompt)
    completion = gpt3_completion(scriptprompt)
    completion = completion.replace(r'\n', '\n')
    if which=="1":
        completion="ORDINARY WORLD:"+completion
    if which=="2":
        completion="OPENING IMAGE:"+completion
    if which=="3":
        completion="ACT I \nSETUP:"+completion
    print(completion)
    print("1 Accept and save")
    print("2 quit")
    goy=input("1,2: ")
    if goy=="2":
        quit()
    elif goy=="1":
        root = Tk()
        root.filename =  asksaveasfilename(initialdir = "/",title = "Save breakdown",filetypes = (("text files","*.txt"),("all files","*.*")))
        print (root.filename)
                        
        with open(root.filename+".TXT", "w", encoding='utf-8') as f:
           f.write(completion)  # write some data to the file               
           root.mainloop()
        root.destroy()
        
    
    
        
        