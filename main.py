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
from youtubesearchpython import SearchVideos


#connecting to database

conn = sqlite3.connect('shows.db')
c = conn.cursor()

#created tabel
# c.execute(""" CREATE TABLE tv_shows(
#    id VARCHAR(255) UNIQUE,
#    name VARCHAR(255) UNIQUE,
#    link VARCHAR(255) NOT NULL,
#    last_season INTEGER,
#    last_episode INTEGER,
#    user_season INTEGER,
#    user_episode INTEGER,
#    last_watch DATETIME,
#    score DECIMAL(3,2),
#    trailer_link VARCHAR(255),
#    image_link VARCHAR(255)
# ) 
#    """)

conn.commit()

#settings
background_color = '#131010'

root = Tk()
root.title('bingeWatch')
root.configure(bg = background_color)
root.attributes('-fullscreen', True)
#root.resizable(False, False)


def exit_ (root): 
    root.destroy()

discover_button = Button(root, text = "Discover", command = lambda: home_page(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
discover_button.place(x = 40, y = root.winfo_screenheight() *  0.25 - 50)

favorite_button = Button(root, text = "Favorite", command = lambda: favorites(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
favorite_button.place(x = 40, y = root.winfo_screenheight() * 0.5 - 50)

exit_button = Button(root, text = "Exit", command = lambda: exit_(root), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000")
exit_button.place(x = 40, y = root.winfo_screenheight() * 0.75 - 50)

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
name = []
                
def add_favorites(obj, id, name):
    #today = date.today()
    results = SearchVideos(name + ' Official Trailer', offset = 1, mode = "dict", max_results = 1).result()
    trailer_link = results['search_result'][0]['link']
    tv_index = str(obj['results'][id]['id'])
    imdb_link = "https://www.imdb.com/title/tt"+tv_index+"/?ref_=nv_sr_srsg_0"
    img_url = 'https://image.tmdb.org/t/p/w500' + obj['results'][id]['poster_path']

    response = requests.get("https://api.themoviedb.org/3/tv/"+ tv_index +"?api_key=ead60b2309bd3aba9817000af517c069&language=en-US")
    json_tv_data = json.loads(response.text)
    
    last_season_to_air = json_tv_data['last_episode_to_air']['season_number']
    last_episode_to_air = json_tv_data['last_episode_to_air']['episode_number']

    c.execute(""" INSERT OR IGNORE INTO tv_shows VALUES
        (?, ?, ?, ?, ?, 0, 0, NULL, NULL, ?, ?)

    """, (tv_index, name, imdb_link, last_season_to_air, last_episode_to_air, trailer_link, img_url))
    conn.commit()

    c.execute("SELECT * FROM tv_shows")
    print(c.fetchall())
    print('\n')
    

def _show(data):
    print('ai deschis: {}'.format(data[1]))



def favorites():
    for widget in root.winfo_children():
         if widget != discover_button and widget != favorite_button and widget != exit_button:
            widget.destroy()


    def on_configure(event):  
        canvas.configure(scrollregion=canvas.bbox('all'))


    c = conn.cursor()
    row = c.execute("select * from tv_shows")
    rows = c.fetchall()
    endline = 0
    photoimage_list.clear() 
    vertical_pos = 0
    open_buttons = []
    

    canvas = Canvas(root, width = root.winfo_screenwidth() , height = root.winfo_screenheight() -25, bg = background_color, bd = 0, highlightthickness=0)
    canvas.place(x = 300, y=20)

    scrollbar = Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side='right', fill = 'y')
   
    iterate = 0

    for row in rows:
       

        img_url = row[10]
        img_data = requests.get(img_url).content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        img = img._PhotoImage__photo.subsample(3)
        photoimage_list.append(img)

        panel = Label(canvas, image = img)
        
        if(endline > 4):
            vertical_pos = vertical_pos + 340
            endline = 0
        #print('button for {}' .format(row[1]))
        canvas.create_window((20 + row_space * endline,230+ vertical_pos), window = panel, anchor = 'nw')
        open_buttons.append(Button(canvas, command = lambda c = iterate: _show(rows[c]), text = "Open Show", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
        canvas.create_window((50 + row_space * endline, 505 + vertical_pos), window = open_buttons[iterate], anchor = 'nw')
        
        iterate += 1
        
        #panel.place(x = 20 + row_space * endline , y = 250 + vertical_pos)
        endline += 1

    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', on_configure)

    c.close()


def home_page():
    fav_buttons = []
    for widget in root.winfo_children():
        if widget != discover_button and widget != favorite_button and widget != exit_button:
            widget.destroy()

    for i in range(15):
            
            name.append(json_data['results'][i]['name'])
            img_url = 'https://image.tmdb.org/t/p/w500' + json_data['results'][i]['poster_path']
            print(name[i])
            print(img_url)
            print('\n')

            img_data = requests.get(img_url).content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            img = img._PhotoImage__photo.subsample(3)
            photoimage_list.append(img)
            panel = Label(root, image=img)
            
            if i <= 4:  
                panel.place(x = 300 + row_space * i , y = 80)
                fav_buttons.append(Button(root, command = lambda c = i: add_favorites(json_data, c, name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
                fav_buttons[i].place(x = 330 + row_space * i, y = 345)
            elif i > 4 and i <= 9:
                panel.place(x = 300 + row_space * (i - 5) , y = 400)
                fav_buttons.append(Button(root, command = lambda c = i: add_favorites(json_data, c,name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
                fav_buttons[i].place(x = 330 + row_space * (i-5), y = 665)
            elif i >9:
                panel.place(x = 300 + row_space * (i - 10) , y = 725)
                fav_buttons.append(Button(root, command = lambda c = i: add_favorites(json_data, c, name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
                fav_buttons[i].place(x = 330 + row_space * (i-10), y = 990)
           

if response.status_code != 404:
    home_page()
    
            

root.mainloop()




