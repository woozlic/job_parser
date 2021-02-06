from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from os import environ

from databaser import add_link

import logging

from aiogram import Bot, Dispatcher, executor, types
import asyncio

debug = False

if not debug:
    TELEGRAM_TOKEN = environ['TELEGRAM_TOKEN']
    MY_ID = environ['MY_ID']
else:
    from secret_codes import TELEGRAM_TOKEN, MY_ID

URL_PARSE = 'https://chelyabinsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=Python&L_save_area=true&area=104&from=cluster_area&showClusters=true'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def scheduled(wait_for):

    while True:
        await asyncio.sleep(wait_for)
        post_list = parse()
        for post in post_list:
            if add_link(post['link']):
                msg = f'{post["title"]}\n{post["link"]}\n{post["company"]}\n{post["short_text"]}'
                await bot.send_message(MY_ID, msg)
                await asyncio.sleep(10)


def parse(page=0):

    post_list = []

    userAgent = UserAgent().random
    headers = {'User-Agent': userAgent}
    req = requests.get(URL_PARSE, params={'page': page}, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    pages = soup.find('span', class_='bloko-button-group').text
    posts = soup.find_all('div', class_='vacancy-serp-item')

    for post in posts:
        title = post.find('span', class_='g-user-content').text
        link = post.find('a', class_='HH-LinkModifier')['href']
        company = post.find('div', class_='vacancy-serp-item__meta-info').text
        short_text = post.find('div', class_='g-user-content').text

        post_list.append({'title': title, 'link': link, 'company': company, 'short_text': short_text})

    return post_list


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)
