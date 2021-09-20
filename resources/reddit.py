import pandas as pd
import numpy as np
import praw

import cv2
import requests

from tkinter import *
from tkinter.ttk import *
from PIL import Image as PILIMAGE
import os
from pathlib import Path

class Reddit:

    def __init__(self, client_ID, client_secret):
        
        self.reddit = praw.Reddit(
            client_id=client_ID,
            client_secret=client_secret,
            user_agent='cor',
            username=None,
            password=None
        )
        self.index = 0

        
        

        
    def getSubreddit(self, csvFile):
        
        self.subreddits = []
        f_final = open(csvFile, "r")
        
        for line in f_final:
            sub = line.strip()
            self.subreddits.append(sub)

    def run(self, N, path):
        print(path)
        self.downloadImage(N, path)
        

    def downloadImage(self, N, path):

        ignoreImages = [cv2.imread("resources/ignoreImages/imageNF.png"), cv2.imread("resources/ignoreImages/DeletedIMG.png")]
        
        for subreddit in self.subreddits:
            if not os.path.exists(f"{path}/{subreddit}"):
                os.makedirs(f"{path}/{subreddit}")
        
            
            subreddit = self.reddit.subreddit(subreddit)
            i = 0
            for submission in subreddit.new(limit=int(N)):
                
                
                #
                # 
                # self.progress['value'] += self.progress['value']
                
                if "jpg" in submission.url.lower() or "png" in submission.url.lower():
                    
                     
                    resp = requests.get(submission.url.lower(), stream=True).raw
                    image = np.asarray(bytearray(resp.read()), dtype='uint8')
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                    

                    # Compare with ignore Image
                    ignoreERROR = False

                    compare_image = cv2.resize(image, (224, 224))
                    for ignore in ignoreImages:
                        
                        diff = cv2.subtract(ignore, compare_image)
                        b_ch, g_ch ,r_ch = cv2.split(diff)
                        tdiff = cv2.countNonZero(b_ch) + cv2.countNonZero(g_ch) + cv2.countNonZero(r_ch)
                        
                        # Image has to be ignore
                        if tdiff == 0:
                            ignoreERROR = True
                    
                    if not ignoreERROR:
                        
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        img = PILIMAGE.fromarray(image)
                        img.save(f"{path}/{subreddit}/{i}.png")
                        print(f"saved --> {path}/{subreddit}/{i}.png")
                        i += 1
                    
                    


            

            
        

    

        




