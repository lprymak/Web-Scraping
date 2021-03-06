from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from IPython.display import display_html
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

# # Latest News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    titles = []
    paras = []
    lnks = []

    for x in soup.find_all('div', class_="list_text"):
        title = x.find('div', class_="content_title")
        par = x.find('div', class_="article_teaser_body")
        link = x.a['href']
        titles.append(title.text)
        paras.append(par.text)
        lnks.append(link)

    news = []
    if len(titles) > 4:
        max_rng = 4
    else:
        max_rng=len(titles)
    for x in range(0, max_rng):
        news.append({'title':titles[x], 'text':paras[x], '_url':"https://mars.nasa.gov" + lnks[x]})
    
# # Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=mars&category=featured#submit/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    first_slide = soup.find('li', class_='slide').a['data-fancybox-href']

    featured_image_url = "https://www.jpl.nasa.gov" + first_slide

# # Background Image
    bgImage = soup.find_all(attrs={"data-title": "A Fresh Crater near Sirenum Fossae"})[0]['data-fancybox-href']
    bg_url = "https://www.jpl.nasa.gov" + bgImage

# # Latest Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    tweets = soup.find_all('div', class_='content')

    marsWx_tweets = []
    for tw in tweets:
        if tw.a['href'] == "/MarsWxReport" :
            marsWx_tweets.append(tw)

    wx = marsWx_tweets[0].find('p', class_='tweet-text')
    
    # Remove picture link text from full text
    if wx.a.text:
        wx = wx.text.strip(wx.a.text)
    else:
        wx = wx.text

    mars_weather = wx.replace('\n', ' ')

# # Mars Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    table = soup.find_all('table', id="tablepress-mars")[0]

    table_str = f"""{table}"""
    table_str = table_str.replace('\n', '')

    html_table = table_str.replace('''class="tablepress tablepress-id-mars''', '''class="tablepress tablepress-id-mars table-hover table-light table-borderless''')

# # Hemisphere Images
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    images_lnks = soup.find_all('div', class_='item')

    hrefs = [images_lnks[x].a['href'] for x in range (0, len(images_lnks))]
    
    image_urls = []
    for endpoint in hrefs:
        url = 'https://astrogeology.usgs.gov/' + endpoint
        browser.visit(url)
        
        html = browser.html
        soup = bs(html, 'html.parser')

        image_urls.append("https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src'])


    hemisphere_image_urls = []
    for x in range(0, len(images_lnks)):
        hemisphere_image_urls.append({'title': images_lnks[x].h3.text, 'img_url': image_urls[x]})

    mars_data = {'news': news, 'weather':mars_weather, 'featured_image':featured_image_url, 'bg_image':bg_url, 'facts':html_table, 'hemisphere_images':hemisphere_image_urls}
    browser.quit()

    return mars_data