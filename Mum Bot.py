import discord
import asyncio
import pickle 
import datetime
from datetime import timedelta
import os
import time
import logging
import urllib.request
import sys
import wget
import socket
import dropbox

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

socket.setdefaulttimeout(45)

client = discord.Client()
server = client.get_server('214249708711837696')

def modcheck(user):
    modobject = open('modid', 'rb')
    modrole = pickle.load(modobject)
    userid = user.id
    server = client.get_server('214249708711837696')
    try:
        member = server.get_member(userid) 
        checkrole = member.roles
        modtrue = 0
        modobject.close()
        for role in checkrole:
            if role.id == modrole:
                modtrue = 1
                break
        if modtrue == 0:
            return False
        elif modtrue ==0 and userid == '119815473750736899':
            return True
        else:
            return True
    except:
        print('ERROR RETRIEVING USER')
        print(user.id)
        return False

def megarolecheck(user):
    modobject = open('megaid', 'rb')
    modrole = pickle.load(modobject)
    userid = user.id
    server = client.get_server('214249708711837696')
    try:
        member = server.get_member(userid) 
        checkrole = member.roles
        modtrue = 0
        modobject.close()
        for role in checkrole:
            if role.id == modrole:
                modtrue = 1
                break
        if modtrue == 0:
            return False
        elif modtrue ==0 and userid == '119815473750736899':
            return True
        else:
            return True
    except:
        print('ERROR RETRIEVING USER')
        print(user.id)
        return False

def get(name, returntype):
    tempobject = open(name, 'rb')
    tempid = pickle.load(tempobject)
    tempobject.close()
    server = client.get_server('214249708711837696')
    if returntype == 'id':
        return tempid
    elif returntype == 'channel':
        tempchan = client.get_channel(tempid)
        return tempchan
    elif returntype == 'role':
        temprole = discord.utils.get(server.roles, id=tempid)
        return temprole
    elif returntype == 'int':
        tempnum = int(tempid)
        return tempnum
    elif returntype == 'onoff':
        if tempid == 'on':
            return True
        else:
            return False

def servercheck(message):
    testid = '305782987893768202'
    realid = '214249708711837696'
    if message.server != None:
        if message.server.id == realid or message.server.id == testid:
            return True 
        else:
            return False
    else:
        return False

def channelcheck(message):
    listenobject = open('listenid', 'rb')
    listenlist = pickle.load(listenobject)
    listenobject.close()
    good = 0
    for checkid in listenlist:
        if message.channel.id == checkid:
            good = 1
            return True
    if good == 0:
        return False

'''def subcheck(message):
    subchan = get('subid', 'channel')
    if message.channel.id == subchan.id:
        return True
    else:
        return False'''

def delcheck(message):
    if message.content == 'yes' or message.content == 'no' or message.content == 'Yes' or message.content == 'No':
        return True
    else:
        return False

def editcheck(message):
    if message.content.startswith('Change') or message.content.startswith('Stop') or message.content.startswith('change') or message.content.startswith('stop'):
        return True
    else:
        return False

def modvotecheck(reaction, user):
    e = str(reaction.emoji)
    emoji1 = e.startswith('❌')
    emoji2 = e.startswith('✅')
    emoji3 = e.startswith('1⃣')
    emoji4 = e.startswith('2⃣')
    emoji5 = e.startswith('🔢')
    reactor = modcheck(user)
    if reactor == True:
        return True

def selfcheck(user):
    botid = '305833091879141396'
    if user.id == botid:
        return True
    else:
        return False

def addnote(message):
    if message.content.startswith('note') or message.content.startswith('Note'):
        return True
    else:
        return False

async def sendembed(preformat, channel, title, content, author):
    embedbase = None
    if preformat == 'No':
        titleformat = '🚫 ' + title
        embedbase = discord.Embed(colour = discord.Colour.dark_red(), type='rich', title=titleformat, description = content)
        embedbase.timestamp = datetime.datetime.now()
    elif preformat == 'Yes':
        titleformat = '✅ ' + title
        embedbase = discord.Embed(colour = discord.Colour.dark_green(), type='rich', title=titleformat, description = content)
        embedbase.timestamp = datetime.datetime.now()
    elif preformat == 'Maybe':
        titleformat = '⚠ ' + title
        embedbase = discord.Embed(colour = discord.Colour.dark_gold(), type='rich', title=titleformat, description = content)
        embedbase.timestamp = datetime.datetime.now()
    elif preformat == 'What':
        titleformat = '❔ ' + title
        embedbase = discord.Embed(colour = discord.Colour.dark_purple(), type='rich', title=titleformat, description = content)
        embedbase.timestamp = datetime.datetime.now()
    elif preformat == None:
        embedbase = discord.Embed(type='rich', title=title, description = content)
        embedbase.timestamp = datetime.datetime.now()
    else:
        return
    if author == None:
        await client.send_message(channel, embed=embedbase)
    else:
        embedbase.set_author(name=author.name, icon_url=author.avatar_url)
        await client.send_message(channel, embed=embedbase)

async def storeimage(link):
    storechannel = client.get_channel('317835738458619904')
    errorchannel = client.get_channel('305194878139367427')
    sendheader = tokenid
    if ('.com' in link) or ('.net' in link):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        urllib.request.install_opener(opener)
        try:
            filename, headers = urllib.request.urlretrieve(url=link)
            os.rename(filename, filename + ".png")
            newfilename = filename + '.png'
            sendimage = open(os.path.abspath(newfilename), 'rb')
            stored_image = await client.send_file(storechannel, newfilename, content=None)
            sendimage.close()
            found_embeds = stored_image.attachments
            for tempembed in found_embeds:
                post_image = tempembed['url'] 
            return post_image
        except:
            descrip = 'A problem occurred when trying to store image '+link
            await sendembed('Maybe', errorchannel, 'Error', descrip, None)
            return None
    else:
        print('Something went wrong when storing the image')
        return None

async def resizeimage(link, size):
    baselink = link
    split = list(baselink)
    adjsize = '&w=' + str(size)
    split.append(adjsize)
    templink = ''.join(split)
    templink2 = templink.replace('https://', '')
    templink1 = 'https://images.weserv.nl/?url='+templink2
    print('storing ' + templink1)
    finallink = await storeimage(templink1)
    return finallink

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')

@client.event
async def on_member_join(member):
    ctime = member.created_at
    ntime = datetime.datetime.utcnow()
    tdiff1 = (ntime - ctime)
    seconds = tdiff1.total_seconds()
    tdiff = seconds/60
    bnum = get('autoban', 'int')
    mchan = client.get_channel('305194878139367427')
    if bnum == 0:
        pass
    elif (tdiff <= bnum):
        await sendembed('Maybe', mchan, 'Newly Created Account Banned', 'User ' + member.mention + ' has been banned for having a creation time that was ' + str(tdiff) + ' minutes ago.', None)
        await client.ban(member)

'''@client.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    run = get('voicechannel', 'onoff')
    if run == True:
        giverole = get('voiceid', 'role')
        if not before.voice == after.voice:
            voicechanobject = open('voicechan', 'rb')
            voicechan = pickle.load(voicechanobject)
            voicechanobject.close()
            if after.voice_channel == voicechan:
                yield from client.add_roles(after, giverole)
            elif after.voice_channel != voicechan:
                yield from client.remove_roles(after, giverole)'''

@client.event
async def on_reaction_add(reaction, user):
    scheck = servercheck(reaction.message)
    mcheck = modcheck(user)
    isitme = selfcheck(user)
    emotesub = get('emotesub', 'onoff')
    ccheck = channelcheck(reaction.message)
    mvtrue = False
    found_embeds_temp = reaction.message.embeds
    server = client.get_server('214249708711837696')
    if (scheck == True) and (mcheck == True) and (isitme == False) and (emotesub == True) and (len(found_embeds_temp) != 0) and ((reaction.emoji == '❌') or (reaction.emoji == '✅')):
        livingroom = client.get_channel('214249708711837696')
        verdict = reaction.emoji
        sendmedaddy = get('modvote', 'channel')
        found_embeds = found_embeds_temp[0]
        findfields = found_embeds['fields']
        found_name = ''
        found_emotename = ''
        post_image = found_embeds['image']['url']
        findname = found_embeds['fields']
        for field in findfields:
            if ('Submitted by:' in field['name']):
                found_name = field['value']
            elif ('Emote Name:' in field['name']):
                found_emotename = field['value']
        if '<@!' in found_name:
            finalid1 = found_name.replace('<@!', '')
        else:
            finalid1 = found_name.replace('<@', '')
        finalid = finalid1.replace('>', '')
        saveauthor = server.get_member(finalid)
        if verdict == '❌':
            denyreason = await client.send_message(sendmedaddy, ':one: for file requirements, :two: for content requirements :x: to cancel')
            time.sleep(0.5)
            await client.add_reaction(denyreason, '1⃣')
            time.sleep(0.5)
            await client.add_reaction(denyreason, '2⃣')
            time.sleep(0.5)
            await client.add_reaction(denyreason, '❌')
            denychoose = await client.wait_for_reaction(emoji=['1⃣', '2⃣', '❌'], message=denyreason, check=modvotecheck)
            reasonemote = denychoose.reaction.emoji
            if reasonemote == '❌':
                await client.delete_message(denychoose.reaction.message)
                return
            denynote = await client.send_message(sendmedaddy, 'Would you like to add a note? :white_check_mark: or :x:. 🔢 to cancel')
            time.sleep(0.5)
            await client.add_reaction(denynote, '✅')
            time.sleep(0.5)
            await client.add_reaction(denynote, '❌')
            time.sleep(0.5)
            await client.add_reaction(denynote, '🔢')
            denynotereact = await client.wait_for_reaction(emoji=['✅', '❌', '🔢'], message=denynote, check=modvotecheck)
            notevote = denynotereact.reaction.emoji
            findtrue = 0
            if notevote == '✅':
                findtrue = 1
            elif notevote == '🔢':
                await client.delete_message(denynote)
                return
            if reasonemote == '1⃣':
                if findtrue == 1:
                    notemessage = await client.send_message(sendmedaddy, 'Please type your note. Your message **must** begin with note (e.g. `note this sucks`)')
                    responsetemp = await client.wait_for_message(check=addnote, channel=sendmedaddy)
                    response1 = responsetemp.content.replace('note ','')
                    response = responsetemp.content.replace('note ','')
                    try:
                        await client.send_message(saveauthor,':x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the file requirements. Please reread the pinned submission guidelines.')
                        await client.send_message(saveauthor,'A reviewer gave the following note:```'+response+'```')
                    except:
                        await client.send_message(livingroom, saveauthor.mention + ' :x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the file requirements. Please reread the pinned submission guidelines.')
                        await client.send_message(livingroom,'A reviewer gave the following note:```'+response+'```')
                    await client.delete_message(notemessage)
                    await client.delete_message(responsetemp)
                else:
                    try:
                        await client.send_message(saveauthor,':x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the file requirements. Please reread the pinned submission guidelines.')
                    except:
                        await client.send_message(livingroom, saveauthor.mention + ' :x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the file requirements. Please reread the pinned submission guidelines.')
            elif reasonemote == '2⃣':
                if findtrue == 1:
                    notemessage = await client.send_message(sendmedaddy, 'Please type your note. Your message **must** begin with \'note\' or \'Note\' (e.g. `note this sucks`)')
                    responsetemp = await client.wait_for_message(check=addnote, channel=sendmedaddy)
                    response = responsetemp.content.replace('note ','')
                    try:
                        await client.send_message(saveauthor,':x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the content requirements. Please reread the pinned submission guidelines.')
                        await client.send_message(saveauthor,'A reviewer gave the following note:```'+response+'```')
                    except:
                        await client.send_message(livingroom, saveauthor.mention + ' :x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the content requirements. Please reread the pinned submission guidelines.')
                        await client.send_message(livingroom,'A reviewer gave the following note:```'+response+'```')
                    await client.delete_message(notemessage)
                    await client.delete_message(responsetemp)
                else:
                    try:
                        await client.send_message(saveauthor, ':x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the content requirements. Please reread the pinned submission guidelines.')
                    except:
                        await client.send_message(livingroom, saveauthor.mention + ' :x: Your submission ' + found_emotename + ' has been rejected at stage 1, as it failed to meet the content requirements. Please reread the pinned submission guidelines.')
            else:
                try:
                    await client.send_message(saveauthor, ':x: Your submission ' + found_emotename + ' has been rejected at stage 1. Please reread the pinned submission guidelines.')
                except:
                    await client.send_message(livingroom, saveauthor.mention + ' :x: Your submission ' + found_emotename + ' has been rejected at stage 1. Please reread the pinned submission guidelines.')
            await client.delete_message(denyreason)
            await client.delete_message(denynote)
            await client.delete_message(reaction.message)
        elif verdict == '✅':
            try:
                await client.send_message(saveauthor, ':white_check_mark: Your submission ' + found_emotename + ' has passed stage 1, and has been posted in the emote voting channel.')
            except:
                await client.send_message(livingroom, saveauthor.mention + ' :white_check_mark: Your submission ' + found_emotename + ' has passed stage 1, and has been posted in the emote voting channel.')
            vote = get('voteid', 'channel')
            votepost = discord.Embed(colour = discord.Colour.teal(), type='rich')
            votepost.set_image(url=post_image)
            votepost.add_field(name='Emote Name: ', value = found_emotename, inline=True)
            votepost.add_field(name='Submitted by: ', value = saveauthor.mention, inline=True)
            votepost.timestamp = datetime.datetime.now()
            publicvotemessage = await client.send_message(vote, embed = votepost)
            await client.add_reaction(publicvotemessage, '👍')
            await client.add_reaction(publicvotemessage, '👎')
            await client.delete_message(reaction.message)
    elif (scheck == True) and (mcheck == True) and (reaction.message.channel.id == '326122367795593226') and (isitme == False):
        dcheck = reaction.emoji
        if reaction.message.author.id=='204255221017214977' and ('Reported' in reaction.message.content):
            descrip = reaction.message.content
            if dcheck == '✅':
                await sendembed('Yes', reaction.message.channel, 'Action Taken', descrip, user)
            elif dcheck == '🚫':
                await sendembed('No', reaction.message.channel, 'No Action Necessary', descrip, user)
            elif dcheck == '⚠':
                await sendembed('Maybe', reaction.message.channel, 'Troll Report', descrip, user)
            await client.delete_message(reaction.message)
    elif (scheck==True) and (reaction.emoji == '⭐') and (reaction.message.channel.id!='301798483525107712') and (reaction.message.author.id != '155149108183695360') and (reaction.message.author.id != '204255221017214977'):
        post_reactions = reaction.message.reactions
        starnumbase = get('starnum', 'int')
        starnum = 0
        starlist = []
        for tempreact in post_reactions:
            if tempreact.emoji == '⭐':
                starlist = await client.get_reaction_users(tempreact, limit=5)
                starnum = tempreact.count
        modstar = 0
        for reactor in starlist:
            if (reactor.id == '119815473750736899') or (modcheck(reactor) == True):
                modstar = 1
        if modstar == 1:
            starchan = get('starid', 'channel')
            async for found_message in client.logs_from(starchan, limit=50):
                if reaction.message.id in found_message.content:
                    return 
            post_colour = discord.Colour.gold()
            post = discord.Embed(colour = post_colour, description = reaction.message.content)
            nameme = reaction.message.author.name + '#' + reaction.message.author.discriminator
            post.set_author(name=nameme, icon_url=reaction.message.author.avatar_url)
            post.timestamp = datetime.datetime.now()
            found_embeds = reaction.message.attachments
            post_image = None
            if len(found_embeds) != 0:
                for tempembed in found_embeds:
                    post_image = tempembed['url']
                try:
                    post.set_image(url=post_image)
                except:
                    print('I tried')
            info = '⭐ ' + reaction.message.channel.mention + ' ID: ' + reaction.message.id
            # fuck selfstarring thots
            if reaction.message.id in starlist:
                selfstar_alert = '🚨 🚨 ' + reaction.message.author.mention + ' IS A THOT AND SELF-STARRED THEIR MEME 🚨 🚨'
                await client.send_message(reaction.message.channel, selfstar_alert)
            await client.send_message(starchan, info, embed = post) ###################################################################################### RIGHT HERE, DUMBFUCK
            return
        elif starnum == starnumbase and modstar == 0:
            starchan = get('starid', 'channel')
            async for found_message in client.logs_from(starchan, limit=50):
                if reaction.message.id in found_message.content:
                    return 
            post_colour = discord.Colour.gold()
            post = discord.Embed(colour = post_colour, description = reaction.message.content)
            nameme = reaction.message.author.name + '#' + reaction.message.author.discriminator
            post.set_author(name=nameme, icon_url=reaction.message.author.avatar_url)
            post.timestamp = datetime.datetime.now()
            found_embeds = reaction.message.attachments
            post_image = None
            if len(found_embeds) != 0:
                for tempembed in found_embeds:
                    post_image = tempembed['url']
                try:
                    post.set_image(url=post_image)
                except:
                    print('I tried')
            info = '⭐ ' + reaction.message.channel.mention + ' ID: ' + reaction.message.id
            # fuck selfstarring thots
            if reaction.message.id in starlist:
                selfstar_alert = '🚨 🚨 ' + reaction.message.author.mention + ' IS A THOT AND SELF-STARRED THEIR MEME 🚨 🚨'
                await client.send_message(reaction.message.channel, selfstar_alert)
            await client.send_message(starchan, info, embed = post)

@client.event
async def on_message(message):
    if message.author.id != '326698230152691722':
        mcheck = modcheck(message.author)
        scheck = servercheck(message)
        ccheck = channelcheck(message)
        emotesub = get('emotesub', 'onoff')
        #subtrue = subcheck(message)
        isitme = selfcheck(message.author)
        megacheck = megarolecheck(message.author)
        starchan = get('starid', 'channel')
        strip = message.content.replace(' ', '')
        uwu = None
        for role in message.role_mentions:
            mcheck = len([m.name for m in message.author.server.members if role in m.roles])
            if mcheck >= 100:
                server = message.server
                mum = server.get_member('119815473750736899')
                if message.author.id != '119815473750736899':
                    for owo in message.author.roles:
                        await client.remove_roles(message.author, owo)
                    message.author.roles = []
                    targetrole = discord.utils.get(message.author.server.roles, name='thonks')
                    await client.remove_roles(message.author, targetrole)
                    await sendembed('No', mum, '@everyone mention detected', 'User ' + message.author.mention +' has mentioned everyone and been automatically demoted.', None)
        if (message.mention_everyone == True and ccheck == False):
            mum = server.get_member('119815473750736899')
            if message.author.id != '119815473750736899':
                for owo in message.author.roles:
                    await client.remove_roles(message.author, owo)
                message.author.roles = []
                targetrole = discord.utils.get(message.author.server.roles, name='thonks')
                await client.remove_roles(message.author, targetrole)
                await sendembed('No', mum, '@everyone mention detected', 'User ' + message.author.mention +' has mentioned everyone and been automatically demoted.', None)
                embed = discord.Embed(colour = discord.Colour.dark_red(), type='rich', title = '🚫 Raid/spam protection has shut this channel down', description = 'Due to a mention of all the users in the server, this channel and all voice channels except for music have been temporarily closed for all users.\n\nPlease wait for an admin to address the situation, and do not DM any staff in the meantime.')
                embed.timestamp = datetime.datetime.now()
                lockchannels = ['214249708711837696', '358579062270328833', '357001028769546252', '356816009778167809', '313544575698337792']
                for number in lockchannels:
                    storechannel = client.get_channel(number)
                    await client.send_message(storechannel, embed = embed)
                    overwrite1 = discord.PermissionOverwrite()
                    if storechannel.id == '356816009778167809':
                        overwrite1.read_messages = True
                    overwrite1.send_messages = False
                    overwrite1.add_reactions = False
                    await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                voiceshutdown = ['323195721086140417', '323197019151925248', '322225458957647872']
                for number in voiceshutdown:
                    tempchan = client.get_channel(number)
                    overwrite2 = discord.PermissionOverwrite()
                    overwrite2.connect = False
                    await client.edit_channel_permissions(tempchan, targetrole, overwrite2)
        elif (mcheck == True) and (scheck == True) and (ccheck == True) and (message.content.startswith('$')) and (isitme == False):
            if message.content.startswith('$status'):
                vote = get('voteid', 'channel')
                stat = get('statid', 'channel')
                if message.content == '$status help' or message.content == '$status':
                    await client.send_message(message.channel, '```$status [Set/Edit/Delete] [Emote Name **in colons** or Massreject] [Approved/Rejected/Pending/Global/Retired/Status Attribute/ # to reject] [Stage #] [Note]\nStatus Attributes: Name, Image, Author, Status, Note```')
                else:
                    parse = message.content
                    sep = parse.split()
                    if sep[1] == 'set':
                        if sep[2] == 'Massreject' and len(sep) == 4:
                            print('Running Massreject')
                            async for found_message in client.logs_from(vote, limit=int(sep[3])):
                                if selfcheck(found_message.author) == True:
                                    post_status = 'Rejected'
                                    post_stage = '2'
                                    post_up = None
                                    post_down = None
                                    post_reactions = found_message.reactions
                                    for tempreact in post_reactions:
                                        if tempreact.emoji == '👍':
                                            post_up = tempreact.count
                                        elif tempreact.emoji == '👎':
                                            post_down = tempreact.count
                                    post_image = 'https://img.ifcdn.com/images/9871875b70ccd920395f799284902f3c4b3fd519f9c1c1000aa95dd4ab9f159b_1.jpg'
                                    found_embeds_temp = found_message.embeds
                                    found_embeds = found_embeds_temp[0]
                                    post_image=found_embeds['image']['url']
                                    found_name = ''
                                    find_key = ''
                                    findfields = found_embeds['fields']
                                    for field in findfields:
                                        if ('Submitted by:' in field['name']):
                                            found_name = field['value']
                                        elif ('Emote Name:' in field['name']):
                                            find_key = field['value']
                                    post_colour = discord.Colour.red()
                                    post = discord.Embed(colour = post_colour)
                                    post.set_image(url=post_image)
                                    post.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                                    post.add_field(name='Emote Name: ', value = find_key, inline=True)
                                    post.add_field(name='Status: ', value='**' + post_status + '** at stage ' + post_stage + ' (' + str(post_up) + ' 👍 - ' + str(post_down) + ' 👎)', inline=False)
                                    post.add_field(name='Submitted by: ', value = found_name, inline=True)
                                    post.timestamp = datetime.datetime.now()
                                    await client.send_message(stat, found_name, embed = post)
                        elif sep[2] != 'Massreject':     
                            colcountstr = sep[2]
                            colcount = colcountstr.count(':')
                            colfix = ''
                            if colcount != 2 and colcount != 0:
                                colfix = colcountstr.replace(':', '')
                                colfix = ':' + colcountstr + ':'
                            elif colcount == 0:
                                colfix = ':' + colcountstr + ':'
                            else:
                                colfix = colcountstr
                            find_key = colfix
                            post_status_temp = sep[3]
                            post_status = post_status_temp.title()
                            if post_status != 'Retired':
                                post_stage_temp = sep[4]
                                post_stage = ''
                                if (post_stage_temp == '1') or (post_stage_temp == '2') or (post_stage_temp == '3') or (post_stage_temp == '4'):
                                    post_stage = post_stage_temp
                                else:
                                    await client.send_message(message.channel, 'Please check message parameters [Stage not found].')
                                    return
                            found_message = None
                            found = '0'
                            async for check in client.logs_from(vote, limit=200):
                                checkembed = check.embeds
                                check_embed1 = None
                                if len(checkembed) == 1:
                                    check_embed1 = checkembed[0]
                                    findfields = check_embed1['fields']
                                    for field in findfields:
                                        if (find_key in field['value']):
                                            found_message = check
                                            found = '1'
                                            break
                                else:
                                    if (find_key in check.content) and ('$status' not in check.content) and (len(check.reactions)==2):
                                        found_message = check
                                        found = '1'
                                        break
                            post_up = None
                            post_down = None
                            post_image = 'https://img.ifcdn.com/images/9871875b70ccd920395f799284902f3c4b3fd519f9c1c1000aa95dd4ab9f159b_1.jpg'
                            post_note_add = 0
                            if found == '1':
                                '''found_embeds = found_message.attachments
                                for tempembed in found_embeds:
                                    post_image = tempembed['url'] 
                                post_reactions = found_message.reactions'''
                                found_embeds_temp = found_message.embeds
                                found_embeds = found_embeds_temp[0]
                                post_image=found_embeds['image']['url']
                                post_reactions = found_message.reactions
                                if post_status != 'Retired':
                                    for tempreact in post_reactions:
                                        if tempreact.emoji == '👍':
                                            post_up = tempreact.count
                                        elif tempreact.emoji == '👎':
                                            post_down = tempreact.count
                                if len(sep) >= 6:
                                    post_note_temp = sep[5:]
                                    post_note = ' '.join(post_note_temp)
                                    post_note_add = 1
                                '''post_name_temp = []
                                for postmem in found_message.mentions:
                                    post_name_temp.append(postmem.mention)
                                post_name = ' '.join(post_name_temp)'''
                                found_name = ''
                                findname = found_embeds['fields']
                                print(findname)
                                for field in findname:
                                    if ('Submitted by:' in field['name']):
                                        found_name = field['value']
                                        break
                                post_colour = discord.Colour.light_grey()
                                if post_status == 'Approved':
                                    post_colour = discord.Colour.green()
                                elif post_status == 'Rejected':
                                    post_colour = discord.Colour.red()
                                elif post_status == 'Retired':
                                    post_colour = discord.Colour.red()
                                elif post_status == 'Pending':
                                    post_colour = discord.Colour.gold()
                                elif post_status == 'Global':
                                    post_colour = discord.Colour.purple()
                                post = discord.Embed(colour = post_colour)
                                post.set_image(url=post_image)
                                post.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                                post.add_field(name='Emote Name: ', value = find_key, inline=True)
                                if post_status != 'Retired':
                                    post.add_field(name='Status: ', value='**' + post_status + '** at stage ' + post_stage + ' (' + str(post_up) + ' 👍 - ' + str(post_down) + ' 👎)', inline=False)
                                    post.add_field(name='Submitted by: ', value = found_name, inline=True)
                                else:
                                    post.add_field(name='Status: ', value=post_status, inline=False)
                                post.timestamp = datetime.datetime.now()
                                if post_note_add == 1:
                                    post.add_field(name='Moderator Note: ', value=post_note, inline=False)
                                await client.send_message(stat, found_name, embed = post)
                                deleteme = await client.send_message(message.channel, 'Please confirm message deletion [Yes/No]')
                                deletecheck = await client.wait_for_message(timeout= 300, author=message.author, channel=message.channel, check=delcheck)
                                if deletecheck.content == 'yes' or deletecheck.content == 'Yes':
                                    await client.delete_message(found_message)
                                    await client.delete_message(deleteme)
                                    await client.delete_message(deletecheck)
                                    return
                                if deletecheck.content == 'no' or deletecheck.content == 'No':
                                    await client.delete_message(deleteme)
                                    await client.delete_message(deletecheck)
                                    return
                            else: 
                                await client.send_message(message.channel, 'Please check message parameters [Keyword not found].')
                    elif sep[1] == 'delete':
                        colcountstr = sep[2]
                        colcount = colcountstr.count(':')
                        colfix = ''
                        if colcount != 2 and colcount != 0:
                            colfix = colcountstr.replace(':', '')
                            colfix = ':' + colcountstr + ':'
                        elif colcount == 0:
                            colfix = ':' + colcountstr + ':'
                        else:
                            colfix = colcountstr
                        find_key = colfix
                        found = '0'
                        async for check in client.logs_from(stat):
                                c_embedlist = check.embeds
                                check_embed = None
                                if len(c_embedlist) == 1:
                                    check_embed = c_embedlist[0]
                                    findfields = check_embed['fields']
                                    for field in findfields:
                                        if (find_key in field['value']):
                                            found_message = check
                                            found = '1'
                                            break
                        if found == '1':
                            await client.delete_message(found_message)
                            await client.send_message(message.channel, 'Status update regarding {} has been deleted.' .format(sep[2]))
                        else:
                            await client.send_message(message.channel, 'Search term {} not found!' .format(sep[2]))
                    elif sep[1] == 'edit':
                        if len(sep) > 3:
                            colcountstr = sep[2]
                            colcount = colcountstr.count(':')
                            colfix = ''
                            if colcount != 2 and colcount != 0:
                                colfix = colcountstr.replace(':', '')
                                colfix = ':' + colcountstr + ':'
                            elif colcount == 0:
                                colfix = ':' + colcountstr + ':'
                            else:
                                colfix = colcountstr
                            find_key = colfix
                            found = '0'
                            async for check in client.logs_from(stat):
                                c_embedlist = check.embeds
                                check_embed = None
                                if len(c_embedlist) == 1:
                                    check_embed = c_embedlist[0]
                                    findfields = check_embed['fields']
                                    for field in findfields:
                                        if (find_key in field['value']):
                                            found_message = check
                                            found = '1'
                                            break
                            if found == '1':
                                embedlist = found_message.embeds
                                found_embed = None
                                if len(embedlist) == 1:
                                    found_embed = embedlist[0]
                                #name, image, author, status, note
                                if sep[3] == 'name' or sep[3] == 'Name':
                                    await client.send_message(message.channel, 'Input the following: `Change [New name **in colons**]`')
                                    einput = await client.wait_for_message(timeout = 300, author=message.author, channel=message.channel, check=editcheck)
                                    editparse = einput.content
                                    esplit = editparse.split()
                                    imgsave = found_embed['image']['url']
                                    del found_embed['image']
                                    if einput == None or einput == 'Stop':
                                        return
                                    else:
                                        for fields_dict in found_embed['fields']:
                                            if fields_dict['name'] == 'Emote Name:':
                                                fields_dict['value'] = esplit[1]
                                                break
                                        final_embed = discord.Embed.from_data(found_embed)
                                        final_embed.set_image(url=imgsave)
                                        await client.edit_message(found_message, new_content=found_message.content, embed=final_embed)
                                elif sep[3] == 'image' or sep[3] == 'Image':
                                    await client.send_message(message.channel, 'Input the following: `Change [New image link]`')
                                    einput = await client.wait_for_message(timeout = 300, author=message.author, channel=message.channel, check=editcheck)
                                    editparse = einput.content
                                    esplit = editparse.split()
                                    if einput == None or einput == 'Stop':
                                        return
                                    else:
                                        final_embed = discord.Embed.from_data(found_embed)
                                        final_embed.set_image(url=esplit[1])
                                        await client.edit_message(found_message, new_content=found_message.content, embed=final_embed)
                                elif sep[3] == 'author' or sep[3] == 'Author':
                                    await client.send_message(message.channel, 'Input the following: `Change [New author]`')
                                    einput = await client.wait_for_message(timeout = 300, author=message.author, channel=message.channel, check=editcheck)
                                    editparse = einput.content
                                    esplit = editparse.split()
                                    imgsave = found_embed['image']['url']
                                    del found_embed['image']
                                    if einput == None or einput == 'Stop':
                                        return
                                    else:
                                        for fields_dict in found_embed['fields']:
                                            if fields_dict['name'] == 'Submitted by:':
                                                fields_dict['value'] = esplit[1]
                                                break
                                        final_embed = discord.Embed.from_data(found_embed)
                                        final_embed.set_image(url=imgsave)
                                        await client.edit_message(found_message, new_content=esplit[1], embed=final_embed)
                                elif sep[3] == 'status' or sep[3] == 'Status':
                                    currentstat = ''
                                    for fields_dict in found_embed['fields']:
                                            if fields_dict['name'] == 'Status:':
                                                currentstat = fields_dict['value']
                                                break
                                    await client.send_message(message.channel, 'Current status is: ' + currentstat + '. Please ensure to reinput the number of votes if necessary.')
                                    await client.send_message(message.channel, 'Input the following: `Change [Approved/Rejected/Pending/Global/Retired] [Stage - optional] [Upvotes - optional] [Downvotes - optional]`')
                                    einput = await client.wait_for_message(timeout = 300, author=message.author, channel=message.channel, check=editcheck)
                                    editparse = einput.content
                                    esplit = editparse.split()
                                    imgsave = found_embed['image']['url']
                                    del found_embed['image']
                                    if einput == None or einput == 'Stop':
                                        return
                                    else:
                                        newval = '**Error** please report to mum.'
                                        if len(esplit) == 4:
                                            newval = '**' + esplit[1].title() + '**' + ' (' + esplit[2] + ' 👍 - ' + esplit[3] + ' 👎)'
                                        elif len(esplit) == 5:
                                            newval = '**' + esplit[1].title() + '**' + ' at stage ' + esplit[2] + ' (' + esplit[3] + ' 👍 - ' + esplit[4] + ' 👎)'
                                        elif len(esplit) == 3:
                                            newval = '**' + esplit[1].title() + '**' + ' at stage ' + esplit[2]
                                        elif len(esplit) == 2:
                                            newval = '**' + esplit[1].title() + '**'
                                        for fields_dict in found_embed['fields']:
                                            if fields_dict['name'] == 'Status:':
                                                fields_dict['value'] = newval
                                                break
                                        post_colour = discord.Colour.light_grey()
                                        if esplit[1].title() == 'Approved':
                                            post_colour = discord.Colour.green()
                                        elif esplit[1].title() == 'Rejected':
                                            post_colour = discord.Colour.red()
                                        elif esplit[1].title() == 'Retired':
                                            post_colour = discord.Colour.red()
                                        elif esplit[1].title() == 'Pending':
                                            post_colour = discord.Colour.gold()
                                        elif esplit[1].title() == 'Global':
                                            post_colour = discord.Colour.purple()
                                        final_embed = discord.Embed.from_data(found_embed)
                                        final_embed.colour = post_colour
                                        final_embed.set_image(url=imgsave)
                                        await client.edit_message(found_message, new_content=found_message.content, embed=final_embed)
                                elif sep[3] == 'note' or sep[3] == 'Note':
                                    await client.send_message(message.channel, 'Input the following: `Change [Delete/New note]`')
                                    einput = await client.wait_for_message(timeout = 300, author=message.author, channel=message.channel, check=editcheck)
                                    editparse = einput.content
                                    esplit = editparse.split()
                                    imgsave = found_embed['image']['url']
                                    del found_embed['image']
                                    if einput == None or einput == 'Stop':
                                        return
                                    else:
                                        final_embed = None
                                        if esplit[1] == 'Delete' or esplit[1] == 'delete' or esplit[1] == 'del':
                                            del found_embed['fields'][3]
                                            final_embed = discord.Embed.from_data(found_embed)
                                        else:
                                            newnote_temp = esplit[1:]
                                            newnote = ' '.join(newnote_temp)
                                            exists = 0
                                            for fields_dict in found_embed['fields']:
                                                if fields_dict['name'] == 'Moderator Note:':
                                                    exists = 1
                                                    fields_dict['value'] = newnote
                                                    final_embed = discord.Embed.from_data(found_embed)
                                            if exists == 0:
                                                final_embed = discord.Embed.from_data(found_embed)
                                                final_embed.add_field(name='Moderator Note:', value=newnote, inline=False)
                                        final_embed.set_image(url=imgsave)
                                        await client.edit_message(found_message, new_content=found_message.content, embed=final_embed)
                                else:
                                    await client.send_message(message.channel, 'Edit term {} not found!' .format(sep[3]))
                            else:
                                await client.send_message(message.channel, 'Search term {} not found!' .format(sep[2]))
                        else:
                            await client.send_message(message.channel, 'Please check message parameters [Something is missing].') 
                    else: 
                        await client.send_message(message.channel, 'Please check message parameters [Action not found].')
            elif message.content.startswith('$modset'):
                temp = message.content
                sepmod = temp.split()
                if len(sepmod) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$modset @modrole', None)
                else:
                    modstr = sepmod[1]
                    finalid1 = modstr.replace('<@&', '')
                    finalid = finalid1.replace('>', '')
                    modobject = open('modid', 'wb')
                    pickle.dump(finalid, modobject)
                    modobject.close()
                    descrip = 'Base modrole set as '+finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$megaset'):
                temp = message.content
                sepmod = temp.split()
                if len(sepmod) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$megaset @megathinkrole', None)
                else:
                    modstr = sepmod[1]
                    finalid1 = modstr.replace('<@&', '')
                    finalid = finalid1.replace('>', '')
                    modobject = open('megaid', 'wb')
                    pickle.dump(finalid, modobject)
                    modobject.close()
                    descrip = 'Megathink role set as ' + finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$voiceroleset'):
                temp = message.content
                sep = temp.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$voiceroleset @voicerole', None)
                else:
                    idstr = sep[1]
                    finalid1 = idstr.replace('<@&', '')
                    finalid = finalid1.replace('>', '')
                    voiceobject = open('voiceid', 'wb')
                    pickle.dump(finalid, voiceobject)
                    voiceobject.close()
                    descrip = 'Voice chat role set as ' + finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$voteset'):
                temp = message.content
                sep = temp.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$voteset #voting-channel', None)
                else:
                    chanstr = sep[1]
                    finalid1 = chanstr.replace('<#', '')
                    finalid = finalid1.replace('>', '')
                    voteobject = open('voteid', 'wb')
                    pickle.dump(finalid, voteobject)
                    voteobject.close()
                    descrip = 'Voting channel set as ' + finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$statset'):
                temp = message.content
                sep = temp.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$statset #status-channel', None)
                else:
                    chanstr = sep[1]
                    finalid1 = chanstr.replace('<#', '')
                    finalid = finalid1.replace('>', '')
                    statobject = open('statid', 'wb')
                    pickle.dump(finalid, statobject)
                    statobject.close()
                    descrip = 'Status channel set as ' + finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$subset'):
                temp = message.content
                sep = temp.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$subset #submission-channel', None)
                else:
                    chanstr = sep[1]
                    finalid1 = chanstr.replace('<#', '')
                    finalid = finalid1.replace('>', '')
                    subobject = open('subid', 'wb')
                    pickle.dump(finalid, subobject)
                    subobject.close()
                    descrip = 'Submission channel set as ' + finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$modvoteset'):
                temp = message.content
                sep = temp.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$modvoteset #mod-voting-channel', None)
                else:
                    chanstr = sep[1]
                    finalid1 = chanstr.replace('<#', '')
                    finalid = finalid1.replace('>', '')
                    modvoteobject = open('modvote', 'wb')
                    pickle.dump(finalid, modvoteobject)
                    modvoteobject.close()
                    descrip = 'Mod voting channel set as ' + finalid
                    await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$listen') and message.author.id == '119815473750736899':
                parse = message.content
                sep = parse.split()
                listenid = []
                if len(sep) == 3:
                    if os.path.exists('listenid'):
                        listenobject = open('listenid', 'rb')
                        listenid = pickle.load(listenobject)
                        listenobject.close()
                    else:
                        await sendembed('Maybe', message.channel, 'Missing File', 'No listen channel list found! Appending to new list.', None)
                    if sep[1] == 'add':
                        channel = sep[2]
                        finalid1 = channel.replace('<#', '')
                        finalid = finalid1.replace('>', '')
                        listenid.append(finalid)
                        listenobject = open('listenid', 'wb')
                        pickle.dump(listenid, listenobject)
                        listenobject.close()
                        descrip = 'Listen channel '+finalid+' has been added'
                        await sendembed('Yes', message.channel, 'Channel Added', descrip, None)
                    elif sep[1] == 'delete':
                        finallist = []
                        channel = sep[2]
                        finalid1 = channel.replace('<#', '')
                        finalid = finalid1.replace('>', '')
                        for checkid in listenid:
                            if checkid != finalid:
                                finallist.append(checkid)
                        listenobject = open('listenid', 'wb')
                        pickle.dump(finallist, listenobject)
                        listenobject.close()
                        descrip = 'Listen channel '+finalid+' has been removed'
                        await sendembed('No', message.channel, 'Channel Removed', descrip, None)
                    else:
                        await sendembed('Maybe', message.channel, 'Invalid Command', 'The function you have called does not exist. Please type $listen for a list of available functions and current listening channels.', None)
                elif len(sep) == 1:
                    chanlist = 'None'
                    if os.path.exists('listenid'):
                        listenobject = open('listenid', 'rb')
                        listenid = pickle.load(listenobject)
                        listenobject.close()
                        if len(listenid) == 0:
                            chanlist = 'None'
                        else: 
                            chanlist = ', '.join(listenid)
                    else:
                        chanlist = 'None'
                    descrip = '$listen [add/delete] [#channel]\n\n'+ 'Current listening channels: ' + chanlist
                    await sendembed('What', message.channel, 'Command Syntax', descrip, None)
                else:
                    await sendembed('Maybe', message.channel, 'Invalid Command', 'You have inputted an invalid number of variables. Please type $listen for a list of available functions and current listening channels.', None)
            elif message.content.startswith('$feature'):
                parse = message.content
                sep = parse.split()
                activefeatures = []
                if len(sep) == 1:
                    check1 = get('emotesub', 'onoff')
                    if check1 == True:
                        activefeatures.append('emotesub - on, ')
                    else:
                        activefeatures.append('emotesub - off, ')
                    check2 = get('voicechannel', 'onoff')
                    if check2 == True:
                        activefeatures.append('voicechannel - on')
                    else:
                        activefeatures.append('voicechannel - off')
                    activestring = ''.join(activefeatures)
                    descrip = '**Command Syntax:** $feature [feature] [on/off]\n\n' + '**Available Features:** emotesub - handles emote submissions, voicechannel - gives users in voice chat access to a voice channel-only channel\n\n' + '**Feature Status:** ' + activestring
                    await sendembed('What', message.channel, 'Feature Information', descrip, None)
                elif sep[2] == 'on':
                    if sep[1] == 'emotesub':
                        onoff = sep[2]
                        emoteobject = open('emotesub', 'wb')
                        pickle.dump(onoff, emoteobject)
                        emoteobject.close()
                        await sendembed('Yes', message.channel, 'Feature Enabled', 'Automated emote submissions have been turned on.', None)
                    elif sep[1] == 'voicechannel':
                        onoff = sep[2]
                        voiceobject = open('voicechannel', 'wb')
                        pickle.dump(onoff, voiceobject)
                        voiceobject.close()
                        await sendembed('Yes', message.channel, 'Feature Enabled', 'Automated voice text channel has been turned on.', None)
                    else:
                        await sendembed('Maybe', message.channel, 'Invalid Command', 'The function you have called does not exist. Please type $feature for command syntax and information.', None)
                elif sep[2] == 'off':
                    if sep[1] == 'emotesub':
                        onoff = sep[2]
                        emoteobject = open('emotesub', 'wb')
                        pickle.dump(onoff, emoteobject)
                        emoteobject.close()
                        await sendembed('No', message.channel, 'Feature Disabled', 'Automated emote submissions have been turned off.', None)
                    elif sep[1] == 'voicechannel':
                        onoff = sep[2]
                        voiceobject = open('voicechannel', 'wb')
                        pickle.dump(onoff, voiceobject)
                        voiceobject.close()
                        await sendembed('No', message.channel, 'Feature Disabled', 'Automated voice text channel has been turned off.', None)
                    else:
                        await sendembed('Maybe', message.channel, 'Invalid Command', 'The function you have called does not exist. Please type $feature for command syntax and information.', None)
            elif message.content.startswith('$help'):
                descrip = '**🔨 Moderation**\n$shutdown [all/#channel_names] - shuts down channel(s)\n$restore [all/#channel_names]- reopens channel(s)\n$purge - delete messages from a channel\n$pmute - permanently mute a user\n$bkick - kick a user from the station\n\n**🔧 Utility**\n$broadcast - start/end a broadcast\n$feature - turn bot modules on/off\n$settings - view roles and channels for this bot\n$starboard - manage starboard channel and minimum star amount\n$modset - set the moderator role for this bot\n$voiceroleset - set the automatic voice role to be given\n$listen - add or remove a channel for the bot to listen to\n$subset - set the emote submission channel\n$modvoteset - set the moderator voting channel\n$voteset - set the user voting channel\n$statset - set the emote status channel\n\n**🤔 Emotes**\n$status - post a status update or edit a status update for an emote\n$review - view an emote and add vote options to it\n\n**🕹 Fun**\n$memes - list of copypastas'
                await sendembed('What', message.channel, 'Available Commands', descrip, None)
            elif message.content.startswith('$iloveyou'):
                await client.send_message(message.channel, 'OK I ADMIT IT I LOVE YOU OK i fucking love you and it breaks my heart when i see you play with someone else or anyone commenting in your profile i just want to be your boyfriend and put a heart in my profile linking to your profile and have a walltext of you commenting cute things i want to play video games talk in discord all night and watch a movie together but you just seem so uninterested in me it fucking kills me and i cant take it anymore i want to remove you but i care too much about you so please i\'m begging you to either love me back or remove me and NEVER contact me again it hurts so much to say this because i need you by my side but if you don\'t love me then i want you to leave because seeing your icon in my friendlist would kill me everyday of my pathetic life')
            elif message.content=='$bruce':
                await client.send_message(message.channel, 'Hey its bruce from the lab. I just wanted to say that you\'re honestly the most beautiful girl I\'ve ever seen. I don\'t mean to be creepy or anything i just couldn\'t help myself from approaching u once i saw u talking to mike')
            elif message.content.startswith('$bruce2'):
                await client.send_message(message.channel, 'Hey its lab from the bruce. I just wanted to say that you\'re honestly the most ugly girl I\'ve ever seen. I don\'t mean to be amazing or anything i just couldn\'t help myself from approaching u once i saw u talking to mike')
            elif message.content.startswith('$hands'):
                await client.send_message(message.channel, 'Thanks bud, so kind\nYour hands were warm\nAnd very very tiny')
            elif message.content.startswith('$lovely'):
                await client.send_message(message.channel, 'My dearest long legged, lovely, picturesque treasure, how are you doing today? I\'m better now that you\'re here -- while you\'re still responding, do you want to grab a drink later? Get something to eat? Get married? The usual')    
            elif message.content.startswith('$confess'):
                await client.send_message(message.channel, 'Your such a fucking bitch honestly you told me to confess and now your turning me down why does anyone like you I hope you take your ugly face and [redacted]')
            elif message.content.startswith('$saki'):
                await client.send_message(message.channel, 'l    i    t    e    r    a    l    l    y    a    l    l    d    a    y    e    v    e    r    y    d    a    y    <    3')
            elif message.content.startswith('$dimash'):
                di1 = discord.utils.get(message.author.server.emojis, name='dimash1')
                di2 = discord.utils.get(message.author.server.emojis, name='dimash2')
                await client.send_message(message.channel, str(di1)+str(di2)+':microphone2: weeeeeeeeeeeeeeeeeeeoooooooooooooooooo')
            elif message.content.startswith('$memes'):
                descrip = '$iloveyou\n$bruce\n$bruce2\n$hands\n$lovely\n$confess\n$roar\n$saki\n$dimash'
                await sendembed('What', message.channel, 'Memes', descrip, None)
            elif message.content.startswith('$settings'):
                modobject = open('modid', 'rb')
                modroletemp = pickle.load(modobject)
                modobject.close()
                modrole = discord.utils.get(message.author.server.roles, id=modroletemp)
                modname = modrole.name
                voiceobject = open('voiceid', 'rb')
                voiceid = pickle.load(voiceobject)
                voiceobject.close()
                voicerole = discord.utils.get(message.author.server.roles, id=voiceid)
                voicename = voicerole.name
                listenlist = []
                if os.path.exists('listenid'):
                    listenobject = open('listenid', 'rb')
                    listenid = pickle.load(listenobject)
                    listenobject.close()
                    if len(listenid) == 0:
                        listenlist = ['None']
                    else: 
                        for tempid in listenid:
                            temprole = discord.utils.get(message.author.server.channels, id=tempid)
                            try:
                                tempname = temprole.name
                            except:
                                print('N/A')
                            listenlist.append(tempname)
                else:
                    listenlist = 'None'
                listenname = ', '.join(listenlist)
                subobject = open('subid', 'rb')
                subidtemp = pickle.load(subobject)
                subid = client.get_channel(subidtemp)
                subobject.close()
                subname = subid.name
                modvoteobject = open('modvote', 'rb')
                modvotetemp = pickle.load(modvoteobject)
                modid = client.get_channel(modvotetemp)
                modvoteobject.close()
                modchanname = modid.name
                voteobject = open('voteid', 'rb')
                voteidtemp = pickle.load(voteobject)
                voteid = client.get_channel(voteidtemp)
                voteobject.close()
                votename = voteid.name
                statobject = open('statid', 'rb')
                statidtemp = pickle.load(statobject)
                statid = client.get_channel(statidtemp)
                statobject.close()
                statname = statid.name
                descrip = 'Roles:\nBot moderator role - {}\nVoice Chat Role - {}\n\nChannels:\nListening Channels - {}\nSubmission Channel - {}\nModerator Voting Channel - {}\nUser Voting Channel - {}\nEmote Status Channel - {}'.format(modname, voicename, listenname, subname, modchanname, votename, statname)
                await sendembed('What', message.channel, 'Server Settings', descrip, None)
            elif message.content.startswith('$settoken'):
                parse = message.content
                sep = parse.split()
                tokenid = sep[1]
                tokenobject = open('temptoken', 'wb')
                pickle.dump(tokenid, tokenobject)
                tokenobject.close()
            elif message.content.startswith('$purge'):
                parse = message.content
                sep = parse.split()
                if len(sep) == 2:
                    mgs = []
                    number = sep[1]
                    number = int(number)
                    if number >= 2:
                        async for x in client.logs_from(message.channel, limit = number):
                            mgs.append(x)
                        title = 'Purging `'+sep[1]+'` messages'
                        await sendembed('No', message.channel, title, None, message.author)
                        await client.delete_messages(mgs)
                    else:
                        await sendembed('Maybe', message.channel, 'Error Purging Messages', 'Invalid number of messages to purge!', message.author)
                elif len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$purge [# of messages to purge]` -- number must be >= 2', None)
                else:
                    await sendembed('What', message.channel, 'Invalid Command', 'Type `$purge` for command syntax', None)
            elif (message.content.startswith('$terminate')) and (message.author.id == '119815473750736899'):
                await sendembed('No', message.channel, 'Bot Terminated', None, message.author)
                await client.delete_message(message)
                sys.exit()
            elif message.content.startswith('$startvote'):
                vote = get('voteid', 'channel')
                descrip = 'Voting has been opened in '+vote.id+'\n\n Now adding reactions'
                await sendembed('Yes', message.channel, 'Voting Opened', 'Voting has been opened in ', message.author)
                async for x in client.logs_from(vote):
                    if selfcheck(x.author) == True:
                        try:
                            await client.add_reaction(x, '👍')
                        except:
                            print('owo')
                        try:
                            await client.add_reaction(x, '👎')
                        except:
                            print('owo')
            elif message.content.startswith('$review'):
                vote = get('voteid', 'channel')
                parse = message.content
                sep = parse.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$review [emotename]` -- case sensitive', None)
                    return
                elif len(sep) == 2:
                    colcountstr = sep[1]
                    colcount = colcountstr.count(':')
                    colfix = ''
                    if colcount != 2 and colcount != 0:
                        colfix = colcountstr.replace(':', '')
                        colfix = ':' + colcountstr + ':'
                    elif colcount == 0:
                        colfix = ':' + colcountstr + ':'
                    else:
                        colfix = colcountstr
                    find_key = colfix
                    found_message = None
                    found = ''
                    async for check in client.logs_from(vote, limit=200):
                        checkembed = check.embeds
                        check_embed1 = None
                        if len(checkembed) == 1:
                            check_embed1 = checkembed[0]
                            findfields = check_embed1['fields']
                            for field in findfields:
                                if (find_key in field['value']):
                                    found_message = check
                                    found = '1'
                                    break
                        else:
                            if (find_key in check.content) and ('$status' not in check.content) and (len(check.reactions)==2):
                                found_message = check
                                found = '1'
                                break
                    if found == '1':
                        found_embeds_temp = found_message.embeds
                        found_embeds = found_embeds_temp[0]
                        post_image = found_embeds['image']['url']
                        final_embed = discord.Embed.from_data(found_embeds)
                        final_embed.set_image(url = post_image)
                        modvotemessage = await client.send_message(message.channel, embed = final_embed)
                        time.sleep(0.5)
                        await client.add_reaction(modvotemessage, '👍')
                        time.sleep(0.5)
                        await client.add_reaction(modvotemessage, '👎')
                        await client.delete_message(message)
                    else:
                        await client.send_message(message.channel, 'Search term `'+find_key+'` not found')
                        return
            elif message.content.startswith('$pmute'):
                parse = message.content
                sep = parse.split()
                muterole = discord.utils.get(message.author.server.roles, id='303319098430062602')
                if len(sep) != 1:
                    userlist = message.mentions
                    mutelist = []
                    for user in userlist:
                        try:
                            await client.add_roles(user, muterole)
                            mutelist.append(user.mention)
                        except:
                            print('owo')
                    if len(mutelist) == 1:
                        descrip = 'User ' + ''.join(mutelist) + ' has been permanently muted'
                        await sendembed('No', message.channel, 'User Muted', descrip, message.author)
                    else:
                        descrip = 'Users ' + ' '.join(mutelist) + ' have been permanently muted'
                        await sendembed('No', message.channel, 'Users Muted', descrip, message.author)
                    await client.delete_message(message)
                else:
                    await sendembed('What', message.channel, 'Command Syntax', '$pmute [@user1] [@user2], etc.', None)
            elif message.content.startswith('$shutdown'):
                parse = message.content
                sep = parse.split()
                await sendembed('No', message.channel, 'Shutdown Initiated', None, message.author)
                embed = discord.Embed(colour = discord.Colour.dark_red(), type='rich', title = '🚫 Raid/spam protection has shut this channel down', description = 'Due to excessive chat activity, this channel and all voice channels except for music have been temporarily closed for all users.\n\nPlease wait for an admin to address the situation, and do not DM any staff in the meantime.')
                embed.timestamp = datetime.datetime.now()
                targetrole = discord.utils.get(message.author.server.roles, name='thonks')
                if len(sep) == 1:
                    storechannel = message.channel
                    await client.send_message(storechannel, embed = embed)
                    overwrite1 = discord.PermissionOverwrite()
                    if storechannel.id == '356816009778167809':
                        overwrite1.read_messages = True
                    overwrite1.send_messages = False
                    overwrite1.add_reactions = False
                    await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                else:
                    if sep[1] == 'all':
                        lockchannels = ['214249708711837696', '358579062270328833', '357001028769546252', '356816009778167809', '313544575698337792']
                        for number in lockchannels:
                            storechannel = client.get_channel(number)
                            await client.send_message(storechannel, embed = embed)
                            overwrite1 = discord.PermissionOverwrite()
                            if storechannel.id == '356816009778167809':
                                overwrite1.read_messages = True
                            overwrite1.send_messages = False
                            overwrite1.add_reactions = False
                            await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                    else:
                        lockchannels = message.channel_mentions
                        for storechannel in lockchannels:
                            await client.send_message(storechannel, embed = embed)
                            overwrite1 = discord.PermissionOverwrite()
                            if storechannel.id == '356816009778167809':
                                overwrite1.read_messages = True
                            overwrite1.send_messages = False
                            overwrite1.add_reactions = False
                            await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                voiceshutdown = ['323195721086140417', '323197019151925248', '322225458957647872', '360409181968138240']
                for number in voiceshutdown:
                    tempchan = client.get_channel(number)
                    overwrite2 = discord.PermissionOverwrite()
                    overwrite2.connect = False
                    await client.edit_channel_permissions(tempchan, targetrole, overwrite2)
            elif message.content.startswith('$restore'):
                parse = message.content
                sep = parse.split()
                await sendembed('Yes', message.channel, 'Restore Initiated', None, message.author)
                embed = discord.Embed(colour = discord.Colour.dark_green(), type='rich', title = '✅ Raid/spam protection has been lifted on this channel', description = 'The situation has been handled and this channel has been reopened.\n\nPlease do not spam messages asking what happened -- refer to the information in #announcements.')
                embed.timestamp = datetime.datetime.now()
                targetrole = discord.utils.get(message.author.server.roles, name='thonks')
                if len(sep) == 1:
                    storechannel = message.channel
                    await client.send_message(storechannel, embed = embed)
                    overwrite1 = discord.PermissionOverwrite()
                    if storechannel.id == '356816009778167809':
                        overwrite1.read_messages = True
                    overwrite1.send_messages = None
                    overwrite1.add_reactions = None
                    await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                else:
                    if sep[1] == 'all':
                        lockchannels = ['214249708711837696', '358579062270328833', '357001028769546252', '356816009778167809', '313544575698337792']
                        for number in lockchannels:
                            storechannel = client.get_channel(number)
                            await client.send_message(storechannel, embed = embed)
                            overwrite1 = discord.PermissionOverwrite()
                            if storechannel.id == '356816009778167809':
                                overwrite1.read_messages = True
                            overwrite1.send_messages = None
                            overwrite1.add_reactions = None
                            await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                    else:
                        lockchannels = message.channel_mentions
                        for storechannel in lockchannels:
                            await client.send_message(storechannel, embed = embed)
                            overwrite1 = discord.PermissionOverwrite()
                            if storechannel.id == '356816009778167809':
                                overwrite1.read_messages = True
                            overwrite1.send_messages = None
                            overwrite1.add_reactions = None
                            await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                voiceshutdown = ['323195721086140417', '323197019151925248', '322225458957647872', '360409181968138240']
                for number in voiceshutdown:
                    tempchan = client.get_channel(number)
                    overwrite2 = discord.PermissionOverwrite()
                    overwrite2.connect = False
                    await client.edit_channel_permissions(tempchan, targetrole, overwrite2)
            elif message.content.startswith('$starboard'):
                parse = message.content
                sep = parse.split()
                if len(sep) == 1:
                    await sendembed('What', message.channel, 'Command Syntax', '$starboard [set/num] [channel/minimum stars]', None)
                else:
                    if sep[1] == 'Set' or sep[1] == 'set':
                        channel = sep[2]
                        finalid1 = channel.replace('<#', '')
                        starid = finalid1.replace('>', '')
                        starobject = open('starid', 'wb')
                        pickle.dump(starid, starobject)
                        starobject.close()
                        descrip = 'Starboard channel set as '+starid
                        await sendembed('Yes', message.channel, 'Success', descrip, None)
                    elif sep[1] == 'num' or sep[1] == 'Num':
                        starnum = sep[2]
                        starobject = open('starnum', 'wb')
                        pickle.dump(starnum, starobject)
                        starobject.close()
                        descrip = 'Minimum star number set as '+starnum
                        await sendembed('Yes', message.channel, 'Success', descrip, None)
            elif message.content.startswith('$broadcast'):
                parse = message.content
                sep = parse.split()
                if len(sep) != 1:
                    if (sep[1] == 'channel') or (sep[1] == 'Channel'):
                        voicechan = discord.utils.get(message.author.server.channels, id= sep[2])
                        voicechanobject = open('voicechan', 'wb')
                        pickle.dump(voicechan, voicechanobject)
                        voicechanobject.close()
                        descrip = 'Channel '+voicechan.name +' set as broadcast channel'
                        await sendembed('Yes', message.channel, 'Success', descrip, None)
                    elif (sep[1] == 'add') or (sep[1] == 'Add'):
                        tempchan = message.author.voice_channel
                        voicechanobject = open('voicechan', 'rb')
                        voicechan = pickle.load(voicechanobject)
                        voicechanobject.close()
                        userlist = message.mentions
                        broadcasterperm = discord.PermissionOverwrite()
                        broadcasterperm.connect = True
                        broadcasterperm.speak = True
                        await sendembed('Yes', message.channel, 'Broadcaster(s) Added', None, None)
                        for user in userlist:
                            await client.edit_channel_permissions(voicechan, user, broadcasterperm)
                            if tempchan != None:
                                try:
                                    await client.server_voice_state(user, mute=False)
                                except:
                                    pass
                            else:
                                await sendembed('Maybe', message.channel, 'Unable to Unmute', 'Please manually unmute the broadcaster(s). You must be in the voice channel for automated unmute to work.', None)
                    elif (sep[1] == 'remove') or (sep[1] == 'Remove'):
                        tempchan = message.author.voice_channel
                        voicechanobject = open('voicechan', 'rb')
                        voicechan = pickle.load(voicechanobject)
                        voicechanobject.close()
                        userlist = message.mentions
                        broadcasterperm = discord.PermissionOverwrite()
                        broadcasterperm.connect = None
                        broadcasterperm.speak = False
                        await sendembed('No', message.channel, 'Broadcaster(s) Removed', None, None)
                        for user in userlist:
                            await client.edit_channel_permissions(voicechan, user, broadcasterperm)
                            if tempchan != None:
                                try:
                                    await client.server_voice_state(user, mute=True)
                                except:
                                    pass
                            else:
                                await sendembed('Maybe', message.channel, 'Unable to Mute', 'Please manually mute the broadcaster(s). You must be in the voice channel for automated mute to work.', None)
                    elif (sep[1] == 'start') or (sep[1] == 'Start'):
                        await sendembed('Yes', message.channel, 'Brodcast Starting', None, message.author)
                        voicechanobject = open('voicechan', 'rb')
                        voicechan = pickle.load(voicechanobject)
                        voicechanobject.close()
                        storechannel = client.get_channel('301798483525107712')
                        description = sep
                        description.pop(0)
                        description.pop(0)
                        strdes = ' '.join(description)
                        describeme = message.author.mention + ' has started a broadcast: ' + strdes+'! To listen, join the Mum\'s Station voice channel.\n\nPlease keep discussion to the automatically available home theater text channel.'
                        embed = discord.Embed(colour = discord.Colour.dark_green(), type='rich', title = '🎙 Broadcast Started', description = describeme)
                        embed.timestamp = datetime.datetime.now()
                        await client.send_message(storechannel, embed = embed)
                        targetrole = discord.utils.get(message.author.server.roles, name='thonks')
                        thonksperm = discord.PermissionOverwrite()
                        thonksperm.connect = True
                        thonksperm.speak = False
                        await client.edit_channel_permissions(voicechan, targetrole, thonksperm)
                    elif (sep[1] == 'end') or (sep[1] == 'end') or (sep[1] == 'stop') or (sep[1] == 'stop'):
                        tempchan = message.author.voice_channel
                        voicechanobject = open('voicechan', 'rb')
                        voicechan = pickle.load(voicechanobject)
                        voicechanobject.close()
                        if (tempchan == None) or (tempchan.id != voicechan.id):
                            await sendembed('Maybe', message.channel, 'Error Ending Broadcast', 'You must be in the broadcast channel to end the broadcast.', None)
                            return
                        else:
                            await sendembed('No', message.channel, 'Broadcast Ending', None, message.author)
                            storechannel = client.get_channel('301798483525107712')
                            describeme = 'The broadcast has ended and all users have been disconnected. Thank you for listening!'
                            embed = discord.Embed(colour = discord.Colour.dark_red(), type='rich', title = '🎙 Broadcast Ended', description = describeme)
                            embed.timestamp = datetime.datetime.now()
                            await client.send_message(storechannel, embed = embed)
                            targetrole = discord.utils.get(message.author.server.roles, name='thonks')
                            thonksperm = discord.PermissionOverwrite()
                            thonksperm.connect = False
                            thonksperm.speak = False
                            await client.edit_channel_permissions(voicechan, targetrole, thonksperm)
                            disconnect = await client.create_channel(server, 'Disconnecting...', type=discord.ChannelType.voice)
                            for user in tempchan.voice_members:
                                try:
                                    await client.move_member(user, disconnect)
                                except:
                                    print('error moving user')
                            await client.delete_channel(disconnect)
                else:
                    await sendembed('What', message.channel, 'Command Syntax', '$broadcast [add/remove/start/end] [@user1 @user2 for changing broadcasters / description for starting a broadcast]', None)
            elif message.content.startswith('$bkick'):
                parse = message.content
                sep = parse.split()
                if len(sep) != 1:
                    voicechanobject = open('voicechan', 'rb')
                    voicechan = pickle.load(voicechanobject)
                    voicechanobject.close()
                    userlist = message.mentions
                    kickperm = discord.PermissionOverwrite()
                    kickperm.connect = False
                    kickperm.speak = False
                    try:
                        kickchan = await client.create_channel(server, 'Kicking...', type=discord.ChannelType.voice)
                    except:
                        await sendembed('Maybe', message.channel, 'Error Kicking User', 'Unable to kick at this time. Please retry once the voice channel has disappeared.', message.author)
                        await client.delete_message(message)
                        return
                    kicklist = []
                    for user in userlist:
                        await client.edit_channel_permissions(voicechan, user, kickperm)
                        try:
                            await client.move_member(user, kickchan)
                        except:
                            print('error moving user')
                        kicklist.append(user.mention)
                    await client.delete_channel(kickchan)
                    kickstr = ' '.join(kicklist)
                    if len(sep) == 2:
                        title = 'User '+kickstr+' has been kicked from the channel'
                        await sendembed('No', message.channel, title, None, message.author)
                        await client.delete_message(message)
                    else:
                        title = 'Users '+kickstr+' have been kicked from the channel'
                        await sendembed('No', message.channel, title, None, message.author)
                        await client.delete_message(message)
                else:
                    await sendembed('What', message.channel, 'Command Syntax', '$bkick [@user1] [@user2], etc.', None)
            elif message.content.startswith('$memberdata'):
                dtokenobject = open('dtoken', 'rb')
                dtokenid = pickle.load(dtokenobject)
                dtokenobject.close()
                d = dropbox.Dropbox(dtokenid)
                targetfile = '/' + str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day) + ' ' + str(datetime.datetime.now().hour) + ':' +  str(datetime.datetime.now().minute) + ' MEMBER COUNT.csv'
                with open('mcountlogs.csv', 'rb') as f:
                    meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
                link = d.sharing_create_shared_link(targetfile)
                url = link.url
                await sendembed('Yes', message.channel, 'Member Data Uploaded', url, None)
                    #await sendembed('Maybe', message.channel, 'Member Data Failed to Upload', 'Yell at mum', None)
            elif message.content.startswith('$autoban'):
                parse = message.content
                sep = parse.split()
                if len(sep) != 2:
                    await sendembed('No', message.channel, 'Invalid Number of Variables', None, None)
                else:
                    banobject = open('autoban', 'wb')
                    pickle.dump(sep[1], banobject)
                    banobject.close()
                    await sendembed('Yes', message.channel, 'Autoban Time Updated', 'Autoban time has been set to creation within the past ' + sep[1] + ' minutes', None)
            else:
                await sendembed('Maybe', message.channel, 'Invalid Command', None, None)
        elif message.channel.id == starchan.id and isitme == True:
            repeatlist = []
            async for check in client.logs_from(starchan, limit=7):
                if message.content == check.content:
                    repeatlist.append(check)
            repeatlist.pop(0)
            if len(repeatlist) >= 1:
                if len(repeatlist) == 1:
                    try:
                        await client.delete_message(repeatlist[0])
                    except:
                        print('Starboard delete failure')
                else:
                    try:
                        await client.delete_messages(repeatlist)
                    except:
                        time.sleep(5)
                        try:
                            await client.delete_messages(repeatlist)
                        except:
                            print('Starboard delete failure')
        elif message.server == None and message.content.startswith('$') and isitme == False:
            await client.send_message(message.author, 'You cannot use commands in DMs.')
        elif message.content.startswith('$pmute') and (mcheck == True) and (isitme == False):
            parse = message.content
            sep = parse.split()
            muterole = discord.utils.get(message.author.server.roles, id='303319098430062602')
            if len(sep) != 1:
                userlist = message.mentions
                mutelist = []
                for user in userlist:
                    try:
                        await client.add_roles(user, muterole)
                        mutelist.append(user.mention)
                    except:
                        print('owo')
                if len(mutelist) == 1:
                    descrip = 'User ' + ''.join(mutelist) + ' has been permanently muted'
                    await sendembed('No', message.channel, 'User Muted', descrip, message.author)
                else:
                    descrip = 'Users ' + ' '.join(mutelist) + ' have been permanently muted'
                    await sendembed('No', message.channel, 'Users Muted', descrip, message.author)
                await client.delete_message(message)
            else:
                await sendembed('What', message.channel, 'Command Syntax', '$pmute [@user1] [@user2], etc.', None)
        elif message.content.startswith('$iloveyou') and (megacheck == True or message.author.id == '115110682399080453'):
            await client.send_message(message.channel, 'OK I ADMIT IT I LOVE YOU OK i fucking love you and it breaks my heart when i see you play with someone else or anyone commenting in your profile i just want to be your boyfriend and put a heart in my profile linking to your profile and have a walltext of you commenting cute things i want to play video games talk in discord all night and watch a movie together but you just seem so uninterested in me it fucking kills me and i cant take it anymore i want to remove you but i care too much about you so please i\'m begging you to either love me back or remove me and NEVER contact me again it hurts so much to say this because i need you by my side but if you don\'t love me then i want you to leave because seeing your icon in my friendlist would kill me everyday of my pathetic life')
        elif message.content=='$bruce' and megacheck == True:
            await client.send_message(message.channel, 'Hey its bruce from the lab. I just wanted to say that you\'re honestly the most beautiful girl I\'ve ever seen. I don\'t mean to be creepy or anything i just couldn\'t help myself from approaching u once i saw u talking to mike')
        elif message.content.startswith('$bruce2') and megacheck == True:
            await client.send_message(message.channel, 'Hey its lab from the bruce. I just wanted to say that you\'re honestly the most ugly girl I\'ve ever seen. I don\'t mean to be amazing or anything i just couldn\'t help myself from approaching u once i saw u talking to mike')
        elif message.content.startswith('$hands') and megacheck == True:
            await client.send_message(message.channel, 'Thanks bud, so kind\nYour hands were warm\nAnd very very tiny')
        elif message.content.startswith('$lovely') and megacheck == True:
            await client.send_message(message.channel, 'My dearest long legged, lovely, picturesque treasure, how are you doing today? I\'m better now that you\'re here -- while you\'re still responding, do you want to grab a drink later? Get something to eat? Get married? The usual')    
        elif message.content.startswith('$confess') and megacheck == True:
            await client.send_message(message.channel, 'Your such a fucking bitch honestly you told me to confess and now your turning me down why does anyone like you I hope you take your ugly face and [redacted]')
        elif message.content.startswith('$roar') and megacheck == True:
            await client.send_message(message.channel, '`ROAR MOTHER FUCKER`')
        elif message.content.startswith('$saki') and megacheck == True:
            await client.send_message(message.channel, 'l    i    t    e    r    a    l    l    y    a    l    l    d    a    y    e    v    e    r    y    d    a    y    <    3')
        elif message.content.startswith('$dimash') and megacheck == True:
            di1 = discord.utils.get(message.author.server.emojis, name='dimash1')
            di2 = discord.utils.get(message.author.server.emojis, name='dimash2')
            await client.send_message(message.channel, str(di1)+str(di2)+':microphone2: weeeeeeeeeeeeeeeeeeeoooooooooooooooooo')
        elif message.content.startswith('$memes') and megacheck == True:
            descrip = '$iloveyou\n$bruce\n$bruce2\n$hands\n$lovely\n$confess\n$roar\n$saki\n$dimash'
            await sendembed('What', message.channel, 'Memes', descrip, None)
        elif message.content.startswith('$purge') and mcheck == True:
            parse = message.content
            sep = parse.split()
            if len(sep) == 2:
                mgs = []
                number = sep[1]
                number = int(number)
                if number >= 2:
                    async for x in client.logs_from(message.channel, limit = number):
                        mgs.append(x)
                    title = 'Purging `'+sep[1]+'` messages'
                    await sendembed('No', message.channel, title, None, message.author)
                    await client.delete_messages(mgs)
                else:
                    await sendembed('Maybe', message.channel, 'Error Purging Messages', 'Invalid number of messages to purge!', message.author)
            elif len(sep) == 1:
                await sendembed('What', message.channel, 'Command Syntax', '$purge [# of messages to purge]` -- number must be >= 2', None)
            else:
                await sendembed('What', message.channel, 'Invalid Command', 'Type `$purge` for command syntax', None)
        elif message.content.startswith('$shutdown'):
            parse = message.content
            sep = parse.split()
            await sendembed('No', message.channel, 'Shutdown Initiated', None, message.author)
            embed = discord.Embed(colour = discord.Colour.dark_red(), type='rich', title = '🚫 Raid/spam protection has shut this channel down', description = 'Due to excessive chat activity, this channel and all voice channels except for music have been temporarily closed for all users.\n\nPlease wait for an admin to address the situation, and do not DM any staff in the meantime.')
            embed.timestamp = datetime.datetime.now()
            targetrole = discord.utils.get(message.author.server.roles, name='thonks')
            if len(sep) == 1:
                storechannel = message.channel
                await client.send_message(storechannel, embed = embed)
                overwrite1 = discord.PermissionOverwrite()
                if storechannel.id == '356816009778167809':
                    overwrite1.read_messages = True
                overwrite1.send_messages = False
                overwrite1.add_reactions = False
                await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
            else:
                if sep[1] == 'all':
                    lockchannels = ['214249708711837696', '358579062270328833', '357001028769546252', '356816009778167809', '313544575698337792']
                    for number in lockchannels:
                        storechannel = client.get_channel(number)
                        await client.send_message(storechannel, embed = embed)
                        overwrite1 = discord.PermissionOverwrite()
                        if storechannel.id == '356816009778167809':
                            overwrite1.read_messages = True
                        overwrite1.send_messages = False
                        overwrite1.add_reactions = False
                        await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                else:
                    lockchannels = message.channel_mentions
                    for storechannel in lockchannels:
                        await client.send_message(storechannel, embed = embed)
                        overwrite1 = discord.PermissionOverwrite()
                        if storechannel.id == '356816009778167809':
                            overwrite1.read_messages = True
                        overwrite1.send_messages = False
                        overwrite1.add_reactions = False
                        await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
            voiceshutdown = ['323195721086140417', '323197019151925248', '322225458957647872', '360409181968138240']
            for number in voiceshutdown:
                tempchan = client.get_channel(number)
                overwrite2 = discord.PermissionOverwrite()
                overwrite2.connect = False
                await client.edit_channel_permissions(tempchan, targetrole, overwrite2)
        elif message.content.startswith('$restore'):
            parse = message.content
            sep = parse.split()
            await sendembed('Yes', message.channel, 'Restore Initiated', None, message.author)
            embed = discord.Embed(colour = discord.Colour.dark_green(), type='rich', title = '✅ Raid/spam protection has been lifted on this channel', description = 'The situation has been handled and this channel has been reopened.\n\nPlease do not spam messages asking what happened -- refer to the information in #announcements.')
            embed.timestamp = datetime.datetime.now()
            targetrole = discord.utils.get(message.author.server.roles, name='thonks')
            if len(sep) == 1:
                storechannel = message.channel
                await client.send_message(storechannel, embed = embed)
                overwrite1 = discord.PermissionOverwrite()
                if storechannel.id == '356816009778167809':
                    overwrite1.read_messages = True
                overwrite1.send_messages = None
                overwrite1.add_reactions = None
                await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
            else:
                if sep[1] == 'all':
                    lockchannels = ['214249708711837696', '358579062270328833', '357001028769546252', '356816009778167809', '313544575698337792']
                    for number in lockchannels:
                        storechannel = client.get_channel(number)
                        await client.send_message(storechannel, embed = embed)
                        overwrite1 = discord.PermissionOverwrite()
                        if storechannel.id == '356816009778167809':
                            overwrite1.read_messages = True
                        overwrite1.send_messages = None
                        overwrite1.add_reactions = None
                        await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
                else:
                    lockchannels = message.channel_mentions
                    for storechannel in lockchannels:
                        await client.send_message(storechannel, embed = embed)
                        overwrite1 = discord.PermissionOverwrite()
                        if storechannel.id == '356816009778167809':
                            overwrite1.read_messages = True
                        overwrite1.send_messages = None
                        overwrite1.add_reactions = None
                        await client.edit_channel_permissions(storechannel, targetrole, overwrite1)
            voiceshutdown = ['323195721086140417', '323197019151925248', '322225458957647872', '360409181968138240']
            for number in voiceshutdown:
                tempchan = client.get_channel(number)
                overwrite2 = discord.PermissionOverwrite()
                overwrite2.connect = False
                await client.edit_channel_permissions(tempchan, targetrole, overwrite2)
        elif message.content.startswith('$bkick') and mcheck == True:
            parse = message.content
            sep = parse.split()
            if len(sep) != 1:
                voicechanobject = open('voicechan', 'rb')
                voicechan = pickle.load(voicechanobject)
                voicechanobject.close()
                userlist = message.mentions
                kickperm = discord.PermissionOverwrite()
                kickperm.connect = False
                kickperm.speak = False
                try:
                    kickchan = await client.create_channel(server, 'Kicking...', type=discord.ChannelType.voice)
                except:
                    await sendembed('Maybe', message.channel, 'Error Kicking User', 'Unable to kick at this time. Please retry once the voice channel has disappeared.', message.author)
                    await client.delete_message(message)
                    return
                kicklist = []
                for user in userlist:
                    await client.edit_channel_permissions(voicechan, user, kickperm)
                    try:
                        await client.move_member(user, kickchan)
                    except:
                        print('error moving user')
                    kicklist.append(user.mention)
                await client.delete_channel(kickchan)
                kickstr = ' '.join(kicklist)
                if len(sep) == 2:
                    title = 'User '+kickstr+' has been kicked from the channel'
                    await sendembed('No', message.channel, title, None, message.author)
                    await client.delete_message(message)
                else:
                    title = 'Users '+kickstr+' have been kicked from the channel'
                    await sendembed('No', message.channel, title, None, message.author)
                    await client.delete_message(message)
            else:
                await sendembed('What', message.channel, 'Command Syntax', '$bkick [@user1] [@user2], etc.', None)
        elif strip == '?warnings' and mcheck == True:
            await sendembed('No', message.channel, 'You fucked up', 'Give Dyno the \'Send Messages\' permission in Roles to fix this. Idiot.', None)
            server = client.get_server('214249708711837696')
            dynorole = discord.utils.get(server.roles, id='301803043291267072')
            dynoperms = dynorole.permissions
            dynoperms.send_messages = False
            await client.edit_role(server, dynorole, permissions=dynoperms)
        elif message.author.id=='204255221017214977' and ccheck==True and ('Reported' in message.content):
            await client.add_reaction(message, '✅')
            time.sleep(0.5)
            await client.add_reaction(message, '🚫')
            time.sleep(0.5)
            await client.add_reaction(message, '⚠')
            time.sleep(0.5)
    else:
        return
tokenobject = open('tokenid', 'rb')
tokenid = pickle.load(tokenobject)
tokenobject.close()
client.run(tokenid)