import telebot
import time
from icmplib import multiping
from ntoken import TOKEN
from hosts import servers_dict

bot = telebot.TeleBot(TOKEN)

servers_ip = list(servers_dict.keys())

print(servers_ip)

hosts = multiping(servers_ip)

stopping = False

@bot.message_handler(commands=['start'])
def start_message(message):
        bot.send_message(message.chat.id, 'Поехали')


@bot.message_handler(commands=['add'])
def start_message(message):
        bot.send_message(message.chat.id, 'Введите данные в формате: "хост <ip> <название>"')


@bot.message_handler(commands=['list'])
def list_message(message):
        bot.send_message(message.chat.id, str(servers_dict))


@bot.message_handler(commands=['remove'])
def start_message(message):
        bot.send_message(message.chat.id, 'Введите данные в формате: "удалить <ip>"')


@bot.message_handler(commands=['startping'])
def start_ping(message):

    chatid = message.chat.id

    global stopping

    stopping = False

    ping_process(chatid)


@bot.message_handler(commands=['stopping'])
def stop_ping(message):

    global stopping

    stopping = True


def ping_process(chatid):

    while stopping is False:
        check_servers(hosts, chatid)
        time.sleep(10)


@bot.message_handler(content_types=['text'])
def remove_server(message):

    chatid = message.chat.id

    if message.text.startswith('удалить'):

            ip = (message.text[8:])

            modify_servers_list('del', ip, chatid)

    if message.text.startswith('хост'):
            index = message.text.find('хост')
            pair = (message.text[index+5:]).split(' ', 1)
            ip = pair[0]
            host_name = pair[1]

            modify_servers_list('add', ip, chatid, host_name)


def check_servers(_hosts, chatid):

    for host in hosts:
            serv_name = servers_dict.get(host.address)
            if host.is_alive is False:
                bot.send_message(chatid, f'{host.address} ({serv_name}) не пингуется!')


def modify_servers_list(action, ip, chatid, host_name=''):

        if action == 'del':
            host_name = servers_dict.get(ip)
            servers_dict.pop(ip)
            bot.send_message(chatid, f'хост {ip} ({host_name}) удален')
        if action == 'add':
            servers_dict[ip] = host_name
            bot.send_message(chatid, f'хост {ip} ({host_name}) добавлен в список отслеживаемых')

        global servers_ip
        global hosts

        servers_ip = list(servers_dict.keys())
        hosts = multiping(servers_ip)

        f = open('hosts.py', 'w')
        f.write(str('servers_dict = ' + str(servers_dict)))
        f.close()

        return servers_dict


bot.polling()



