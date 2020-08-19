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
    data = {"news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featuredImage(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now(),
            "cerberus" : get_cerberus(browser),
            "schiaparelli": get_schiaparelli(browser),
            "syrtis_major": get_syrtis_major(browser),
            "valles_marineris": get_valles_marineris(browser)
        }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

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
    
    return news_title, news_p


def featuredImage(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        image_url = img_soup.find('div', class_ = 'carousel_items')('article')[0]['style'].\
        replace('background-image: url(','').replace(');', '')[1:-1]

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url}'
    
    return img_url

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
    return df.to_html()

def get_cerberus(brower):

# # Visit the mars nasa news site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url) 

def get_schiaparelli(browser):
    # ### Scrape Featured Image from USGS site
    ### Get Mars Hemisphere images

    # Visit URL: USGS
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hrefs = []
    titles = []
    for x in [0,1,2,3]:
        # initial page click
        browser.find_by_css('a.product-item h3')[x].click()
        # get html from new page
        html= browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        # get title
        title_elem = imgs_soup.find('h2', class_ ='title').text
        titles.append(title_elem)
        # get href
        href = imgs_soup.find('a', text = 'Sample').get('href')
        hrefs.append(href)
        browser.back()
    
    cerberus = hrefs[0]
    schiaparelli = hrefs[1]
    syrtis_major = hrefs[2]
    valles_marineris = hrefs[3]

    return schiaparelli

def get_syrtis_major(browser):
    # ### Scrape Featured Image from USGS site
    ### Get Mars Hemisphere images

    # Visit URL: USGS
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hrefs = []
    titles = []
    for x in [0,1,2,3]:
        # initial page click
        browser.find_by_css('a.product-item h3')[x].click()
        # get html from new page
        html= browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        # get title
        title_elem = imgs_soup.find('h2', class_ ='title').text
        titles.append(title_elem)
        # get href
        href = imgs_soup.find('a', text = 'Sample').get('href')
        hrefs.append(href)
        browser.back()
    
    cerberus = hrefs[0]
    schiaparelli = hrefs[1]
    syrtis_major = hrefs[2]
    valles_marineris = hrefs[3]

    return syrtis_major

def get_valles_marineris(browser):
    # ### Scrape Featured Image from USGS site
    ### Get Mars Hemisphere images

    # Visit URL: USGS
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hrefs = []
    titles = []
    for x in [0,1,2,3]:
        # initial page click
        browser.find_by_css('a.product-item h3')[x].click()
        # get html from new page
        html= browser.html
        imgs_soup = BeautifulSoup(html, 'html.parser')
        # get title
        title_elem = imgs_soup.find('h2', class_ ='title').text
        titles.append(title_elem)
        # get href
        href = imgs_soup.find('a', text = 'Sample').get('href')
        hrefs.append(href)
        browser.back()
    
    cerberus = hrefs[0]
    schiaparelli = hrefs[1]
    syrtis_major = hrefs[2]
    valles_marineris = hrefs[3]

    return valles_marineris

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
