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
from PIL import UnidentifiedImageError
import webbrowser
import api

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
#    score FLOAT,
#    trailer_link VARCHAR(255),
#    image_link VARCHAR(255),
#    finished BIT,
#    snoozed BIT
# ) 
#    """)

conn.commit()

#settings
background_color = '#131010'

root = Tk()
root.configure(bg = background_color)
root.attributes('-fullscreen', True)




#placing the aside buttons
search_button = Button(root, text = "Search", command = lambda: searchWindow(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
search_button.place(x = 40, y = root.winfo_screenheight() *  0.10  - 50)

discover_button = Button(root, text = "Trending", command = lambda: home_page(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
discover_button.place(x = 40, y = root.winfo_screenheight() *  0.30 - 50)

favorite_button = Button(root, text = "Favorites", command = lambda: favorites(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
favorite_button.place(x = 40, y = root.winfo_screenheight() * 0.50 - 50)

collection_button = Button(root, text = "Collection", command = lambda: show_collection(), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000" )
collection_button.place(x = 40, y = root.winfo_screenheight() * 0.70 - 50)

exit_button = Button(root, text = "Exit", command = lambda: exit_(root), width = 20, height = 5, bg = '#000000', fg = '#FFCB09', font = 'sans-serif', activebackground = '#FFCB09', activeforeground = "#000000")
exit_button.place(x = 40, y = root.winfo_screenheight() * 0.90 - 50)

def jprint(obj):
    # created a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

### making a request for trending TV's in the last week
### posting them on the home screen

api_key_code = api.api_key()
print(api_key_code)

response = requests.get('https://api.themoviedb.org/3/trending/tv/day?api_key=' + api_key_code)
json_data = json.loads(response.text)

row_space = 300
photoimage_list = []

def searchResults(obj, widget1, widget2, widget3):
    """ this will be called when the user submits the search query """
    for widget in root.winfo_children():
        if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != widget1 and widget != widget2 and widget != widget3 and widget != collection_button:
            widget.destroy()
    photoimage_list.clear()
    name = []
    fav_buttons= []
    show_name = obj.get()
    response = requests.get("https://api.themoviedb.org/3/search/tv?api_key=ead60b2309bd3aba9817000af517c069&language=en-US&page=1&query=" + show_name + "&include_adult=false")
    json_data = json.loads(response.text)
    #displaying first 10 results
    if int(json_data['total_results']) > 10:
        displayedResults = 10
    else:
        displayedResults = int(json_data['total_results'])

    for index in range(0,displayedResults):
        name.append(json_data['results'][index]['name'])
        img_url = 'https://image.tmdb.org/t/p/w500' + str(json_data['results'][index]['poster_path'])
        try:
            img_data = requests.get(img_url).content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            img = img._PhotoImage__photo.subsample(3)
            if img != 'https://image.tmdb.org/t/p/w500None':
                photoimage_list.append(img)
        
        except UnidentifiedImageError:
            print(img_url)

        panel = Label(root, image=img)
        
        if index < 5:
            panel.place(x = 350 + row_space * index , y = 250)
            fav_buttons.append(Button(root, command = lambda c = index: add_favorites(json_data, c, name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
            fav_buttons[index].place(x = 380 + row_space * index, y = 520)
        else:
            panel.place(x = 350 + row_space * (index - 5) , y = 600)
            fav_buttons.append(Button(root, command = lambda c = index: add_favorites(json_data, c,name[c]), text = "Add to Favorites", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
            fav_buttons[index].place(x = 380 + row_space * (index-5), y = 870)

    for pic in photoimage_list:
        print(pic)

def searchWindow():
    """ this function will display the search window, where the user can type a tv show and add it to favorites"""
    for widget in root.winfo_children():
         if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != collection_button:
            widget.destroy()
    
    text = Label(root, text = 'Type a TV Show: ', font = ('Verdana', 25), bg = '#696969')
    text.place(relx=0.30,rely=0.15, anchor = CENTER)
    input = Entry(root, width = 30, font = ('Verdana', 25), fg = '#696969')
    input.place(relx=0.55, rely=0.15, anchor=CENTER)
    submitButton = Button(root, text="Submit", width=10, command = lambda: searchResults(input, text, input, submitButton), font = ('Verdana', 16), bg = '#696969')
    submitButton.place(relx = 0.76, rely = 0.15, anchor = CENTER)
    
def callback(url):
    webbrowser.open_new(url)

def show_collection():
    """ this function will display all the snoozed shows"""
    for widget in root.winfo_children():
        if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != collection_button:
            widget.destroy()

    c = conn.cursor()
    #selecting the snoozed one first
    c.execute('SELECT * FROM tv_shows WHERE snoozed = 1')
    
    rows = c.fetchall()
    #and then the finished ones
    c.execute('SELECT * FROM tv_shows WHERE finished = 1')
    finished_shows = c.fetchall()
    #storing all of them in rows
    rows = rows + finished_shows
    
    canvas = Canvas(root, width = root.winfo_screenwidth() , height = root.winfo_screenheight() -25, bg = background_color, bd = 0, highlightthickness=0)
    canvas.place(x = 325, y=20)

    scrollbar = Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side='right', fill = 'y')

    def on_configure(event):  
        canvas.configure(scrollregion=canvas.bbox('all'))

    endline = 0
    iterate = 0
    vertical_pos = 0
    unsnooze_buttons = []

    for row in rows:
        #displaying all the shows
        img_data = requests.get(row[10]).content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        img = img._PhotoImage__photo.subsample(3)
        photoimage_list.append(img)

        panel = Label(canvas, image = img)
        #4 on a row
        if(endline > 4):
            vertical_pos = vertical_pos + 340
            endline = 0

        canvas.create_window((30 + row_space * endline,240+ vertical_pos), window = panel, anchor = 'nw')
        if rows[iterate][12] == 1:
            unsnooze_buttons.append(Button(canvas, command = lambda c = iterate : unsnooze(rows[c]), text = 'Unsnooze', bg ='#554014'))
            canvas.create_window((200 + row_space * endline, 240 + vertical_pos), window = unsnooze_buttons[iterate], anchor = 'nw')
        if rows[iterate][11] == 1:
            status = Label(canvas, text = 'Finished', bg ='#D99300')
            canvas.create_window((200 + row_space * endline, 240 + vertical_pos), window = status, anchor = 'nw')

        iterate += 1
        endline += 1


    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', on_configure)

def _show(data, season, episode, flag): 

    """ This will be shown open 'Open show' button will be pressed
        This function will display almost all the data from the DB
    
    """ 

    #as before we remove every widget but those aside
    for widget in root.winfo_children():
         if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != collection_button:
            widget.destroy()

    #displaying the show's title
    title = Label(root, text = data[1], bg = background_color, fg = '#FFCB09', font = ('sans-serif', 40), highlightcolor = '#FFF')
    title.pack()

    data_list = list(data)
        
    last_viewed_season = season
    last_viewed_episode = episode + 1

    time_date = data[7]

    if flag:
        time_date = str(date.today())

    #updating the data in the db
    c = conn.cursor()
    c.execute(""" UPDATE tv_shows SET user_season = ?, user_episode = ?, last_watch = ? WHERE id LIKE ? """, (int(season), int(episode), time_date, data[0]))    
    data_list[5] = season
    data_list[6] = episode
    data_list[7] = str(time_date)
  
    data = tuple(data_list)
    conn.commit()
    c.close()

    #displaying the poster of the show
    img_url = data[10]
    img_data = requests.get(img_url).content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    img = img._PhotoImage__photo.subsample(2)
    photoimage_list.append(img)
    panel = Label(root, image = img)
    panel.place(x = 840, y = 110)

    show_length = Label(root, text = 'Seasons: {}  Episodes: {}'.format(data[3], data[4]))
    show_length.place(x = 900, y  = 500)

    #mark episode as watched 
    if last_viewed_episode == int(data[4]) + 1:
        last_viewed_season = season + 1
        last_viewed_episode = 1
    
    if season == int(data[3]) and episode == int(data[4]):
        #checking if the user finished the show
        mark_button = Button(root, text = "You've finished the show", command = lambda: favorites(), width = 28, height = 3, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 12), activebackground = '#FFCB09', activeforeground = "#000000")
        c = conn.cursor()
        #if so the show will be updated as finished in the db and will no longer appear in this window
        c.execute(""" UPDATE tv_shows SET finished = 1 WHERE id LIKE ? """, (data[0],))
        conn.commit()
        c.close()  
        mark_button.place(relx = 0.435, y = 540)
        
        last_time_watched =  Label(root, text = 'Last time you watched {} was on {}'.format(data[1], data[7]), font = ('sans-serif', 12) )
        last_time_watched.configure(anchor = CENTER)
        last_time_watched.pack()
    else:
        mark_button = Button(root, text = "Next: Episode {} of Season {}".format(last_viewed_episode, last_viewed_season), command = lambda: _show(data, last_viewed_season, last_viewed_episode, flag = True), width = 28, height = 3, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 12), activebackground = '#FFCB09', activeforeground = "#000000")
        mark_button.place(relx = 0.435, y = 540)

    if last_viewed_episode > 1:
        current_episode =  Label(root, text = """ You're currently at Episode: {} Season: {} """.format(data[6], data[5]), font = ('sans-serif', 12) )
        current_episode.configure(anchor = CENTER)
        current_episode.pack()

        last_time_watched =  Label(root, text = 'Last time you watched {} was on {}'.format(data[1], data[7]), font = ('sans-serif', 12) )
        last_time_watched.configure(anchor = CENTER)
        last_time_watched.pack()

    #placing the hyperlink button that will redirect to the trailer of the show
    hyperlinkTrailer = Label(root, text = 'Trailer', bg ='#FF0000', fg = '#FFFFFF', font = ('sans-serif', 15, 'bold'), padx = 12, pady = 6)
    hyperlinkTrailer.place(relx = 0.45, y = 640)
    hyperlinkTrailer.bind('<Button-1>', lambda e: callback(data[9]))

    #placing the hyperlink button that will redirect to TMDB show's page
    hyperlinkTMDB = Label(root, text = 'TMDB', bg ='#01b4e4', fg = '#FFFFFF', font = ('sans-serif', 15, 'bold'), padx = 12, pady = 6)
    hyperlinkTMDB.place(relx = 0.51, y = 640)
    hyperlinkTMDB.bind('<Button-1>', lambda e: callback(data[2] + '/season/' + str(data[5]) + '/episode/' + str(data[6])))

    def update_score(id, rating, widget):
        """ updating the score """
        widget.destroy()
        
        c = conn.cursor()
        c.execute(""" SELECT score from tv_shows WHERE id LIKE ? """, (id,))
        conn.commit()
        string =''.join(str(x) for x in c.fetchall())
        score = float(string[1] + string[2] + string[3])
        
        if score != 0.0:
            updated_score = (score + int(rating)) / 2
        else:
            updated_score = (score + int(rating))
        c.execute(""" UPDATE tv_shows SET score = ? WHERE id LIKE ? """, (updated_score, id))

        conn.commit()
        c.close()
        score_box = Label(root, text = updated_score, bg = '#E09500', font = ('Verdana', 32, 'bold'), width = 5, pady = 15)
        score_box.place(x = 1720, y= 0)
   
    #placing input box for the score
    rating = Entry(root, width = 5, font = ('Verdana', 16), fg = '#696969')
    rating.place(x = 910, y = 720)

    submitButton = Button(root, text="Rate", command =  lambda: update_score(data[0],rating.get(), score_box) , width=5, font = ('Verdana', 10), bg = '#696969')
    submitButton.place(x = 985,y = 720)
    
    c = conn.cursor()
    c.execute(""" SELECT score from tv_shows WHERE id LIKE ? """, (data[0],))
    string = ''.join(str(x) for x in c.fetchall())
    score = float(string[1] + string[2] + string[3])
    
    score_box = Label(root, text = score, bg = '#E09500', font = ('Verdana', 32, 'bold'), pady = 15, width = 5)
    score_box.place(x = 1720, y= 0)

    c.close()

def add_favorites(obj, id, name):
    """ This will be called when "Add to favorites" button is pressed """
    #requesting the trailer link from youtube API
    results = SearchVideos(name + ' Official Trailer', offset = 1, mode = "dict", max_results = 1).result()
    trailer_link = results['search_result'][0]['link']
    tv_index = str(obj['results'][id]['id'])
    tmdb_link = "https://www.themoviedb.org/tv/"+tv_index
    img_url = 'https://image.tmdb.org/t/p/w500' + obj['results'][id]['poster_path']

    #requesting the episode post from the API
    response = requests.get("https://api.themoviedb.org/3/tv/"+ tv_index +"?api_key=ead60b2309bd3aba9817000af517c069&language=en-US")
    json_tv_data = json.loads(response.text)
    
    print(json_tv_data['last_episode_to_air']['season_number'])
    last_season_to_air = json_tv_data['last_episode_to_air']['season_number']
    last_episode_to_air = json_tv_data['last_episode_to_air']['episode_number']
    #inserting all the data from json to the database
    c.execute(""" INSERT OR IGNORE INTO tv_shows VALUES
        (?, ?, ?, ?, ?, 1, 0, NULL, 0, ?, ?, False, 0)

    """, (tv_index, name, tmdb_link, last_season_to_air, last_episode_to_air, trailer_link, img_url))
    conn.commit()

    c.execute("SELECT * FROM tv_shows")
    print(c.fetchall())
    print('\n')
    c.close()

def snooze(data):
    """ snoozing a show """
    c = conn.cursor()
    c.execute("UPDATE tv_shows SET snoozed = 1 where id = ?", (data[0],))
    conn.commit()
    c.close()
    favorites()

def unsnooze(data):
    """ unsnoozing a show """
    c = conn.cursor()
    c.execute("UPDATE tv_shows SET snoozed = 0 where id = ?", (data[0],))
    conn.commit()
    c.close()
    show_collection()

def favorites():
    """ This function will display all favorites titles added by the user"""
    for widget in root.winfo_children():
        #first we remove anything but the 4 buttons aside
         if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != collection_button:
            widget.destroy()


    def on_configure(event):
        """ scolling the canvas on event"""  
        canvas.configure(scrollregion=canvas.bbox('all'))


    c = conn.cursor()
    #fetching from the DB all the active tv shows: that are not finished nor snoozed
    row = c.execute("select * from tv_shows where finished = 0 and snoozed = 0 order by score desc")
    rows = c.fetchall()
    endline = 0
    photoimage_list.clear() 
    vertical_pos = 0
    open_buttons = []
    snooze_buttons = []
    
    #creating a canvas so we can scroll
    canvas = Canvas(root, width = root.winfo_screenwidth() , height = root.winfo_screenheight() -25, bg = background_color, bd = 0, highlightthickness=0)
    canvas.place(x = 325, y=20)

    scrollbar = Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side='right', fill = 'y')
   
    iterate = 0
    #adding all the favorite titles to the canvas 
    for row in rows:    
        img_url = row[10]
        img_data = requests.get(img_url).content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        img = img._PhotoImage__photo.subsample(3)
        photoimage_list.append(img)

        panel = Label(canvas, image = img)
        #4 titles per row
        if(endline > 4):
            vertical_pos = vertical_pos + 340
            endline = 0

        canvas.create_window((30 + row_space * endline,240+ vertical_pos), window = panel, anchor = 'nw')

        #placing the corresponding buttons
        open_buttons.append(Button(canvas, command = lambda c = iterate: _show(rows[c], rows[c][5], rows[c][6], flag = False), text = "Open Show", width = 13, height = 2, bg = '#000000', fg = '#FFCB09', font = ('sans-serif', 10) , activebackground = '#FFCB09', activeforeground = "#000000" ))
        canvas.create_window((60 + row_space * endline, 515 + vertical_pos), window = open_buttons[iterate], anchor = 'nw')  

        snooze_buttons.append(Button(canvas, command = lambda c = iterate : snooze(rows[c]), text = 'Snooze', bg ='#554014'))
        canvas.create_window((200 + row_space * endline, 240 + vertical_pos), window = snooze_buttons[iterate], anchor = 'nw')

        iterate += 1
        endline += 1


    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', on_configure)

    c.close()

def home_page():
    """ Placing all the widgets on the home screen."""
    fav_buttons = []
    name = []
    for widget in root.winfo_children():
        if widget != discover_button and widget != favorite_button and widget != exit_button and widget != search_button and widget != collection_button:
            widget.destroy()
    #choosing 15 title's from the trending request
    for i in range(15):
            
            name.append(json_data['results'][i]['name'])
            img_url = 'https://image.tmdb.org/t/p/w500' + json_data['results'][i]['poster_path']
            print(name[i])
            print(img_url)
            print('\n')

            #requesting from API the title's poster
            img_data = requests.get(img_url).content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            img = img._PhotoImage__photo.subsample(3)
            photoimage_list.append(img)
            panel = Label(root, image=img)

            #placing the "Add to favorites" button for every title
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
    
def exit_ (root):
    root.destroy()
root.mainloop()
