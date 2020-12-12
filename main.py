import sqlite3
from datetime import date
from tkinter import *
from PIL import ImageFont, ImageTk, Image
from tmdbv3api import *
import json
import requests
import os
from io import BytesIO
from random import randrange



#settings
background_color = '#131010'

root = Tk()
root.title('bingeWatch')
root.configure(bg = background_color)
root.attributes('-fullscreen', True)
root.resizable(False, False)

def exit_ (root): 
    root.destroy()

 
discover_button = Button(root, text = "Discover", width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
discover_button.place(x = 40, y = root.winfo_screenheight() *  0.25 - 50)

favorite_button = Button(root, text = "Favorite", width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
favorite_button.place(x = 40, y = root.winfo_screenheight() * 0.5 - 50)

exit_button = Button(root, text = "Exit", command = lambda: exit_(root), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
exit_button.place(x = 40, y = root.winfo_screenheight() * 0.75 - 50)

### API

tmdb = TMDb()
tmdb.api_key = 'https://api.themoviedb.org/3/movie/550?api_key=ead60b2309bd3aba9817000af517c069'



def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

### making a request for trending TV's in the last week
### posting them on the home screen

response = requests.get('https://api.themoviedb.org/3/trending/tv/day?api_key=ead60b2309bd3aba9817000af517c069')
json_data = json.loads(response.text)

row_space = 300
photoimage_list = []

if response.status_code != 404:
    for i in range(15):
            id = randrange(0,20)
            name = json_data['results'][id]['name']
            img_url = 'https://image.tmdb.org/t/p/w500' + json_data['results'][id]['poster_path']
            print(name)
            print(img_url)
            print('\n')

            img_data = requests.get(img_url).content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            img = img._PhotoImage__photo.subsample(3)
            photoimage_list.append(img)
            panel = Label(root, image=img)
            
            if i <= 4: 
                panel.place(x = 400 + row_space * i , y = 80)
            elif i > 4 and i <= 9:
                panel.place(x = 400 + row_space * (i - 5) , y = 400)
            elif i >9:
                panel.place(x = 400 + row_space * (i - 10) , y = 725)
            
        

root.mainloop()

#conn = sqlite3.connect('movies.db')

#c = conn.cursor()

# created tabel
#c.execute(""" CREATE TABLE movies(
 #   name VARCHAR(255) NOT NULL,
 #  link VARCHAR(255) NOT NULL,
 #   last_season INTEGER,
 #   last_episode INTEGER,
 #   user_season INTEGER,
 #   user_episode INTEGER,
 #   last_watch DATETIME,
 #   score DECIMAL(3,2),
 #   trailer_link VARCHAR(255)
#) 
#    """)

#conn.commit()
#today = date.today()
#print("1. add")
#action = int(input())
#if action==1:
#    print("add movie name")
#    name = input()
#    print("add imdb link")
#    link = input()

#c.execute(""" INSERT INTO movies VALUES

#    (?, ?, 0, 0 , 0, 0, ?, 3.23, 'link')

#""", (name, link, today))
#conn.commit()

#c.execute("SELECT * FROM movies")
#print(c.fetchall())
