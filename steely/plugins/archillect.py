'''
Get the latest image from archillect.
'''
from urllib import request
from bs4 import BeautifulSoup


__author__ = 'iandioch'
COMMAND = 'arch'
URL = 'http://archillect.com'


def get_html(url):
    return request.urlopen(url).read()


def get_latest_image_url():
    root_html = get_html(URL)
    soup = BeautifulSoup(root_html, 'html.parser')
    cont = soup.find(id='container')
    link = cont.a['href']

    latest_post_url = URL + link
    latest_post_html = get_html(latest_post_url)
    soup = BeautifulSoup(latest_post_html, 'html.parser')
    return soup.find('img')['src']


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    image = get_latest_image_url()
    bot.sendRemoteImage(image, thread_id=thread_id, thread_type=thread_type)


if __name__ == '__main__':
    print(get_latest_image_url())
