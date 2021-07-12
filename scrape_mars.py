
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time
import numpy as np

def browser_init():     
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

# Create a Beautiful Soup object
    news_html = browser.html
    news_soup = bs(news_html,'lxml')
    print(news_soup)

# Extract title  and paragraph text
    news_title = news_soup.find("div",class_="content_title").text
    news_para = news_soup.find("div", class_="rollover_description_inner").text
    print(f"Title is: {news_title}")
    print(f"Paragraph is: {news_para}")

# JPL Mars Space Images - Featured Image
    jurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jurl)

    jhtml = browser.html
    print(jhtml)

    jpl_soup = bs(jhtml,"html.parser")
    print(jpl_soup)

    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    html=browser.html
    soup = bs(html,"html.parser")

    print(soup)

    print(soup.prettify())

    results=soup.find_all("img", class_="headerimage fade-in")

    print(results)

    for result in results:
        image_source=result["src"]
        print(image_source)

    base_link = (f"https://spaceimages-mars.com/{image_source}")
    base_link

#mars fact

    murl = 'https://galaxyfacts-mars.com/'
#browser.visit(murl)

    table = pd.read_html(murl)
    table

    df=table[0]
    df

    df=df.rename(columns={0:"",1:"Mars",2:"Earth"})

    cols=list(df.columns[[0]])
    df=df.set_index(cols)
    print(df)

    df=df.append(pd.Series(name="Description"))
    df=df.reindex(np.roll(df.index,shift=1))
    df=df.fillna("")

    df

    df.to_html("table.html")

# Visit the USGS Astrogeology Science Center Site
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup=bs(html,"html.parser")

    hemisphere_image_urls = []
    base_url="https://marshemispheres.com/"
    results=soup.find_all("div",attrs={"class":"item"})
#print(results)

    for result in results:
         hemisphere=result.find("a")["href"]
    
    hemisphere=base_url+hemisphere
    # print(hemisphere)
    hemisphere_image_urls.append(hemisphere)
    
    for url in hemisphere_image_urls:
        print(url)
    
    images_url=[]
    image_title=[]

    for url in hemisphere_image_urls:
        browser.visit(url)
        html=browser.html
        soup=bs(html,"html.parser")
        results=soup.find("a",href=lambda href:href and href.endswith("jpg"))
        image_url = results["href"]
        images_url.append(image_url)

        results=soup.find_all("h2",class_="title")
    for result in results:
        title=result.text
        image_title.append(title)


    mars={}
    mars["headline"]=news_title
    mars["news"]=news_para
    mars['images']=image_source
    mars["picture_urls"]=hemisphere_image_urls
    mars['pictures']=images_url
    mars["title"]=image_title


    browser.quit()    
    return mars


    





