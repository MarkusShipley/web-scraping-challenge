from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import html5lib
import lxml
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    
    executable_path = {"executable_path": "./chromedriver.exe"}
    browser = Browser("chrome", **executable_path)

    mars_info_dictionary = dict()

    #PART 1
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title')

    news_title = news_title.text.strip()

    mars_info_dictionary['news_titles'] = news_title

    news_paragraph = soup.find('div', class_='article_teaser_body')
    news_paragraph

    news_paragraph = news_paragraph.text.strip()

    mars_info_dictionary['news_paragraph'] = news_paragraph


    #PART 2
    url_2 = "https://spaceimages-mars.com/"
    browser.visit(url_2)


    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('img', class_='headerimage fade-in')
    img_link = img['src']

    featured_image_url = url_2 + img_link

    mars_info_dictionary ['featured_image'] = featured_image_url 


    #PART 3
    url_3 = "https://galaxyfacts-mars.com/"

    df = pd.read_html(url_3)

    mars_df = (df[1])
    
    mars_df.columns = ['name', 'measure']

    mars_info_dictionary['mars_facts'] = mars_df.to_dict('records')
    
    
    #PART 4
    #hemisphere_image_urls = {}
    hemisphere_info = []
    
    url_4 = "https://marshemispheres.com/"

    browser.visit(url_4)

    html = browser.html

    soup = bs(html, 'html.parser')

    nav_list = soup.find('div', class_="collapsible results")

    all_hemispheres = nav_list.find_all('div', class_="item")

    for hemisphere in all_hemispheres:
        
        hemisphere_name = hemisphere.find('h3').text

        link = hemisphere.find('a', class_ = "itemLink product-item")['href']

        hemisphere_link = url_4 + link

        browser.visit(hemisphere_link)

        html = browser.html

        soup = bs(html, 'html.parser')

        img = soup.find('img', class_='wide-image')
        hemisphere_img_link = img['src']

        hemisphere_image_url = url_4 + hemisphere_img_link

        hemisphere_image_urls = {}
        hemisphere_image_urls['name'] = hemisphere_name
        hemisphere_image_urls['url'] = hemisphere_image_url
        hemisphere_info.append(hemisphere_image_urls)

    browser.quit()    
    
    mars_info_dictionary['hemisphere_images'] = hemisphere_info

    return mars_info_dictionary
