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
#    last_watch VARCHAR(255),
#    score DECIMAL(3,2),
#    trailer_link VARCHAR(255),
#    image_link VARCHAR(255)
# ) 
#    """)

conn.commit()

#settings
background_color = '#131010'

root = Tk()
root.configure(bg = background_color)
root.attributes('-fullscreen', True)
#root.resizable(False, False)


def exit_ (root): 
    root.destroy()

search_button = Button(root, text = "Search", command = lambda: searchWindow(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
search_button.place(x = 40, y = root.winfo_screenheight() *  0.20  - 50)

discover_button = Button(root, text = "Discover", command = lambda: home_page(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
discover_button.place(x = 40, y = root.winfo_screenheight() *  0.40 - 50)

favorite_button = Button(root, text = "Favorite", command = lambda: favorites(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
favorite_button.place(x = 40, y = root.winfo_screenheight() * 0.60 - 50)

exit_button = Button(root, text = "Exit", command = lambda: exit_(root), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000")
exit_button.place(x = 40, y = root.winfo_screenheight() * 0.80 - 50)

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



def searchResults(obj, widget1, widget2, widget3):
    for widget in root.winfo_children():
        if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != widget1 and widget != widget2 and widget != widget3:
            widget.destroy()
    name = []
    fav_buttons= []
    show_name = obj.get()
    response = requests.get("https://api.themoviedb.org/3/search/tv?api_key=ead60b2309bd3aba9817000af517c069&language=en-US&page=1&query=" + show_name + "&include_adult=false")
    json_data = json.loads(response.text)
    
    if int(json_data['total_results']) > 10:
        displayedResults = 10
    else:
        displayedResults = int(json_data['total_results'])

    for index in range(0,displayedResults):
        name.append(json_data['results'][index]['name'])
        img_url = 'https://image.tmdb.org/t/p/w500' + str(json_data['results'][index]['poster_path'])
        debut = str(json_data['results'][index]['first_air_date'])
        
        img_data = requests.get(img_url).content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        img = img._PhotoImage__photo.subsample(3)
        photoimage_list.append(img)
        panel = Label(root, image=img)
        
        if index < 5:  
            panel.place(x = 350 + row_space * index , y = 250)
            fav_buttons.append(Button(root, command = lambda c = index: add_favorites(json_data, c, name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
            fav_buttons[index].place(x = 380 + row_space * index, y = 520)
        else:
            panel.place(x = 350 + row_space * (index - 5) , y = 600)
            fav_buttons.append(Button(root, command = lambda c = index: add_favorites(json_data, c,name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
            fav_buttons[index].place(x = 380 + row_space * (index-5), y = 870)



def searchWindow():
    print('search')
    for widget in root.winfo_children():
         if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button:
            widget.destroy()
    text = Label(root, text = 'Type a TV Show: ', font = ('Verdana', 25), bg = '#696969')
    text.place(relx=0.30,rely=0.15, anchor = CENTER)
    input = Entry(root, width = 30, font = ('Verdana', 25), fg = '#696969')
    input.place(relx=0.55, rely=0.15, anchor=CENTER)
    submitButton = Button(root, text="Submit", width=10, command = lambda: searchResults(input, text, input, submitButton), font = ('Verdana', 16), bg = '#696969')
    submitButton.place(relx = 0.76, rely = 0.15, anchor = CENTER)


def add_favorites(obj, id, name):
    
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
        (?, ?, ?, ?, ?, 1, 0, NULL, NULL, ?, ?)

    """, (tv_index, name, imdb_link, last_season_to_air, last_episode_to_air, trailer_link, img_url))
    conn.commit()

    c.execute("SELECT * FROM tv_shows")
    print(c.fetchall())
    print('\n')
    

def _show(data, season, episode):  
    
    for widget in root.winfo_children():
         if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button:
            widget.destroy()

    title = Label(root, text = data[1], bg = background_color, fg = '#FFCB09', font = ('sans-serif', 40), highlightcolor = '#FFF')
    title.pack()

    data_list = list(data)
        
    last_viewed_season = season
    last_viewed_episode = episode + 1

    time_date = data[7]

    if episode != 0:
        time_date = str(date.today())

    c = conn.cursor()
    c.execute(""" UPDATE tv_shows SET user_season = ?, user_episode = ?, last_watch = ? WHERE id LIKE ? """, (int(season), int(episode), time_date, data[0]))    
    data_list[5] = season
    data_list[6] = episode
    data_list[7] = str(time_date)
  
    data = tuple(data_list)
    conn.commit()
    c.close()


    img_url = data[10]
    img_data = requests.get(img_url).content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    img = img._PhotoImage__photo.subsample(2)
    photoimage_list.append(img)
    panel = Label(root, image = img)
    panel.place(x = 840, y = 80)
    show_length = Label(root, text = 'Seasons: {}  Episodes: {}'.format(data[3], data[4]))
    show_length.place(x = 900, y  = 470)


    if last_viewed_episode == int(data[4]) + 1:
        last_viewed_season = season + 1
        last_viewed_episode = 1

    if season == int(data[3]) and episode == int(data[4]):
        mark_button = Button(root, text = "You've finished the show", command = lambda: favorites(), width = 28, height = 3, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 12), activebackground = '#FFCB09', activeforeground = "#000000")
        mark_button.place(x = 835, y = 500)
    else:
        mark_button = Button(root, text = "I've seen Episode {} of Season {}".format(last_viewed_episode, last_viewed_season), command = lambda: _show(data, last_viewed_season, last_viewed_episode), width = 28, height = 3, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 12), activebackground = '#FFCB09', activeforeground = "#000000")
        mark_button.place(x = 835, y = 500)
    
    if last_viewed_episode > 1  and last_viewed_season == 1:
        last_time_watched =  Label(root, text = 'Last time you watched {} was on {}'.format(data[1], data[7]))
        last_time_watched.place(x = 800, y = 580)


    c.close()
def favorites():
    for widget in root.winfo_children():
         if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button:
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
    canvas.place(x = 325, y=20)

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

        canvas.create_window((30 + row_space * endline,240+ vertical_pos), window = panel, anchor = 'nw')
        open_buttons.append(Button(canvas, command = lambda c = iterate: _show(rows[c], rows[c][5], rows[c][6]), text = "Open Show", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
        canvas.create_window((60 + row_space * endline, 515 + vertical_pos), window = open_buttons[iterate], anchor = 'nw')  
        iterate += 1
        endline += 1

    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', on_configure)

    c.close()


def home_page():
    fav_buttons = []
    name = []
    for widget in root.winfo_children():
        if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button:
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
                panel.place(x = 320 + row_space * i , y = 80)
                fav_buttons.append(Button(root, command = lambda c = i: add_favorites(json_data, c, name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
                fav_buttons[i].place(x = 350 + row_space * i, y = 345)
            elif i > 4 and i <= 9:
                panel.place(x = 320 + row_space * (i - 5) , y = 400)
                fav_buttons.append(Button(root, command = lambda c = i: add_favorites(json_data, c,name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
                fav_buttons[i].place(x = 350 + row_space * (i-5), y = 665)
            elif i > 9:
                panel.place(x = 320 + row_space * (i - 10) , y = 725)
                fav_buttons.append(Button(root, command = lambda c = i: add_favorites(json_data, c, name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
                fav_buttons[i].place(x = 350 + row_space * (i-10), y = 990)
           

if response.status_code != 404:
    home_page()
    
            

root.mainloop()




