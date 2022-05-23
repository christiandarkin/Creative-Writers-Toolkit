import os
import openai
from time import time,sleep
import re

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def gpt3_completion(prompt, engine='text-davinci-002', temp=1.1, top_p=1.0, tokens=500, freq_pen=0.5, pres_pen=0.0, stop=['asdfasdf']):
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
 
    for i in range(20):
        #load the prompt file
        folder = "planprompts/"
        filename = "prompt01.txt"
        filepath = os.path.join(folder, filename)
        with open(filepath, "r") as f:
            prompt = f.read()
       #load prompt2
        filepath = os.path.join(folder, "prompt02.txt")
        with open(filepath, "r") as f:
            prompt2 = f.read()
        filepath = os.path.join(folder, "prompt03.txt")
        with open(filepath, "r") as f:
            prompt3 = f.read()
            #call gpt3
            completion1 = gpt3_completion(prompt)
            #save the file in background
            folder = "background/"
            filename = "character" + str(i) + ".txt"
            filepath = os.path.join(folder, filename)
        with open(filepath, "w") as f:
                f.write(completion1)
                print (completion1)
            
        #generate a synopsis
        synopsisprompt = prompt2.replace('<<COMPLETION1>>', completion1)
        
        #call gpt3
        completion2 = gpt3_completion(synopsisprompt)
        #save the file in background
        folder = "background/"
        filename = "synopsis" + str(i) + ".txt"
        filepath = os.path.join(folder, filename)
        with open(filepath, "w") as f:
                f.write(completion2)
                print (completion2)
                
        #create an antagonist
        antagonistprompt = prompt3.replace('<<COMPLETION1>>', completion1).replace('<<COMPLETION2>>', completion2)
        #print ("@@@@@@@@" ,antagonistprompt)
        #call gpt3
        completion3 = gpt3_completion(antagonistprompt)
        #save the file in background
        folder = "background/"
        filename = "antagonist" + str(i) + ".txt"
        filepath = os.path.join(folder, filename)
        with open(filepath, "w") as f:
                f.write(completion3)
                print (completion3)
        
    

        #exit(0)


        