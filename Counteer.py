import discord
import sys
import csv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pickle
import time
import os

client = discord.Client()

def logwrite():
    server = client.get_server('214249708711837696')
    dt = datetime.datetime.now()
    date = str(dt.month) + '/' + str(dt.day)
    time = str(dt.hour) + ':' + str(dt.minute)
    count1 = 0
    count2 = 0
    for user in server.members:
        count1 += 1
        if user.status != discord.Status.offline:
            count2 += 1
    data = [date, time, count2, count1]
    if os.path.exists('mcountlogs.csv'):
        wfile = open('mcountlogs.csv', 'a', newline='')
        writer = csv.writer(wfile, delimiter = ',')
        writer.writerow(data)
    else:
        wfile = open('mcountlogs.csv', 'w')
        writer = csv.writer(wfile, delimiter = ',')
        writer.writerow(data)

def logstart():
    print('Logging started')
    sched = BackgroundScheduler()
    sched.add_job(logwrite, 'interval', minutes = 10)
    sched.start()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    logstart()

tokenobject = open('counttoken', 'rb')
tokenid = pickle.load(tokenobject)
tokenobject.close()
client.run(tokenid)