#!/usr/bin/env python
# coding: utf-8

# In[341]:


import pandas as pd
import requests
import bs4
from decimal import Decimal


# In[180]:


response = requests.get('https://steamspy.com/')
response.encoding ='utf-8'


# In[181]:


response.status_code


# In[182]:


response.headers


# In[183]:


# Parsing document response using BeautifulSoup class
soup = bs4.BeautifulSoup(response.text, 'html.parser')

print(soup.title.text)


# In[184]:


# Checking the html document to know where to get the data from
soup


# In[243]:


# Parent container from which we'll get the data
result_set = soup.select('tbody')


# The hompage shows 3 tables of games with almost the same columns (except for the first table)
# 
# The first group contains the games trending on Steam. The second group shows games recently released on Steam. And the third group is under the title "Top 100 games in the last 2 weeks by total time spent", although the table has 384 rows (games).  
# 
# I'll start by making a table for each group.

# In[319]:


# Container for each game on the first list
result_set[2].select('tr')


# The contents for the first set are like this:  
# 1. Index
# 2. Title, image and link to a detailed view of the game (including game id).
# 3. Release date
# 4. Price
# 5. Score rank
# 6. Owners

# In[315]:


set_1 = result_set[0].select('tr')
set_2 = result_set[1].select('tr')
set_3 = result_set[2].select('tr')


# In[263]:


# Structure of each container
set_1[0].select('td')


# In[305]:


# Creating empty lists that will become dataframe columns
index = []
title = []
game_id = []
game_url = []
img_url = []
release_date = []
price = []
score_rank = []
owners = []


for i in range(len(set_1)):
    data = set_1[i].select('td')
    
    index.append(int(data[0].text))
    title.append(data[1]['data-order'])
    game_id.append(data[1].select('a')[0]['href'].split('/')[2])
    game_url.append('https://steamspy.com' + data[1].select('a')[0]['href'])
    img_url.append(data[1].select('img')[0]['src'])
    release_date.append(data[2]['data-order'])
    price.append(data[3].text.replace('$', ''))
    score_rank.append(data[4].text)
    owners.append(data[5].text)


# In[311]:


# Creating dataframe for set 1
dataframe_1 = pd.DataFrame(zip(index, title, game_id, game_url, img_url, release_date, price, score_rank, owners),
                          columns=['index', 'title', 'game_id', 'game_url', 'img_url', 'release_date', 'price', 'score_rank', 'owners'])


# In[312]:


dataframe_1


# We're good to go with the first dataset. Now let's get the second set.

# In[317]:


# Structure of each container
set_2[0].select('td')


# These are the contents of every container of the second set:
# 
# 1. Index
# 2. Title, image url and link to a detailed view of the game (including game id).
# 3. Release date
# 4. Price
# 5. Score rank
# 6. Owners
# 7. Play time (average and median in parenthesis)
# 
# That is to say, the same content as the first set, except for the field "play time", that at first sight has no values of interest (only zeros).

# In[333]:


# # Exploration
# set_2[0].select('td')[6].text.split(" ")[1].translate({ord('('): None, ord(')'): None})


# In[352]:


# Creating empty lists that will become dataframe columns
index = []
title = []
game_id = []
game_url = []
img_url = []
release_date = []
price = []
score_rank = []
owners = []
play_time_avg = []
play_time_median = []


for i in range(len(set_2)):
    data = set_2[i].select('td')
    
    index.append(int(data[0].text))
    title.append(data[1]['data-order'])
    game_id.append(data[1].select('a')[0]['href'].split('/')[2])
    game_url.append('https://steamspy.com' + data[1].select('a')[0]['href'])
    img_url.append(data[1].select('img')[0]['src'])
    release_date.append(data[2]['data-order'])
    price.append(data[3].text.replace('$', ''))
    score_rank.append(data[4].text)
    owners.append(data[5].text)
    play_time_avg.append(data[6].text.split(" ")[0])
    play_time_median.append(data[6].text.split(" ")[1].translate({ord('('): None, ord(')'): None}))


# In[353]:


# Creating dataframe for set 2
dataframe_2 = pd.DataFrame(zip(index, title, game_id, game_url, img_url, release_date, price,
                               score_rank, owners, play_time_avg, play_time_median),
                           columns=['index', 'title', 'game_id', 'game_url', 'img_url', 'release_date', 'price',
                                    'score_rank', 'owners', 'play_time_avg', 'play_time_median'])


# Now let's get the final set.

# In[339]:


# Structure of each container
set_3[0].select('td')


# The contents are almost the same as the second set, except that now we do have playtime data and also a field with the percentage of owners that actually launched the game in the last two weeks.

# In[354]:


# Creating empty lists that will become dataframe columns
index = []
title = []
game_id = []
game_url = []
img_url = []
release_date = []
price = []
score_rank = []
owners = []
players_launch = []
play_time_avg = []
play_time_median = []


for i in range(len(set_3)):
    data = set_3[i].select('td')
    
    index.append(int(data[0].text))
    title.append(data[1]['data-order'])
    game_id.append(data[1].select('a')[0]['href'].split('/')[2])
    game_url.append('https://steamspy.com' + data[1].select('a')[0]['href'])
    img_url.append(data[1].select('img')[0]['src'])
    release_date.append(data[2]['data-order'])
    price.append(data[3].text.replace('$', ''))
    score_rank.append(data[4].text)
    owners.append(data[5].text)
    players_launch.append(data[6].text)
    play_time_avg.append(data[7].text.split(" ")[0])
    play_time_median.append(data[7].text.split(" ")[1].translate({ord('('): None, ord(')'): None}))


# In[355]:


# Creating dataframe for set 3
dataframe_3 = pd.DataFrame(zip(index, title, game_id, game_url, img_url, release_date, price,
                               score_rank, owners, players_launch, play_time_avg, play_time_median),
                           columns=['index', 'title', 'game_id', 'game_url', 'img_url', 'release_date', 'price',
                                    'score_rank', 'owners', 'players_launch', 'play_time_avg', 'play_time_median'])


# In[356]:


dataframe_3


# ### Individual game page scraping
# 
# Ok, now that we've got our datasets, let's make some more requests enrich the data.  
# We'll make a request for each game's page using the game_url field.

# In[602]:


test_url = dataframe_3.game_url[0]


# In[603]:


response = requests.get(test_url)
response.encoding ='utf-8'


# In[604]:


response.status_code


# In[605]:


# Parsing document response using BeautifulSoup class
soup = bs4.BeautifulSoup(response.text, 'html.parser')

print(soup.title.text)


# In[606]:


soup


# In[563]:


# Data from text page
soup.select('.p-r-30')[0].select('strong')
# soup.select('.p-r-30')[0].find_all('strong', text='Genre:')[0]


# In[597]:


# Data from text page
# soup.select('.p-r-30')[0].select('Strong')
# soup.select('.p-r-30')[0].select('trong')[0].next_sibling.next_sibling
a = soup.select('.p-r-30')[0].find_all('strong', text='Playtime total:')[0].next_sibling
b = a#.next_sibling#.text#next_sibling.text#.next_sibling.next_sibling.text
print(b.text)
print(type(b))
print(b.text=="")
print(isinstance(b,bs4.element.Tag))


# In[599]:


def get_developers(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Developer:')[0].next_sibling
    developer_list = []
    
    while a.text != "Publisher:":
        if isinstance(a, bs4.element.Tag) and a.text != "":
            developer_list.append(a.text)
        
        a = a.next_sibling
    
    return developer_list


def get_publishers(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Publisher:')[0].next_sibling
    publisher_list = []
    
    while a.text != "Genre:":
        if isinstance(a, bs4.element.Tag) and a.text != "":
            publisher_list.append(a.text)
        
        a = a.next_sibling
    
    return publisher_list


def get_genre(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Genre:')[0].next_sibling
    genre_list = []
    
    while a.text != "Languages:":
        if isinstance(a, bs4.element.Tag) and a.text != "":
            genre_list.append(a.text)
        
        a = a.next_sibling
    
    return genre_list


def get_languages(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Languages:')[0].next_sibling
    languages_list = []
    
    while a.text != "Tags:":
        if isinstance(a, bs4.element.Tag) and a.text != "":
            languages_list.append(a.text)
        
        a = a.next_sibling
    
    return languages_list


def get_tags(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Tags:')[0].next_sibling
    tags_list = []
    
    while a.text != "Category:":
        if isinstance(a, bs4.element.Tag) and a.text != "":
            tags_list.append(a.text)
        
        a = a.next_sibling
    
    return tags_list


def get_categories(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Category:')[0].next_sibling
    categories_list = []
    
    while a.text != "":
        if isinstance(a, bs4.element.NavigableString) and a.text != "":
            cat_list = a.text.split(", ")
            cat_list = [i.strip() for i in cat_list]
            
        a = a.next_sibling
    
    return cat_list


def get_followers(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Followers')[0].next_sibling
        
    while isinstance(a, bs4.element.NavigableString):
        if a.text != "":
            followers = a.text
            
        a = a.next_sibling
    
    return followers


def get_peak_players(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Peak concurrent players yesterday')[0].next_sibling
        
    while isinstance(a, bs4.element.NavigableString):
        if a.text != "":
            peak_players = a.text
            
        a = a.next_sibling
    
    return peak_players


def get_youtube_stats(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='YouTube stats')[0].next_sibling
        
    while isinstance(a, bs4.element.NavigableString):
        if a.text != "":
            youtube_stats = a.text
            
        a = a.next_sibling
    
    return youtube_stats


def get_total_playtime(bsoup):
    
    a = bsoup.select('.p-r-30')[0].find_all('strong', text='Playtime total:')[0].next_sibling
        
    while isinstance(a, bs4.element.NavigableString):
        if a.text != "":
            total_playtime = a.text
            
        a = a.next_sibling
    
    return total_playtime


# In[600]:


#from unidecode import unidecode


# In[601]:


get_total_playtime(soup)


# #### Time series
# 
# We can find some time series also in the html document. Curiously enough, at the time of developing this notebook, the front page doesn't show the graphs on Twitch data (which is available through the html scrapping). I remember the graphs were being shown yesterday when I was analyzing the webpage.

# In[631]:


# All charts data
soup.select('.panel-body')[0].find_all("script")


# In[670]:


a = soup.select('.panel-body')[0].find_all("script")[2]

b = a#.next_sibling#.text#next_sibling.text#.next_sibling.next_sibling.text
print(b.text)#.split("[", 1)[1].rsplit("]", 1)[0])
print(type(b))
print(b.text=="")
print(isinstance(b,bs4.element.Tag))


# In[640]:


import json


# In[ ]:


json.loads 


# In[671]:


# Getting a json with data of all 4 charts (PCCU, HCCU, Twitch Daily stats, Twitch Hourly stats)

chart_list = ["pccu", "hccu"]
json_list = []

for i in zip(range(2), chart_list):
    a = soup.select('.panel-body')[0].find_all("script")[i[0]]
    json_list.append(a.text.split("[", 1)[1].rsplit("]", 1)[0].
                     replace("\n","").
                     replace("\r",""))


# In[681]:





# In[ ]:




