import pandas as pd
from downloader import Downloader
from bs4 import BeautifulSoup as bs
import numpy as np

def get_dates(links):
    frame = pd.DataFrame(columns = ['Date', 'Title', 'Link'])
    row = 0
    for link in links:
        try:
            downloader = Downloader()
            html = downloader.Download(url = link)['html']
            soup = bs(html)
            title = soup.find_all(attrs={'class':'header-default__title___2wL7r'})[0].text
            date = soup.find_all('time', attrs = {'class':'date entry-date byline__published___3GjAo'})[0].text
            frame.loc[row] = [date, title, link]
            row += 1
        except IndexError:
            frame.loc[row] = [date, np.nan, link]
            row += 1
    frame.to_excel('info.xlsx')