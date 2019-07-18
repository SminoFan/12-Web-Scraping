from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars_info = {}

    # Visit The Nasa Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest news 
    first_item = soup.find("div", class_ = 'list_text')
    news_title = first_item.find("div", class_="content_title").text
    news_p = first_item.find("div", class_="article_teaser_body").text

    # Store scraped info into dictionary 
    mars_info['news_title'] = news_title
    mars_info['news_story'] = news_p 

    # Visit the url for JPL Featured Space Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    time.sleep(3)

    # Find and store the image url for the current Featured Mars Image 
    html = browser.html
    soup = bs(html, 'html')

    image = soup.find_all("figure", class_="lede")

    featured_image_url = "https://jpl.nasa.gov" + image[0].find("a")['href']
    browser.visit(featured_image_url)

    # Store scraped info into dictionary
    mars_info["featured_image_url"] = featured_image_url
     
    # Visit the Mars Weather twitter account and scrape the weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html')

    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    tweet = tweets[0]

    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    start = tweet_text_box.text.find("sol")
    end = tweet_text_box.text.find("hPa")+3
    mars_weather = tweet_text_box.text[start:end]

    # Store scraped info into dictionary
    mars_info["mars_weather"] = mars_weather

    # Visit the Mars Facts webpage and use Pandas to scrape the table
    # Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html')

    tables = pd.read_html(url)
    mars_data = tables[1]
    mars_data.columns=['description', 'value']
    mars_data = mars_data.set_index('description')
    mars_data = mars_data.to_html()
    mars_data = mars_data.replace('\n', '')

    # Store scraped info into dictionary
    mars_info["mars_facts"] = mars_data

    # Visit the USGS Astrogeology obtain high resolution images for each of Mar's hemispheres.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html')

    hemisphere_image_urls = []

    for i in range(4):
        time.sleep(4)
        imgs = browser.find_by_tag('h3')
        imgs[i].click()
    
        html = browser.html
        soup = bs(html, 'html')
    
        link = soup.find("img", class_="wide-image")["src"]
    
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ link
    
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()

    # Store scraped info into dictionary
    mars_info["mars_hemis"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info
