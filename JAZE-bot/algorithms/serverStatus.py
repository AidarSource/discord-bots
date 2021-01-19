from urllib.request import Request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# returns current amount players of server. ONLY GAMETRACKER URL ALLOWED
def status(url):
    my_url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Opening up connection, grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    # html parser
    page_soup = soup(page_html, "html.parser")
    # grabs current amount of the server players
    currentZE_players = page_soup.find("span", id="HTML_num_players")
    return currentZE_players.text

# returns maximum slots of the server. ONLY GAMETRACKER URL ALLOWED
def max_players(url):
    my_url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Opening up connection, grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    # html parser
    page_soup = soup(page_html, "html.parser")
    # grabs max_players of the server
    maxZE_players = page_soup.find("span", id="HTML_max_players")
    return maxZE_players.text

# returns current map of the server. ONLY GAMETRACKER URL ALLOWED
def current_map(url):
    my_url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Opening up connection, grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    # html parser
    page_soup = soup(page_html, "html.parser")
    # grabs max_players of the server
    currentMap = page_soup.find("div", id="HTML_curr_map")
    return currentMap.text.strip()
