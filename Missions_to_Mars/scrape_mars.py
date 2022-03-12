#!/usr/bin/env python
# coding: utf-8

# In[8]:


# Import Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import html5lib
import lxml
from splinter import Browser
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager


        # In[18]:


        # Set the executable path and initialize Splinter

executable_path = {"executable_path": "./chromedriver.exe"}
browser = Browser("chrome", **executable_path)

def scrape():
        # In[13]:

        mars_info_dictionary = dict()
        # NASA Mars News 
        # Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and Paragraph Text. 
        # Assign the text to variables that you can reference later.

        # Visit the Maars News Site provided in the insructions

        url = 'https://redplanetscience.com/'
        browser.visit(url)


        # In[15]:


        # News Title

        # Using Beautiful Soup, the broswer html will be converted to a soup object.Convert the browser html to a soup object.
        # To collect the latest News Title and Paragraph Text. I am going to the site and inspect the onject to get the classes for
        # the title and paragraph. According to inspect process <div class="content_title> is the class
        # Note: Can use soup because that is the name assigned when importing in bs.

        html = browser.html
        soup = bs(html, 'html.parser')
        news_title = soup.find('div', class_='content_title')
        news_title.text


        # In[16]:


        # After locating the headline, referenced the news_title variable and the .text.strip() functions to make the news title
        # regular text without the html markup
        #https://python.hotexamples.com/examples/bs4/BeautifulSoup/strip/python-beautifulsoup-strip-method-examples.html

        news_title = news_title.text.strip()
        #print(news_title)
        mars_info_dictionary['news_titles'] = news_title

        # In[17]:


        #News Paragraph 

        # According to the inspect process <div class="article_teaser_body">

        news_paragraph = soup.find('div', class_='article_teaser_body')
        news_paragraph

        # In[18]:


        # After locating the paragraph, referenced the news_paragraph variable and the .text.strip() functions to make the 
        # paragraph regular text without the html markup
        #https://python.hotexamples.com/examples/bs4/BeautifulSoup/strip/python-beautifulsoup-strip-method-examples.html

        news_paragraph = news_paragraph.text.strip()
        #print(news_paragraph)
        mars_info_dictionary['news_paragraph'] = news_paragraphs
              
        # In[8]:


        # JPL Mars Space Images - Featured Image


        # In[27]:


        # Visit the url for the Featured Space Image site [here](https://spaceimages-mars.com).
        # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the 
        # url string to a variable called `featured_image_url`.
        # Make sure to find the image url to the full size `.jpg` image.
        # Make sure to save a complete url string for this image.

        url_2 = "https://spaceimages-mars.com/"
        browser.visit(url_2)


        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find('img', class_='headerimage fade-in')
        img_link = img['src']

        featured_image_url = url_2 + img_link
        
        mars_info_dictionary ['featured_image'] = featured_image_url 

        # In[11]:


        ###Scrape the table containing facts about diameter of Mars
        #!pip install html5lib

        url_3 = "https://galaxyfacts-mars.com/"


        # In[13]:

        df = pd.read_html(url_3)
        display(df[1])
        mars_df = (df[1])
        mars_df

        # In[ ]:

        # Converting df to html in case it is needed for the flask portion of the exercise
        mars_df.to_html(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None,index_names=True, justify=None, bold_rows=True, classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False)

        mars_info_dictionary['mars_facts'] = mars_df

        # In[50]:


        #Create empty dictionary for results
        hemisphere_image_urls = {}

        #Define the url
        url_4 = "https://marshemispheres.com/"

        #Go to main website
        browser.visit(url_4)

        #Read page as HTML
        html = browser.html

        #Parse HTML
        soup = bs(html, 'html.parser')

        #Find area that represents the list with hemispheres
        nav_list = soup.find('div', class_="collapsible results")

        #From the above area find every item in the list
        all_hemispheres = nav_list.find_all('div', class_="item")

        #Extract image link for each hemisphere
        for hemisphere in all_hemispheres:
            #Find hemisphere name
            hemisphere_name = hemisphere.find('h3').text

            #Find the link to hemiphere page
            link = hemisphere.find('a', class_ = "itemLink product-item")['href']

            #Create a full URL for hemishphere page
            hemisphere_link = url_4 + link

            #Go to hemisphere page
            browser.visit(hemisphere_link)

            #Read page as HTML
            html = browser.html

            #Parse HTML
            soup = bs(html, 'html.parser')

            #Extract link to full image
            img = soup.find('img', class_='wide-image')
            hemisphere_img_link = img['src']

            #Create a full URL for hemisphere image
            hemisphere_image_url = url_4 + hemisphere_img_link

            #Add hemisphere name and hemisphere url to dictionary with results
            hemisphere_image_urls[hemisphere_name] = hemisphere_image_url
        
        # In[51]:
        hemisphere_image_urls

        mars_info_dictionary['hemisphere_images'] = hemisphere_image_urls
        
        mars = {
            "News_Title": mars_info_dictionary["news_titles"],
            "News_Summary": mars_info_dictionary["news_paragraph"],
            "Featured_Image": mars_info_dictionary["featured_image"],
            "Facts_Table": mars_info_dictionary["mars_fact"],
            "Hemisphere_Image_urls": mars_info_dictionary['hemisphere_images']
        }

        return mars

     



