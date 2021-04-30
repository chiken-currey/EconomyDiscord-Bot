'''                                           
 _____ ____ ___  ____   ___ _____       ____  
| ____/ ___/ _ \| __ ) / _ \_   _|_   _|___ \ 
|  _|| |  | | | |  _ \| | | || | \ \ / / __) |
| |__| |__| |_| | |_) | |_| || |  \ V / / __/ 
|_____\____\___/|____/ \___/ |_|   \_/ |_____|
- A new feature packet discord economy bot.   
                                              
Language(s) : Python, SQL, JSON               
Licensed    : Not Licensed                    
Contributes : Reece Harris                    
'''                                            
 
import discord
from discord.utils import get
from discord.ext import commands
from discord import Intents
from datetime import datetime
import sqlite3
import requests
import random
import json
import time
import os

class BotData():

    prefix = json.load(open('data\\config.json'))['prefix']
    token = json.load(open('data\\config.json'))['token']

    xpmsg = json.load(open('data\\config.json'))['xpmsg']
    xplvl = json.load(open('data\\config.json'))['xplvl']
    spam = json.load(open('data\\config.json'))['spamtime']
    swear = json.load(open('data\\config.json'))['allowswear']
    marksforgrade = json.load(open('data\\config.json'))['marksforgrade']

    colour = json.load(open('data\\config.json'))['colour']
    moneysymbl = json.load(open('data\\config.json'))['moneysymbl']

    base = sqlite3.connect('data\\userdata.db')
    item = sqlite3.connect('data\\useritems.db')
    
    swearlist = json.load(open('data\\bannedWords.json'))
    educationfetch = random.choice(json.load(open('data\\education.json'))['questions'])
    
    def status():
        members = 0
        guilds = 0
        for x in client.get_all_members(): members += 1
        for x in client.guilds: guilds += 1
        status = json.load(open('data\\config.json'))['status'].replace('$total_members$', str(members)).replace('$prefix$', json.load(open('data\\config.json'))['prefix']).replace('$total_guilds$', str(guilds))
        
        return status


client = commands.Bot(command_prefix=BotData.prefix, intents=Intents.all(), help_command=None)

#-Career

@client.command()
async def learn(ctx, *, anwser=None):
    data = ()
    embedVar = discord.Embed(title=discord.Embed.Empty, description=f'** **', color=discord.Colour.from_rgb(BotData.colour[0],BotData.colour[1],BotData.colour[2]))
    if anwser == None:
        with BotData.base as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM members
            WHERE _id = :a''',
            {'a':ctx.author.id})
            data = c.fetchone()
        try:
            if data[12] + 86400 > time.time():
                if data[13] == None:
                    embedVar.add_field(name=f"**You have already learned to much today**", value='** **', inline=True)
                else:
                    embedVar.add_field(name=f"**{data[13]}**", value='True or False', inline=True)
            else:
                datalearn = BotData.educationfetch
                with BotData.base as conn:
                    c.execute("""UPDATE members SET _eduCool = :a, _eduQues = :b, _eduAnw = :c
                    WHERE _id = :d""",
                    {'a': int(time.time()), 'b':datalearn['question'], 'c':datalearn['correct_answer'] ,'d': message.author.id})
                    conn.commit()
                embedVar.add_field(name=f"**{datalearn['question']}**", value='True or False', inline=True)
        except:
            datalearn = BotData.educationfetch
            with BotData.base as conn:
                c.execute("""UPDATE members SET _eduCool = :a, _eduQues = :b, _eduAnw = :c
                WHERE _id = :d""",
                {'a': int(time.time()), 'b':datalearn['question'], 'c':datalearn['correct_answer'] ,'d': ctx.author.id})
                conn.commit()
            embedVar.add_field(name=f"**{datalearn['question']}**", value='True or False', inline=True)
    else:
        with BotData.base as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM members
            WHERE _id = :a''',
            {'a':ctx.author.id})
            data = c.fetchone()
        if str(data[14]) == '0':
            embedVar.add_field(name=f"**You have already learned to much today**", value='** **', inline=True)
        elif str(anwser).lower() == str(data[14]).lower():
            with BotData.base as conn:
                c.execute("""UPDATE members SET _eduPoint = _eduPoint + 1
                WHERE _id = :d""",
                {'d': ctx.author.id})
                conn.commit()
            if data[11] >= BotData.marksforgrade:
                embedVar.add_field(name=f"**Correct +1 grade**", value='** **', inline=False)
                with BotData.base as conn:
                    c.execute("""UPDATE members SET _eduPoint = 0, _eduLevel = _eduLevel + 1
                    WHERE _id = :d""",
                    {'d': ctx.author.id})
                    conn.commit()
            else:
                embedVar.add_field(name=f"**Correct +1 mark**", value='** **', inline=True)
        else:
            embedVar.add_field(name=f"**Incorrect, better luck next time**", value='** **', inline=True)
        with BotData.base as conn:
            c.execute("""UPDATE members SET _eduQues = :b, _eduAnw = :c
            WHERE _id = :d""",
            {'b':None, 'c':False ,'d': ctx.author.id})
            conn.commit()

    await ctx.send(embed=embedVar)


#-Economy

@client.command()
async def shop(ctx):
    data2 = json.load(open('data\\shop.json'))
    if time.time() - data2['time'] >= 86400:
        items = []
        raw_data = json.load(open('data\\items.json'))
        for x in range(9):
            temp = random.choice(raw_data)
            price = random.randint(temp['price']['start'],temp['price']['end'])
            rarity = temp['price']['start'] / price
            items.append({"id": x,"name": temp['name'],"emoji": temp['emoji'],"price": price,"rarity": rarity})
        data2['content'] = items
        data2['time'] = time.time()
        json.dump(data2, open('data\\shop.json', 'w'), indent=2)
    data = json.load(open('data\\shop.json'))
    embedVar = discord.Embed(title=discord.Embed.Empty, description=f'** **', color=discord.Colour.from_rgb(BotData.colour[0],BotData.colour[1],BotData.colour[2]), timestamp=datetime.fromtimestamp(data['time'] + 86400))
    embedVar.set_author(name=f"{ctx.author} | Shop Menu", url=discord.Embed.Empty, icon_url='https://i.imgur.com/lOShv1G.png')
    embedVar.set_footer(text='Shop Refreshes :', icon_url=discord.Embed.Empty)
    for x in data['content']:
        rarity = ''
        if 0.7 <= x['rarity']: rarity = ':first_place:'
        elif 0.5 <= x['rarity'] < 0.7: rarity = ':second_place:'
        else: rarity = ':third_place:'
        embedVar.add_field(name=f"{x['emoji']}**{x['name']}**", value=f"**ID :**{x['id']}\n**Price :** {BotData.moneysymbl} {x['price']}\n**Rarity:** {rarity}*{round(x['rarity'], 2)}*", inline=True)
    await ctx.send(embed=embedVar)

#-UserInformation

@client.command(aliases=['info', 'stat'])
async def stats(ctx):
    with BotData.base as conn:
        c = conn.cursor()
        c.execute('''SELECT * FROM members
        WHERE _id = :a''',
        {'a':ctx.author.id})

        data = c.fetchone()

        embedVar = discord.Embed(title=discord.Embed.Empty, description='** **', color=discord.Colour.from_rgb(BotData.colour[0],BotData.colour[1],BotData.colour[2]))
        embedVar.set_author(name=f"{ctx.author} | Stats Menu", url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
        embedVar.add_field(name="**Economy**", value=f":credit_card: **Bank :** {BotData.moneysymbl} {data[6]}\n:moneybag: **Wallet:** {BotData.moneysymbl} {data[5]}", inline=True)
        embedVar.add_field(name="**Career**", value=f":tools: **Job :**{data[8]}\n:money_with_wings: **Wage :** {BotData.moneysymbl} {data[9]}", inline=True)
        embedVar.add_field(name="** **", value='** **', inline=False)
        embedVar.add_field(name="**Education**", value=f":scroll: **Degrees :**{data[10]}\n:white_check_mark: **Marks :** {BotData.moneysymbl} {data[11]}", inline=True)
        embedVar.add_field(name="**Stats**", value=f":medal: **Level :**{data[3]} *({data[4]}/{BotData.xplvl})*\n:speech_balloon: **Messages :** {data[1]}", inline=True)
        await ctx.author.send(embed=embedVar)

@client.command(aliases=['pocket'])
async def backpack(ctx):
    with BotData.item as conn:
        c = conn.cursor()
        c.execute(f'SELECT * FROM _{ctx.author.id}')
        data = c.fetchall()

        embedVar = discord.Embed(title=discord.Embed.Empty, description='** **', color=discord.Colour.from_rgb(BotData.colour[0],BotData.colour[1],BotData.colour[2]))
        embedVar.set_author(name=f"{ctx.author} | Backpack", url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
        if data == []:
            embedVar.add_field(name="Your Backpack is empty!", value=discord.Embed.Empty, inline=False)
        else:
            for x in data:
                rarity = ''
                if 0.7 <= x[4]: rarity = ':first_place:'
                elif 0.5 <= x[4] < 0.7: rarity = ':second_place:'
                else: rarity = ':third_place:'
                embedVar.add_field(name=f"{x[2]}**{x[1]}**", value=f"**Price :** {BotData.moneysymbl} {x[3]}\n**Rarity:** {rarity}*{round(x[4], 2)}*", inline=True)

        await ctx.author.send(embed=embedVar)


#-Moderation

#-Utilities

@client.command()
async def help(ctx):
    embedVar = discord.Embed(title=discord.Embed.Empty, description=discord.Embed.Empty, color=discord.Colour.from_rgb(BotData.colour[0],BotData.colour[1],BotData.colour[2]))
    embedVar.set_author(name=f"{str(client.user)[:-5]} | Help Menu", url=discord.Embed.Empty, icon_url='https://i.imgur.com/NxONR7a.png')
    embedVar.add_field(name="Profile", value=f"`{BotData.prefix}stats`\n`{BotData.prefix}backpack`", inline=False)
    embedVar.add_field(name="Economy", value=f"`{BotData.prefix}shop`\n`{BotData.prefix}buy [ID]`")
    embedVar.add_field(name="Career", value=f"`{BotData.prefix}learn`\n`{BotData.prefix}learn [anwser]`", inline=False)
    embedVar.add_field(name="Moderation", value=f"`{BotData.prefix}warn [@user] [reason]`\n`{BotData.prefix}purge [amount]`\n`{BotData.prefix}kick [@user] [@reason]`\n`{BotData.prefix}ban [@user] [@reason]`", inline=False)

    await ctx.author.send(embed=embedVar)

@client.command()
async def ping(ctx):
    ms = int(client.latency * 1000)
    if ms < 150 : rate = [23, 235, 23]
    elif 150 < ms < 250: rate = [235, 102, 30]
    else: rate = [235, 47, 26]
    await ctx.send(embed=discord.Embed(title=f"Pong! {ms} ms", description=discord.Embed.Empty, color=discord.Colour.from_rgb(rate[0], rate[1], rate[2])))

#-Events

@client.event
async def on_message(message):
    swearfound = False
    if not BotData.swear:
        for x in BotData.swearlist:
            if x in message.content:
                swearfound = True
    if message.content.startswith(BotData.prefix):
        if isinstance(message.channel, discord.channel.DMChannel):pass
        else:await message.delete()
    else:
        if isinstance(message.channel, discord.channel.DMChannel):pass
        else:
            if not swearfound:
                with BotData.base as conn:
                    c = conn.cursor()
                    c.execute('''SELECT _msgCool FROM members
                    WHERE _id = :a''',
                    {'a':message.author.id})
                    times = str(c.fetchone()).replace(',','').replace('(','').replace(')','')
                    if times == "None":
                        c.execute("""UPDATE members SET _msgCool = :a
                        WHERE _id = :b""",
                        {'a': int(time.time()), 'b': message.author.id})
                        c.execute("""UPDATE members SET _xp = _xp + :a
                        WHERE _id = :b""",
                        {'a': BotData.xpmsg, 'b': message.author.id})
                    else:
                        cooldown = int(time.time()) - int(times)
                        if cooldown > BotData.spam:
                            c.execute("""UPDATE members SET _xp = _xp + :a
                            WHERE _id = :b""",
                            {'a': BotData.xpmsg, 'b': message.author.id})
                            c.execute("""UPDATE members SET _msgCool = :a
                            WHERE _id = :b""",
                            {'a': int(time.time()), 'b': message.author.id})
                        else:
                            if isinstance(message.channel, discord.channel.DMChannel):pass
                            else:await message.delete()

                c.execute("""UPDATE members SET _messages = _messages + :a
                WHERE _id = :b""",
                {'a': 1, 'b': message.author.id})

                c.execute('''SELECT _xp FROM members
                WHERE _id = :a''',
                {'a':message.author.id})

                if int(str(c.fetchone()).replace('(','').replace(')','').replace(',','')) >= BotData.xplvl:
                    c.execute("""UPDATE members SET _level = _level + :a
                    WHERE _id = :b""",
                    {'a': 1, 'b': message.author.id})
                    c.execute("""UPDATE members SET _xp = :a
                    WHERE _id = :b""",
                    {'a': 0, 'b': message.author.id})

                    c.execute('''SELECT _level FROM members
                    WHERE _id = :a''',
                    {'a':message.author.id})

                    level = str(c.fetchone()).replace('(','').replace(')','').replace(',','')
                    levelup = json.load(open('data\\config.json'))['lvlmsg'].replace('$level$', str(level)).replace('$name$', message.author.display_name).replace('$last_level$', str(int(level)-1))

                    embedVar = discord.Embed(title=levelup, description=discord.Embed.Empty, color=discord.Colour.from_rgb(BotData.colour[0],BotData.colour[1],BotData.colour[2]))
                    embedVar.set_author(name=f"{str(client.user)[:-5]} | Level Up", url=discord.Embed.Empty, icon_url=message.author.avatar_url)
                    
                    await message.author.send(embed=embedVar)

    if swearfound:
        if isinstance(message.channel, discord.channel.DMChannel):pass
        else:await message.delete()

    try:
        conn.commit()
    except:
        pass

    await client.process_commands(message)

@client.event # When the member joins add them to the system
async def on_member_join(member):
    with BotData.base as conn:
        c = conn.cursor()
        all_users=[]
        for x in c.fetchall(): all_users.append(str(x).replace(',','').replace('(','').replace(')',''))
        if str(member.id) in all_users:
            pass
        else:
            c.execute('INSERT INTO members VALUES (:id ,:messages, :spam ,:level, :xp ,:money ,:bank, :items ,:job, :jobWage ,:eduLevel ,:eduPoint ,:eduCool ,:eduQues ,:eduAnw)',
            {'id':member.id, 'messages':0, 'spam':None, 'level':0, 'xp':0, 'money':0, 'bank':0, 'items': 0, 'job':None, 'jobWage':0, 'eduLevel':0, 'eduPoint':0, 'eduCool':None, 'eduQues':None, 'eduAnw':False})
            conn.commit()
            conn.close()
            conn2 = sqlite3.connect('data\\useritems.db')
            c2 = conn2.cursor()
            c2.execute(f"""
            CREATE TABLE _{member.id} (
                _id integer(18) NOT NULL,
                _name varchar(32) NOT NULL,
                _emoji varchar(32) NOT NULL,
                _price integer NOT NULL,
                _rarity FLOAT NOT NULL,
                _amount integer NOT NULL
                )
            """)
            conn2.commit()
            conn2.close()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=BotData.status()))

@client.event
async def on_guild_join(guild):
    conn = sqlite3.connect('data\\userdata.db')
    c = conn.cursor()
    db_data = []
    discord_users = []
    entry_users = []
    entry_ids=[]
    c.execute('SELECT _id FROM members')
    for x in c.fetchall():
        db_data.append(str(x).replace(',','').replace('(','').replace(')',''))
    for x in client.get_all_members(): 
        if str(x.id) in discord_users:pass
        else:discord_users.append(str(x.id))
    for x in discord_users:
        if x not in db_data:
            entry_users.append((x, 0, None, 0, 0, 0, 0, 0, None, 0, 0, 0, None, None, False))
            entry_ids.append(x)
    c.executemany('INSERT INTO members VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    entry_users)
    for x in entry_ids:
        conn2 = sqlite3.connect('data\\useritems.db')
        c2 = conn2.cursor()
        c2.execute(f"""
        CREATE TABLE _{x} (
            _id integer(18) NOT NULL,
            _name varchar(32) NOT NULL,
            _emoji varchar(32) NOT NULL,
            _price integer NOT NULL,
            _rarity FLOAT NOT NULL,
            _amount integer NOT NULL
            )""")
        conn2.commit()
        conn2.close()
    conn.commit()
    conn.close()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=BotData.status()))

@client.event
async def on_ready():
    conn = sqlite3.connect('data\\userdata.db')
    c = conn.cursor()
    db_data = []
    discord_users = []
    entry_users = []
    entry_ids=[]
    c.execute('SELECT _id FROM members')
    for x in c.fetchall():
        db_data.append(str(x).replace(',','').replace('(','').replace(')',''))
    for x in client.get_all_members(): 
        if str(x.id) in discord_users:pass
        else:discord_users.append(str(x.id))
    for x in discord_users:
        if x not in db_data:
            entry_users.append((x, 0, None, 0, 0, 0, 0, 0, None, 0, 0, 0, None, None, False))
            entry_ids.append(x)
    c.executemany('INSERT INTO members VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    entry_users)
    for x in entry_ids:
        conn2 = sqlite3.connect('data\\useritems.db')
        c2 = conn2.cursor()
        c2.execute(f"""
        CREATE TABLE _{x} (
            _id integer(18) NOT NULL,
            _name varchar(32) NOT NULL,
            _emoji varchar(32) NOT NULL,
            _price integer NOT NULL,
            _rarity FLOAT NOT NULL,
            _amount integer NOT NULL
            )""")
        conn2.commit()
        conn2.close()
    conn.commit()
    conn.close()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=BotData.status()))
    print("ready")

if __name__ == "__main__":
    client.run(BotData.token)
