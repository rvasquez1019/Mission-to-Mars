# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
  

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": newsTitle,
        "news_paragraph": newsParagraph,
        "featured_image": featuredImage(browser),
        "facts": marsFacts(),
        "last_modified": dt.datetime.now()
    }
    # Hemisphere     
        # "hemisphere1_url": hemispheres[0]["img_url"],
        # "hemisphere1_title": hemispheres[0]["title"],
        # "hemisphere2_url": hemispheres[1]["img_url"],
        # "hemisphere2_title": hemispheres[1]["title"],
        # "hemisphere3_url": hemispheres[2]["img_url"],
        # "hemisphere3_title": hemispheres[2]["title"],
        # "hemisphere4_url": hemispheres[3]["img_url"],
        # "hemisphere4_title": hemispheres[3]["title"],
        

    
    # Stop webdriver and return data
    browser.quit()
    return data



def marsMews(browser):

    # Scrape Mars News 
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
    
    return newsTitle, newsP


def featuredImage(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    fullImageElem = browser.find_by_id('full_image')
    fullImageElem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    moreInfoElem = browser.links.find_by_partial_text('more info')
    moreInfoElem.click()

    # Parse the resulting html with soup
    html = browser.html
    imgSoup = BeautifulSoup(html, 'html.parser')


    # Add try/except for error handling
    try:
        # Find the relative image url
        imgUrlRel = imgSoup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    imgUrl = f'https://www.jpl.nasa.gov{imgUrlRel}'
    
    return imgUrl


def mars_facts():
    
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe 
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap 
    return df.to_html(classes="table table-striped")

# def getHemispheres(brower):

# # Visit the mars nasa news site
# url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
# browser.visit(url) 

# # Convert the browser html to a beautifulSoup object and the quit the browser 
# html = browser.html
# imgSoup = BeautifulSoup(html, 'html.parser')

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
