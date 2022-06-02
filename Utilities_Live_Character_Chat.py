# -*- coding: utf-8 -*-
"""
Created on Tue May 31 08:33:30 2022

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

def gpt3_completion(prompt, engine='text-davinci-002', temp=1.0, top_p=1.0, tokens=1000, freq_pen=0.5, pres_pen=0.0, stop=['YOU:']):
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
    print("This code allows you to have real conversations")
    print("with the characters from your stories.")
    print("Just load in a chracter description (it may be a good idea to add a line about how the character speaks to the description)")
    print("You can also give a situation for the conversation.")
    print("type 'QUIT' to save your conversation and exit")
    
    print("Load a character (any txt file will do as long as it describes your character")
    getcha=input("hit return:")
    if getcha != "n":
          root = Tk()
          root.filename =  askopenfilename(initialdir = "/",title = "Select character file",filetypes = (("text files","*.txt"),("all files","*.*")))
          #print (root.filename)
          character=""
          charname=""
          charfolderpath=""
          with open(root.filename, "r",encoding="utf8") as f:
              character = f.read()
              charname=os.path.basename(root.filename)
              charfolderpath=os. path. dirname(root.filename)
              root.destroy()
    else:
         quit()
    #remove .txt from character name
    charname="CHARACTER"
    charname=input("Character Name: ")
    
    
    print("Give a situation in which your conversation should take place")
    print("You can say 'I'm a police officer interviewing the character about a murder that took place in their home'")
    print("or 'I'm on a date with the character.  We're both nervous.")
    print("or 'I've been captured by the character's guards and taken to her imperial palace'")
    print("or just hit return to get the default: 'I'm the character's trusted friend and they're happy to talk about anything'")
    situation="I'm the character's trusted friend and they're happy to talk about anything"
    situation=input("Situation: ")
    if situation=="":
        situation="I'm the character's trusted friend and they're happy to talk about anything"
    
    #load in conversation prompt file
    prompt=""
    #load prompts
    folder = "planprompts/"
    filepath = os.path.join(folder, "characterchatprompt.txt")
    with open(filepath, "r", encoding='utf-8') as f:
         prompt = f.read()
    
    
    conversation= prompt.replace('<<CHARACTER>>', character).replace('<<SITUATION>>', situation)  
    print(charname+":\n"+conversation)
    
    while True:
        res=""
        response=input("YOU:")
        if response=="QUIT":
            #save prompt and exit
            root = Tk()
            root.filename =  asksaveasfilename(initialdir = "/",title = "Save conversation",filetypes = (("text files","*.txt"),("all files","*.*")))
            print (root.filename)
                            
            with open(root.filename+".TXT", "w", encoding='utf-8') as f:
               f.write(conversation)  # write some data to the file  
               f.close()
               root.withdraw()
               messagebox.showinfo("File saved", "File has been saved successfully.")
               root.destroy()
               
            
            quit()
            
        elif response !="QUIT":
            res="\n\nYOU:"+response+"\n\n"+charname+":" 
            conversation=conversation+res
            print("\n\n"+charname+":")
            
        
        #print("QUERYING GPT3_____________________________________")
        response="frogspawn"
        #print(scriptprompt)
        response = gpt3_completion(conversation)
        response = response.replace(r'\n', '\n')
        conversation=conversation+response
        print (response)
        continue
        
       
        
        
    
    