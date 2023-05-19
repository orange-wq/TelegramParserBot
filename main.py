import requests
from bs4 import BeautifulSoup
import json
from random import choice
import telebot

bot = telebot.TeleBot(token)  # your token

with open('euler_project.json', 'r', encoding='UTF-8') as file:
    all_tasks = json.load(file)


@bot.message_handler(commands=['task'])
def send_task(message):
    task_to_send = choice(all_tasks)
    bot.send_message(message.chat.id, f'Задача для решения: №{task_to_send["Task №"]}\n{task_to_send["Title"]}\n'
                                      f'{task_to_send["conditions"]}')


bot.polling(none_stop=True)

all_tasks = []
count = 1
for page in range(1, 18):

    url = f'https://euler.jakumo.org/problems/pg/{page}.html'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    table = soup.find('table', class_='problems').find_all('tr')[1:]

    with open('euler_project.json', 'w', encoding='UTF-8') as f:

        for item in table:
            print(f'Обрабатываю элемент №{count}')
            link = item.find_all('td')[1].find('a').get('href')
            r = requests.get(link)
            s = BeautifulSoup(r.text, 'lxml')
            title = s.find('div', class_='probTitle').text
            task = [el.text.strip() for el in s.find_all('p')]
            all_tasks.append(
                {
                    'Task №': count,
                    'Title': title,
                    'сonditions': '\n'.join(task)
                }
            )
            count += 1
        json.dump(all_tasks, f, indent=4, ensure_ascii=False)

