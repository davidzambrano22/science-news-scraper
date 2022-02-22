from attr import attr
from query_url import queryUrl
from downloader import Downloader
from bs4 import BeautifulSoup as bs
from argparse import ArgumentParser


def pages_crawler(query, start_date, end_date):
    downloader = Downloader()
    query_generator = queryUrl(query = query, start_date = start_date, end_date = end_date)
    main_query_url = query_generator.get_url()
    articles = True
    count = 1
    while articles == True:
        url = main_query_url if count == 1 else  query_generator.urlPlusPage(main_query_url, count)
        html = downloader.Download(url)['html']
        is_empty = articles_scraper(html)
        if is_empty or count == 5:
            articles = False
        count += 1

def articles_scraper(html):
    soup = bs(html, 'html.parser')
    articles = soup.find_all('li', attrs={'role': 'list-item'})
    if articles:
        links = get_link(articles)
        return False
    else:
        return True

def get_link(articles):
    for art in articles:
        div_list = art.find_all('div', attrs = {'class':'post-item-river__content___2Ae_0'}) 
        if len(div_list) == 0:
            continue
        div = div_list[0]
        h3 = div.find_all('h3')[0]
        link = h3.find_all('a')[0].get('href')
        print(link)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-q', type = str, help = 'Input your search words separated by single space')
    parser.add_argument('-s', type = str, help = 'Input the start date, separating day, month and year by - character,\n likes this: day-month-year')
    parser.add_argument('-e', type = str, help = 'Input the end date, separating day, month and year by - character,\n likes this: day-month-year')
    args = parser.parse_args()
    pages_crawler(args.q, args.s, args.e)
