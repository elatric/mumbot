import discord
import asyncio
import pickle 
import datetime
import os
import time
import logging
import urllib.request
import sys
import wget
import urllib.request

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

def modcheck(user):
    server = client.get_server('214249708711837696')
    modobject = open('modid', 'rb')
    modrole = pickle.load(modobject)
    userid = user.id
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
def getvote():
    voteobject = open('voteid', 'rb')
    voteidtemp = pickle.load(voteobject)
    voteid = client.get_channel(voteidtemp)
    voteobject.close()
    return voteid

def getstat():
    statobject = open('statid', 'rb')
    statidtemp = pickle.load(statobject)
    statid = client.get_channel(statidtemp)
    statobject.close()
    return statid

def getsub():
    subobject = open('subid', 'rb')
    subidtemp = pickle.load(subobject)
    subid = client.get_channel(subidtemp)
    subobject.close()
    return subid

def getmodvote():
    modvoteobject = open('modvote', 'rb')
    modvotetemp = pickle.load(modvoteobject)
    modid = client.get_channel(modvotetemp)
    modvoteobject.close()
    return modid

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

def subcheck(message):
    subchan = getsub()
    if message.channel.id == subchan.id:
        return True
    else:
        return False

def emotesubonoff():
    emoteobject = open('emotesub', 'rb')
    onoff = pickle.load(emoteobject)
    emoteobject.close()
    if onoff == 'on':
        return True
    else:
        return False

def voicechatonoff():
    voiceobject = open('voicechannel', 'rb')
    onoff = pickle.load(voiceobject)
    voiceobject.close()
    if onoff == 'on':
        return True
    else:
        return False

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
    reactor = modcheck(user)
    if reactor == True:
        return True

def selfcheck(user):
    botid = '305833091879141396'
    if user.id == botid:
        return True
    else:
        return False

def getvoicerole(member):
    voiceobject = open('voiceid', 'rb')
    voiceid = pickle.load(voiceobject)
    voiceobject.close()
    voicerole = discord.utils.get(member.server.roles, id=voiceid)
    return voicerole

def addnote(message):
    if message.content.startswith('note'):
        return True
    else:
        return False

async def storeimage(link):
    storechannel = client.get_channel('317835738458619904')
    sendheader = tokenid
    if ('.com' in link) or ('.net' in link):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
        urllib.request.install_opener(opener)
        filename, headers = urllib.request.urlretrieve(url=link)
        #filename = wget.download(link)
        os.rename(filename, filename + ".png")
        newfilename = filename + '.png'
        sendimage = open(os.path.abspath(newfilename), 'rb')
        stored_image = await client.send_file(storechannel, newfilename, content=None)
        sendimage.close()
        found_embeds = stored_image.attachments
        for tempembed in found_embeds:
            post_image = tempembed['url'] 
        return post_image
    else:
        print('Something went wrong when storing the image')
        return None

async def resizeimage(link, size):
    baselink = link
    insert1 = baselink.find('/attachments')
    split = list(baselink)
    adjsize = '?width=' + str(size)
    split.insert(insert1, '.rsz.io')
    split.append(adjsize)
    if 'https' in baselink:
    	split.remove('s')
    templink = ''.join(split)
    finallink = await storeimage(templink)
    return finallink

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    run = voicechatonoff()
    if run == True:
        giverole = getvoicerole(before)
        if not before.voice == after.voice:
            try:
                if after.voice_channel.id == '313489937037131776' or after.voice_channel.id == '313511584435666945' or after.voice_channel.id == '313545012426309632' or after.voice_channel.id == '313536996427694081':
                    yield from client.add_roles(after, giverole)
            except AttributeError:
                yield from client.remove_roles(after, giverole)

@client.event
async def on_reaction_add(reaction, user):
    scheck = servercheck(reaction.message)
    mcheck = modcheck(user)
    isitme = selfcheck(user)
    mvchannel = getmodvote()
    emotesub = emotesubonoff()
    mvtrue = False
    found_embeds_temp = reaction.message.embeds
    if mvchannel.id == reaction.message.channel.id:
        mvtrue = True
    if (scheck == True) and (mcheck == True) and (mvtrue == True) and (isitme == False) and (emotesub == True) and (len(found_embeds_temp) != 0):
        server = client.get_server('214249708711837696')
        livingroom = client.get_channel('214249708711837696')
        verdict = reaction.emoji
        sendmedaddy = getmodvote()
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
            denynote = await client.send_message(sendmedaddy, 'Would you like to add a note? :white_check_mark: or :x:')
            time.sleep(0.5)
            await client.add_reaction(denynote, '✅')
            time.sleep(0.5)
            await client.add_reaction(denynote, '❌')
            denynotereact = await client.wait_for_reaction(emoji=['✅', '❌'], message=denynote, check=modvotecheck)
            notevote = denynotereact.reaction.emoji
            findtrue = 0
            if notevote == '✅':
                findtrue = 1
            if reasonemote == '1⃣':
                if findtrue == 1:
                    notemessage = await client.send_message(sendmedaddy, 'Please type your note. Your message **must** begin with note (e.g. `note this sucks`)')
                    responsetemp = await client.wait_for_message(check=addnote, channel=sendmedaddy)
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
            vote = getvote()    
            votepost = discord.Embed(colour = discord.Colour.teal(), type='rich')
            votepost.set_image(url=post_image)
            votepost.add_field(name='Emote Name: ', value = found_emotename, inline=True)
            votepost.add_field(name='Submitted by: ', value = saveauthor.mention, inline=True)
            votepost.timestamp = datetime.datetime.now()
            publicvotemessage = await client.send_message(vote, embed = votepost)
            await client.delete_message(reaction.message)

@client.event
async def on_message(message):
    mcheck = modcheck(message.author)
    scheck = servercheck(message)
    ccheck = channelcheck(message)
    emotesub = emotesubonoff()
    subtrue = subcheck(message)
    isitme = selfcheck(message.author)
    if (mcheck == True) and (scheck == True) and (ccheck == True) and (message.content.startswith('$')) and (isitme == False):
        if message.content.startswith('$status'):
            vote = getvote()
            stat = getstat()
            if message.content == '$status help' or message.content == '$status':
                await client.send_message(message.channel, '```$status [Set/Edit/Delete] [Emote Name **in colons** or Massreject] [Approved/Rejected/Pending/Global/Retired/Status Attribute/ # to reject] [Stage #] [Note]\nStatus Attributes: Name, Image, Author, Status, Note```')
            else:
                parse = message.content
                sep = parse.split()
                if sep[1] == 'set':
                    if sep[2] == 'Massreject' and len(sep) == 4:
                        print('Running Massreject')
                        async for found_message in client.logs_from(vote, limit=sep[3]):
                            if selfcheck(found_message.author) == True:
                                post_status = 'Rejected'
                                post_stage = '3'
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
                        async for check in client.logs_from(vote):
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
                            for field in findfields:
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
                            await client.send_message(message.channel, 'Please confirm message deletion [Yes/No]')
                            deletecheck = await client.wait_for_message(timeout= 300, author=message.author, channel=message.channel, check=delcheck)
                            if deletecheck.content == 'yes' or deletecheck.content == 'Yes':
                                await client.delete_message(found_message)
                            if deletecheck.content == 'no' or deletecheck.content == 'No':
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
                                print(found_embed)
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
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$modset @modrole`')
            else:
                modstr = sepmod[1]
                finalid1 = modstr.replace('<@&', '')
                finalid = finalid1.replace('>', '')
                modobject = open('modid', 'wb')
                pickle.dump(finalid, modobject)
                modobject.close()
                await client.send_message(message.channel, 'Base modrole set as {}' .format(finalid))
        elif message.content.startswith('$voiceroleset'):
            temp = message.content
            sep = temp.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$voiceroleset @voicerole`')
            else:
                idstr = sep[1]
                finalid1 = idstr.replace('<@&', '')
                finalid = finalid1.replace('>', '')
                voiceobject = open('voiceid', 'wb')
                pickle.dump(finalid, voiceobject)
                voiceobject.close()
                await client.send_message(message.channel, 'Voice chat role set as {}' .format(finalid))
        elif message.content.startswith('$voteset'):
            temp = message.content
            sep = temp.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$voteset #voting-channel`')
            else:
                chanstr = sep[1]
                finalid1 = chanstr.replace('<#', '')
                finalid = finalid1.replace('>', '')
                voteobject = open('voteid', 'wb')
                pickle.dump(finalid, voteobject)
                voteobject.close()
                await client.send_message(message.channel, 'Voting channel set as {}' .format(finalid))
        elif message.content.startswith('$statset'):
            temp = message.content
            sep = temp.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$statset #status-channel`')
            else:
                chanstr = sep[1]
                finalid1 = chanstr.replace('<#', '')
                finalid = finalid1.replace('>', '')
                statobject = open('statid', 'wb')
                pickle.dump(finalid, statobject)
                statobject.close()
                await client.send_message(message.channel, 'Status channel set as {}' .format(finalid))
        elif message.content.startswith('$subset'):
            temp = message.content
            sep = temp.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$subset #submission-channel`')
            else:
                chanstr = sep[1]
                finalid1 = chanstr.replace('<#', '')
                finalid = finalid1.replace('>', '')
                subobject = open('subid', 'wb')
                pickle.dump(finalid, subobject)
                subobject.close()
                await client.send_message(message.channel, 'Submission channel set as {}' .format(finalid))
        elif message.content.startswith('$modvoteset'):
            temp = message.content
            sep = temp.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$modvoteset #mod-voting-channel`')
            else:
                chanstr = sep[1]
                finalid1 = chanstr.replace('<#', '')
                finalid = finalid1.replace('>', '')
                modvoteobject = open('modvote', 'wb')
                pickle.dump(finalid, modvoteobject)
                modvoteobject.close()
                await client.send_message(message.channel, 'Mod voting channel set as {}' .format(finalid))
        elif message.content.startswith('$listen'):
            parse = message.content
            sep = parse.split()
            listenid = []
            if len(sep) == 3:
                if os.path.exists('listenid'):
                    listenobject = open('listenid', 'rb')
                    listenid = pickle.load(listenobject)
                    listenobject.close()
                else:
                    await client.send_message(message.channel, 'No listen channel list found! Appending to new list.')
                if sep[1] == 'add':
                    channel = sep[2]
                    finalid1 = channel.replace('<#', '')
                    finalid = finalid1.replace('>', '')
                    listenid.append(finalid)
                    listenobject = open('listenid', 'wb')
                    pickle.dump(listenid, listenobject)
                    listenobject.close()
                    await client.send_message(message.channel, 'Listen channel `{}` has been added.' .format(finalid))
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
                    await client.send_message(message.channel, 'Listen channel `{}` has been removed.' .format(finalid))
                else:
                    await client.send_message(message.channel, 'Invalid command.')
            elif len(sep) == 1:
                await client.send_message(message.channel, 'The syntax for this command is as follows: `$listen [add/delete] [#channel]`')
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
                await client.send_message(message.channel, 'Current listening channels: `' + chanlist + '`')
            else:
                await client.send_message(message.channel, 'Invalid command.')
        elif message.content.startswith('$feature'):
            parse = message.content
            sep = parse.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'Command Syntax: `$feature [feature] [on/off]`')
                await client.send_message(message.channel, 'Available Features: ```emotesub - moves emote suggestions to mod channel for approval, and then to emote voting\nvoicechannel - gives users in voice chat access to a voice channel-only channel```')
                activefeatures = []
                check1 = emotesubonoff()
                if check1 == True:
                    activefeatures.append('`emotesub - on, ')
                else:
                    activefeatures.append('`emotesub - off, ')
                check2 = voicechatonoff()
                if check2 == True:
                    activefeatures.append('voicechannel - on`')
                else:
                    activefeatures.append('voicechannel - off`')
                activestring = ''.join(activefeatures)
                await client.send_message(message.channel, 'Feature Status: ' + activestring)
            elif sep[2] == 'on':
                if sep[1] == 'emotesub':
                    onoff = sep[2]
                    emoteobject = open('emotesub', 'wb')
                    pickle.dump(onoff, emoteobject)
                    emoteobject.close()
                    await client.send_message(message.channel, 'Automated emote submissions have been turned on.')
                elif sep[1] == 'voicechannel':
                    onoff = sep[2]
                    voiceobject = open('voicechannel', 'wb')
                    pickle.dump(onoff, voiceobject)
                    voiceobject.close()
                    await client.send_message(message.channel, 'Automated voice text channel has been turned on.')
                else:
                    await client.send_message(message.channel, 'Invalid command or input. Type `$feature` for command syntax.')
            elif sep[2] == 'off':
                if sep[1] == 'emotesub':
                    onoff = sep[2]
                    emoteobject = open('emotesub', 'wb')
                    pickle.dump(onoff, emoteobject)
                    emoteobject.close()
                    await client.send_message(message.channel, 'Automated emote submissions have been turned off.')
                elif sep[1] == 'voicechannel':
                    onoff = sep[2]
                    voiceobject = open('voicechannel', 'wb')
                    pickle.dump(onoff, voiceobject)
                    voiceobject.close()
                    await client.send_message(message.channel, 'Automated voice text channel has been turned off.')
                else:
                    await client.send_message(message.channel, 'Invalid command or input. Type `$feature` for command syntax.')
        elif message.content.startswith('$help'):
            await client.send_message(message.channel, 'Available commands: ```$status - post a status update or edit a status update for an emote\n$feature - turn bot modules on/off\n$purge - delete messages from a channel\n$settings - view roles and channels for this bot\n$modset - set the moderator role for this bot\n$voiceroleset - set the automatic voice role to be given\n$listen - add or remove a channel for the bot to listen to\n$subset - set the emote submission channel\n$modvoteset - set the moderator voting channel\n$voteset - set the user voting channel\n$statset - set the emote status channel\n$memes - list of copypastas```')
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
        elif message.content.startswith('$memes'):
            await client.send_message(message.channel, '```$iloveyou\n$bruce\n$bruce2\n$hands\n$lovely```')
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
                        tempname = temprole.name
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
            await client.send_message(message.channel, 'Roles:```Bot moderator role - {}\nVoice Chat Role - {}\n```\nChannels:```Listening Channels - {}\nSubmission Channel - {}\nModerator Voting Channel - {}\nUser Voting Channel - {}\nEmote Status Channel - {}```'.format(modname, voicename, listenname, subname, modchanname, votename, statname))
        elif message.content.startswith('$settoken'):
            parse = message.content
            sep = parse.split()
            tokenid = sep[1]
            tokenobject = open('tokenid', 'wb')
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
                    await client.send_message(message.channel, 'Purging `'+sep[1]+'` messages')
                    await client.delete_messages(mgs)
                else:
                    await client.send_message(message.channel, 'Invalid number of messages to purge!')
            elif len(sep) == 1:
                await client.send_message(message.channel, 'Command syntax is as follows: `$purge [# of messages to purge]` -- number must be >= 2')
            else:
                await client.send_message(message.channel, 'Invalid input! Type `$purge` for command syntax')
        elif message.content.startswith('$terminate'):
            await client.send_message(message.channel, message.author.mention + ' has terminated Mum\'s Helper')
            sys.exit()
        elif message.content.startswith('$startvote'):
            vote = getvote()
            await client.send_message(message.channel, message.author.mention + ' has opened voting in `'+vote.id+'`')
            await client.send_message(message.channel, 'Now adding reactions')
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
        elif message.content.startswith('$imgfix'):
            vote = getvote()
            parse = message.content
            sep = parse.split()
            '''if len(sep) == 1:
                await client.send_message(message.channel, 'Command syntax is as follows: `$imgfix [emotename]` -- case sensitive')
                await client.delete_message(message)
                return'''
            if len(sep) == 1:
                '''colcountstr = sep[1]
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
                found = '0'''
                async for found_message in client.logs_from(vote, limit=112):
                    if selfcheck(found_message.author) == True:
                        '''checkembed = check.embeds
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
                                break'''
                #if found == '1':
                        found_embeds_temp = found_message.embeds
                        found_embeds = found_embeds_temp[0]
                        post_image=found_embeds['image']['proxy_url']
                        finalimage = await storeimage(post_image)
                        await client.send_message(message.author, post_image + '\n' + finalimage)
                        final_embed = discord.Embed.from_data(found_embeds)
                        final_embed.set_image(url=finalimage)
                        time.sleep(2)
                        await client.edit_message(found_message, new_content = None, embed = final_embed)
                await client.delete_message(message)
                '''else:
                    await client.send_message(message.channel, 'Search term `'+find_key+'` not found')
                    await client.delete_message(message)
                    return'''
        elif message.content.startswith('$review'):
            vote = getvote()
            parse = message.content
            sep = parse.split()
            if len(sep) == 1:
                await client.send_message(message.channel, 'Command syntax is as follows: `$review [emotename]` -- case sensitive')
                await client.delete_message(message)
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
                    await client.add_reaction(modvotemessage, '✅')
                    time.sleep(0.5)
                    await client.add_reaction(modvotemessage, '❌')
                    await client.delete_message(message)
                else:
                    await client.send_message(message.channel, 'Search term `'+find_key+'` not found')
                    return
        else:
            await client.send_message(message.channel, 'Invalid command.')
    elif (scheck == True) and (subtrue == True) and (emotesub == True) and (isitme == False):
        time.sleep(2)
        try: 
            message 
        except:
            print('Message mum, something went wrong') 
            return
        else:
            logchannel = client.get_channel('300752762973585418')
            livingroom = client.get_channel('214249708711837696')
            parse = message.content
            sep = parse.split()
            if len(sep) != 1:
                try:
                    await client.send_message(message.author, ':x: Your submission ' + message.content + ' contains unnecessary information. Please reread the pinned submission guidelines.')
                except:
                    await client.send_message(livingroom, message.author.mention+' :x: Your submission ' + message.content + ' contains unnecessary information. Please reread the pinned submission guidelines.')
                post_image = '`none`'
                found_embeds = message.attachments
                for tempembed in found_embeds:
                    post_image = tempembed['proxy_url']
                await client.send_message(logchannel, message.author.mention + ' wrote ```' + message.content + '``` with image ' + post_image)
                await client.delete_message(message)
                return
            else:
                colcountstr = sep[0]
                colcount = colcountstr.count(':')
                if colcount != 2:
                    try:
                        await client.send_message(message.author, ':x: Your submission ' + message.content + '\'s name is incorrectly formatted. Please reread the pinned submission guidelines.')
                    except:
                        await client.send_message(livingroom, message.author.mention + ' :x: Your submission ' + message.content + '\'s name is incorrectly formatted. Please reread the pinned submission guidelines.')
                    post_image = '`none`'
                    found_embeds = message.attachments
                    for tempembed in found_embeds:
                        post_image = tempembed['proxy_url']
                    await client.send_message(logchannel, message.author.mention + ' wrote ```' + message.content + '``` with image ' + post_image)
                    await client.delete_message(message)
                    return
                else:
                    post_image = ''
                    found_embeds = message.attachments
                    for tempembed in found_embeds:
                        temp_image = tempembed['url']
                    print(temp_image)
                    post_image1 = await storeimage(temp_image)
                    if post_image1 != '':
                        iwidth = ''
                        iheight = ''
                        for tempembed in found_embeds:
                            iwidth = tempembed['width']
                            iheight = tempembed['height']
                        if (iwidth == 112) and (iheight == 112) and ('.png' in post_image1):
                            size = 35
                            post_image = await resizeimage(post_image1, size)
                            sendmedaddy = getmodvote()
                            post = discord.Embed(colour = discord.Colour.teal(), type='rich')
                            post.add_field(name='Emote Name: ', value = sep[0], inline=True)
                            post.add_field(name='Submitted by: ', value = message.author.mention, inline=True)
                            post.set_image(url=post_image)
                            modvotemessage = await client.send_message(sendmedaddy, ':white_check_mark: to accept, :x: to reject', embed = post)
                            time.sleep(0.5)
                            await client.add_reaction(modvotemessage, '✅')
                            time.sleep(0.5)
                            await client.add_reaction(modvotemessage, '❌')
                            saveauthor = message.author
                            savecontent = message.content
                            try:
                                await client.send_message(saveauthor, ':white_check_mark: Your submission ' + message.content + ' has been posted in the moderator review channel. Please wait for a status update.')
                            except:
                                await client.send_message(livingroom, message.author.mention+' :white_check_mark: Your submission ' + message.content + ' has been posted in the moderator review channel. Please wait for a status update.')
                            await client.delete_message(message)
                        else:
                            try:
                                await client.send_message(message.author, ':x: Your submission ' + message.content + '\'s image fails to meet the file requirements. Please reread the pinned submission guidelines.')
                            except:
                                await client.send_message(livingroom, message.author.mention+' :x: Your submission ' + message.content + '\'s image fails to meet the file requirements. Please reread the pinned submission guidelines.')
                            await client.delete_message(message)
                            return
                    else:
                        try:
                            await client.send_message(message.author, ':x: Your submission ' + message.content + ' doesn\'t contain an attached image. Please reread the pinned submission guidelines.')
                        except:
                            await client.send_message(livingroom, message.author.mention+' :x: Your submission ' + message.content + ' doesn\'t contain an attached image. Please reread the pinned submission guidelines.')
                        await client.send_message(logchannel, message.author.mention + ' wrote ```' + message.content + '```')
                        await client.delete_message(message)
                        return
    elif message.server == None and message.content.startswith('$') and isitme == False:
        await client.send_message(message.author, 'You cannot use commands in DMs.')
    elif message.content.startswith('$iloveyou') and mcheck == True:
        await client.send_message(message.channel, 'OK I ADMIT IT I LOVE YOU OK i fucking love you and it breaks my heart when i see you play with someone else or anyone commenting in your profile i just want to be your boyfriend and put a heart in my profile linking to your profile and have a walltext of you commenting cute things i want to play video games talk in discord all night and watch a movie together but you just seem so uninterested in me it fucking kills me and i cant take it anymore i want to remove you but i care too much about you so please i\'m begging you to either love me back or remove me and NEVER contact me again it hurts so much to say this because i need you by my side but if you don\'t love me then i want you to leave because seeing your icon in my friendlist would kill me everyday of my pathetic life')
    elif message.content=='$bruce' and mcheck == True:
        await client.send_message(message.channel, 'Hey its bruce from the lab. I just wanted to say that you\'re honestly the most beautiful girl I\'ve ever seen. I don\'t mean to be creepy or anything i just couldn\'t help myself from approaching u once i saw u talking to mike')
    elif message.content.startswith('$bruce2') and mcheck == True:
        await client.send_message(message.channel, 'Hey its lab from the bruce. I just wanted to say that you\'re honestly the most ugly girl I\'ve ever seen. I don\'t mean to be amazing or anything i just couldn\'t help myself from approaching u once i saw u talking to mike')
    elif message.content.startswith('$hands') and mcheck == True:
        await client.send_message(message.channel, 'Thanks bud, so kind\nYour hands were warm\nAnd very very tiny')
    elif message.content.startswith('$lovely') and mcheck == True:
        await client.send_message(message.channel, 'My dearest long legged, lovely, picturesque treasure, how are you doing today? I\'m better now that you\'re here -- while you\'re still responding, do you want to grab a drink later? Get something to eat? Get married? The usual')    
    elif message.content.startswith('$memes') and mcheck == True:
        await client.send_message(message.channel, '```$iloveyou\n$bruce\n$bruce2\n$hands\n$lovely```')
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
                await client.send_message(message.channel, 'Purging `'+sep[1]+'` messages')
                await client.delete_messages(mgs)
            else:
                await client.send_message(message.channel, 'Invalid number of messages to purge!')
        elif len(sep) == 1:
            await client.send_message(message.channel, 'Command syntax is as follows: `$purge [# of messages to purge]` -- number must be >= 2')
        else:
            await client.send_message(message.channel, 'Invalid input! Type `$purge` for command syntax')
    elif message.content.startswith('$') and mcheck == False and isitme == False and ccheck == True:
        await client.send_message(message.channel, 'You do not have permission to use this command.')

tokenobject = open('tokenid', 'rb')
tokenid = pickle.load(tokenobject)
tokenobject.close()
client.run(tokenid)