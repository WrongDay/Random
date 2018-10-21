import discord
from discord.ext import commands
from discord.ext.commands import Bot
import json
import time 
import os
import asyncio
import random
import datetime
import aiohttp
from datetime import datetime
from itertools import cycle

#https://pastebin.com/JMVYJpGY -reminder

def prefix(bot, message):
    with open("serverConfig.json") as f:
        prefixes = json.load(f)
    default_prefix = "w!"
    id = message.server.id
    return prefixes.get(id, default_prefix)

Client = discord.Client()
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')
status = ['Work in progress :/', ';-;', 'Made by Wrong#4794']

async def change_status():
  await client.wait_until_ready()
  msgs = cycle(status)

  while not client.is_closed:
    current_status = next(msgs)
    await client.change_presence(game=discord.Game(name=current_status))
    print()
    await asyncio.sleep(10)

@client.event
async def on_ready():
    print("WrongBot is at your service!")
    print(client.user)

@client.event
async def on_server_join(server):
    await client.send_message(server.owner, """Thanks for inviting me! Make sure I have the following permission to work properly:
    **Manage message** for say, and clear command
    **Kick/Ban** to kick and ban users (optional)""")

@client.event 
async def on_message(message):
  if message.content.startswith("w!reverse"):
        await client.send_message(message.channel, message.content[:8:-1])
      
  if message.content.startswith("w!search"):
        await client.send_typing(message.channel)
        args = message.content.split(" ")
        combargs = (" ".join(args[1:]))
        formatted = combargs.replace(" ", "+")
        em = discord.Embed(title=  (" ".join(args[1:])), url='https://www.google.com/search?source=hp&ei=ojeYW6TEGoz45gKXyI3IBw&q=%s' %(formatted), colour=0x32441c)
        em.set_author(name= 'Search results for: ' + (combargs) ,icon_url='https://cdn.discordapp.com/attachments/486611168891502624/488904081369333772/search-flat.png')
        em.set_footer(text='Search generated by: %s' %(message.author) , icon_url= message.author.avatar_url )
        await client.send_message(message.channel, embed=em )
  
  if message.content.startswith("w!urban"):
        await client.send_typing(message.channel)
        args = message.content.split(" ")
        combargs = (" ".join(args[1:]))
        formatted = combargs.replace(" ", "+")
        em = discord.Embed(title=  (" ".join(args[1:])), url='https://www.urbandictionary.com/define.php?term=%s' %(formatted), colour=0x32441c)
        em.set_author(name= 'Urban search results for: ' + (combargs) ,icon_url='https://cdn.discordapp.com/attachments/486611168891502624/488904081369333772/search-flat.png')
        em.set_footer(text='Search generated by: %s' %(message.author) , icon_url= message.author.avatar_url )
        await client.send_message(message.channel, embed=em )
        
  await client.process_commands(message)
    
 #CONFIGS
@client.command(name="prefix", pass_context=True)
async def prefix(ctx, new_prefix):
    with open("serverConfig.json", "r") as f:
        prefixes = json.load(f)
    author = ctx.message.author
    if ctx.message.author.server_permissions.manage_server:
        prefixes[ctx.message.server.id] = new_prefix
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name="Prefix changed to:", value=f"``{new_prefix}``")
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff0200)
        embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
        embed.add_field(name=":x: Error", value="You are missing the following permission: ```Manage Server```", inline=False)
        await client.say(embed=embed)
        
    with open("serverConfig.json", "w") as f:
        json.dump(prefixes, f)
    
@client.command(pass_context=True)
async def help(ctx):
  author = ctx.message.author

  embed = discord.Embed(
    colour = discord.Colour.green()
  )

  embed.set_author(name='Commands:')
  embed.add_field(name='w!help', value='Shows a list of command WrongBot has', inline=False)
  embed.add_field(name='w!prefix', value='Changes the bot prefix', inline=False)
  embed.add_field(name='w!uptime', value='Shows how long the bot has been on', inline=False)
  embed.add_field(name='w!say', value='Makes the bot say something', inline=False)
  embed.add_field(name='w!reverse', value='Reverse your message', inline=False)
  embed.add_field(name='w!search', value='Searches your input on google', inline=False)
  embed.add_field(name='w!urban', value='Searches your input on urban dictionary', inline=False)
  embed.add_field(name='w!yt', value='Searches your input on YouTube', inline=False)
  embed.add_field(name='w!coinflip', value='A 50 50 chance to land on heads or tails', inline=False)
  embed.add_field(name='w!userinfo', value='Shows info of a user', inline = False)
  embed.add_field(name='w!serverinfo', value='Shows server info', inline=False)
  embed.add_field(name='w!clear', value='Clear messages', inline=False)
  embed.add_field(name='w!kick', value='Kicks a user', inline=False)
  embed.add_field(name='w!ban', value='Bans a user', inline=False)

  await client.send_message(author, embed=embed)
  await client.say('DMed you a message containing all the commands!')

#Fun commands
@client.command(pass_context = True)
async def say(ctx, *args):
    mesg = ' '.join(args)
    await client.delete_message(ctx.message)
    return await client.say(mesg)

@client.command(pass_context=True)
async def coinflip(ctx):
    pick = ['heads','tails']
    flip = random.choice(pick)
    await client.say ("The coin landed on " + flip + '!')
    return

@client.command(pass_context = True)
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://api.reddit.com/r/me_irl/random") as r:
            author = ctx.message.author
            data = await r.json()
            embed = discord.Embed(title="Meme:",
                                  description="*;))))*",
                                  color=0x00ff00)
            embed.set_image(url = data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(icon_url=author.avatar_url, text="| Fun Commands!")

            await client.say(embed=embed)

@client.command(pass_context=True, aliases = ["8ball"])
async def eightball(ctx, *, question):
    author = ctx.message.author
    choice = ['Yes', 'No', 'Better not tell you now']
    picked = random.choice(choice)
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name= "**"+question+"**", value = picked, inline = False)
    embed.set_footer(icon_url=author.avatar_url, text="Fun Commands!")
    await client.say(embed=embed)
    return              
            
#Helpful commands            
@client.command(pass_context = True)
async def avatar(ctx, user: discord.Member = None):
    await client.send_typing(ctx.message.channel)
    if user is None:
        embed = discord.Embed(title="{}'s Avatar:".format(ctx.message.author.name), color=0x00ff00)
        embed.set_image(url=ctx.message.author.avatar_url)
        embed.add_field(name="Link: ", value=ctx.message.author.avatar_url, inline=True)
        await client.say(embed=embed)

    else:
        embed = discord.Embed(title="{}'s Avatar:".format(user.name), color=0x00ff00)
        embed.set_image(url=user.avatar_url)
        embed.add_field(name="Link: ", value=user.avatar_url, inline=True)
        await client.say(embed=embed)

            
@client.command(pass_context=True)
async def userinfo(ctx, user: discord.Member = None):
    if user == None:
        author = ctx.message.author
        embed = discord.Embed(title="{}'s info".format(ctx.message.author.name), description="{}".format(ctx.message.author.mention), color=0x00ff00)
        embed.add_field(name="Name:", value=ctx.message.author.name, inline=True)
        embed.add_field(name="Nickname:", value=ctx.message.author.display_name, inline=True)
        embed.add_field(name="ID:", value=ctx.message.author.id, inline=True)
        embed.add_field(name="Status:", value=ctx.message.author.status, inline=True)
        embed.add_field(name="Highest Role:", value=ctx.message.author.top_role)
        embed.add_field(name="Account Created: ", value=ctx.message.author.created_at, inline=True)
        embed.add_field(name="Joined at:", value=ctx.message.author.joined_at)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(icon_url=author.avatar_url, text="Helpful commands!")
        await client.say(embed=embed)
        
    else:
        author = user
        embed = discord.Embed(title="{}'s info".format(user.name), description="Here's the info.", color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="Nickname:", value=user.display_name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        embed.add_field(name="Account Created: ", value=user.created_at, inline=True)
        embed.add_field(name="Joined at:", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(icon_url=author.avatar_url, text="Helpful commands!")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's the info.", color=0x00ff00)
    embed.set_author(name="Server Info:")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await client.say(embed=embed)
    return 

@client.command(pass_context=True)
async def stats(ctx):
    now = datetime.utcnow()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="Stats", value=f"Connected to {len(client.servers)} servers")
    embed.add_field(name="Avaliable to:", value = f"*{len(set(client.get_all_members()))}* users")
    embed.add_field(name="WrongBot's Uptime", value=f"I've been online for **{elapsed.days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds")
    await client.say(embed=embed)
  
@client.command(pass_context=True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await client.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(title="My ping:", description='*Latency: {}ms*'.format(round((t2-t1)*1000)), color=0x00ff00)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def credits(ctx):
    author = ctx.message.author
    embed = discord.Embed(color = 0x00ff00)
    embed.set_author(name = "Below are some people who helped with the bot development :D")
    embed.add_field(name = "Savage#5185", value = "-helped with .json files, some of these commands won't be possible without him")
    embed.add_field(name = "TheRedMammon#2485", value = "- helps with debugging errors")
    await client.say(embed=embed)               
    
@client.command(pass_context=True)
async def invite(ctx):
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="Click here to invite me！", value = "[here](https://discordbots.org/bot/492031267483811850)", inline = False)
    embed.set_footer(text = "Don't forget to upvote me ;D")
    await client.say(embed=embed)    
    
@client.command(pass_context=True)
async def timer(ctx, time=None):
    if time is None:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':x: **Error**', value='Please specify the amount of second!', inline=False)
        await client.say(embed=embed)
    channel = ctx.message.channel
    author = ctx.message.author
    message = []
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=':stopwatch: Timer!:', value='Timer set for **{}** seconds'.format(int(time), inline=True))
    embed.set_footer(text='Timer:')
    await client.say(embed=embed)
    await asyncio.sleep(int(time))
    msg=await client.say('{}'.format(author.mention))
    await client.delete_message(msg)
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=':stopwatch:', value='Time is up **{}**'.format(author.name), inline=True)
    embed.set_footer(text='Timer:')
    await client.say(embed=embed)       
        
#Music
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say("Joined")

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say("Left")

players = {}
@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
    await client.say("Playing")

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.say("Paused")

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    await client.say("Stopped")

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await client.say("Resumed")

 #Giveaway
@client.command(pass_context = True)
async def giveaway(ctx):
    if ctx.message.author.server_permissions.manage_server:
        if ctx.message.author.bot:
            await client.say("Bots can't use commands.")
            return
        """Create a giveaway throught an interactive setup!"""
        await client.say(":tada: WooHoo!!!! We will create your giveaway :tada:")
        await asyncio.sleep(1)
        await ctx.bot.say("What channel will the giveaway be held in?\n"
                        "\n"
                        "`Ex. Type a channel name in your server. ('general' not #general)`")
        channel_name = await client.wait_for_message(author = ctx.message.author)
        g_channel = discord.utils.get(ctx.message.server.channels, name = channel_name.content)
    
        #Check if the channel even exists!
        if not g_channel:
            await client.say(":x: | Channel Not Found!")
        if g_channel:
            await client.say(":white_check_mark: | Channel Selected!")
            await asyncio.sleep(1)
            await client.say("How long will the giveaway be?\n"
                            "\n"
                            "Ex. 5 Minutes, say 5m, 1 Hour, say 1h, etc. (Please use whole numbers only!")
            duration = await client.wait_for_message(author = ctx.message.author)
            await asyncio.sleep(1)
            await client.say(":tada: Giveaway set to end {} after the start".format(duration.content))
            await asyncio.sleep(1)
            await client.say("How many winner will be selected?\n"
                              "\n"
                              "`Pick 1 (More Winners Coming Soon!)`")
            msg = await client.wait_for_message(author = ctx.message.author)
            g_winners = int(msg.content)
            await asyncio.sleep(1)
            await client.say(":tada: {} winner(s) will be chosen".format(g_winners))
            await asyncio.sleep(1)
            await client.say("What are you giving away?\n"
                            "\n"
                            "`This will become to title of the giveaway`\n"
                            "`Ex. Free Steam Keys`")
            g_prize = await ctx.bot.wait_for_message(author = ctx.message.author)
            await asyncio.sleep(1)
            await client.say("Giving away {}".format(g_prize.content))
            await asyncio.sleep(1)
            await client.say(":tada: Almost done, please confirm the following:")
            await asyncio.sleep(1)
            await client.say("You are Giving away `{}` with `{}` Winners, that will Last `{}`?\n"
                            "\n"
                            "`Respond 'Yes' if this is correct, if not respond 'No'`".format(g_prize.content, g_winners, duration.content))
            response = await client.wait_for_message(author = ctx.message.author, channel = ctx.message.channel)
            response = response.content.lower()

            duration = duration.content

            unit = duration[-1]
            if unit == 's':
                time = int(duration[:-1])
                longunit = 'seconds'
            elif unit == 'm':
                time = int(duration[:-1]) * 60
                longunit = 'minutes'
            elif unit == 'h':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'hours'
            else:
                return

            yesres = 'yes'
            nores = 'no'
            if response.lower() == nores.lower():
                await asyncio.sleep(1)
                await client.say(":x: | Giveaway Canceled")
            if response.lower() == yesres.lower():
                await client.say(":tada: Giveaway Started! :tada:")

                color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
                color = int(color, 16)
                embed=discord.Embed(title=":tada: __**Giveaway: {}**__ :tada:".format(g_prize.content), colour = discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
                embed.add_field(name = "Prize: ",value = "{}".format(g_prize.content))
                embed.add_field(name = "Winners: ", value = "{} Winner(s)".format(g_winners))
                embed.add_field(name = "Time: ", value = "{}".format(duration), inline = True)
                embed.set_footer(text = "React to join! ")
                give_away = await client.send_message(g_channel, embed = embed)
                ga_message = await client.add_reaction(give_away, "\U0001f389")
                await asyncio.sleep(time)#Sleep for the duration

                ga_message = await client.get_message(give_away.channel, give_away.id)
                ga_users=[]
                for user in await client.get_reaction_users(ga_message.reactions[0]):
                    ga_users.append(user.mention)
                ga_client = ctx.message.server.get_member('492031267483811850') #Put your bot id here for this to pull it.
                ga_users.remove(ga_client.mention)
                if len(ga_users) == 0:
                    error = discord.Embed(title=":warning: Rip",description="The giveaway ended with no participants, could not determine a winner",color=0xff0000)
                    await client.say(embed=error)
                else:
                    winner_list=[]
                    for loop in range(g_winners):
                        winner = random.choice(ga_users)
                        ga_users.remove(winner)
                        winner_list.append(winner)
                        msg = ""
            
                color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])#Winning Embed
                color = int(color, 16)
                embed=discord.Embed(title=":tada: __**Giveaway Ended!**__ :tada:", colour = discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
                embed.add_field(name = "Winners: ", value = "{} Winner(s)".format(g_winners))
                embed.add_field(name = "Winner List: ", value = ",\n".join(winner_list))
                embed.add_field(name = "Prize: ", value = "{}".format(g_prize.content))
                embed.set_footer(text = "Better Luck Next Time! Ended.")
                await client.edit_message(give_away, embed = embed)
                for winner in winner_list:
                    msg += ", " + winner
                await client.send_message(g_channel, ":tada: " + ", ".join(winner_list) + " won **{}**".format(g_prize.content))
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
        embed.add_field(name=":x: Error", value="You are missing the following permission: ```Manage Server```", inline=False)
        await client.say(embed=embed)
                
#Economy
@client.command(pass_context=True)
@commands.cooldown(1, 120, commands.BucketType.user)
async def work(ctx):
    with open("economy.json", "r") as f:
       	coins = json.load(f)
    author = ctx.message.author
    coinsc = random.randint(1, 100)
    if not ctx.message.server.id in coins:
       	coins[ctx.message.server.id] = {}
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coins[ctx.message.server.id][author.id] += coinsc
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name=":dollar: | Payment amount:", value=f"${coinsc}", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text="Economy Commands!")
    await client.say(embed=embed)
    with open("economy.json", "w") as f:
        json.dump(coins, f, indent=4)

@work.error
async def cooldown_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        author = ctx.message.author
        embed = discord.Embed(color=0x1434a3)
        embed.add_field(name="Calm Down!", value="Work command is on cooldown for 2 minutes.")
        embed.set_footer(icon_url=author.avatar_url, text="Economy Commands!")
        await client.say(embed=embed)
       
@client.command(pass_context=True)
async def bal(ctx):
    with open("economy.json", "r") as f:
        coins = json.load(f)
    author = ctx.message.author
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coinss = coins[ctx.message.server.id][author.id]
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="<:dollar: | Your balance:", value=f"${coinss}", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text="Economy Commands!")
    await client.say(embed=embed)       
            
#Moderation commands
@client.command(pass_context=True)
async def nickname(ctx, member: discord.User=None, *, newnick=None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_nicknames:
            if member is None:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=':x: Error:', value='```Please specify a user!```', inline=False)
                embed.set_footer(icon_url=author.avatar_url, text="| Utility commands!")
                await client.say(embed=embed)
            
        else:
            embed = discord.Embed(color=0xff0200)
            embed.add_field(name=':x: Error', value='You are missing the following permission: ``Manage Nicknames``', inline=False)
            embed.set_footer(icon_url=author.avatar_url, text='You cant use this command!')
            await client.say(embed=embed)
            
        await client.change_nickname(member, newnick)
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name='Changed:', value=f"You have changed {member.name}'s name to `{newnick}`", inline=True)
        embed.set_footer(icon_url=author.avatar_url, text="| Utility commands!")
        await client.say(embed=embed) 
            
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(name="Something went wrong ;-;")
        embed.add_field(name=":x: Error", value="I'm missing the following permission: ```Manage Nicknames```", inline=False)
        embed.set_footer(icon_url=author.avatar_url, text=f"Make sure my role is higher than {author.name}, that can be another error ;-;")
        await client.say(embed=embed)

    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, I can't nickname other bots at the moment ;-;")
        await client.say(embed=embed)    
        
@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear (ctx, amount=100):
  if ctx.message.author.server_permissions.manage_messages:
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
      messages.append(message)
    await client.delete_messages(messages)
    await client.say('Message cleared')
    return 

@client.command(pass_context=True)
async def addrole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            role = discord.utils.get(ctx.message.server.roles, name=name)
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
                embed.add_field(name=":x: Error", value="Please specify a user!", inline=False)
                embed.set_footer(text=f"Error Created by: {author.name}")
                await client.say(embed=embed)
                return
            if role is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Unknown role!")
                embed.add_field(name=":x: Error", value=f"You made an mistake! ```Error: No role called: {name}```")
                await client.say(embed=embed)
                return
            await client.add_roles(user, role)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role added!")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
            embed.add_field(name=":x: Error", value="You are missing the following permission: ```Manage Roles```", inline=False)
            await client.say(embed=embed)
            
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar.url, name="An error had occured!")
        embed.add_field(name=":x: Error", value="I'm missing the following permission: ```Manage Roles```", inline=False)
        await client.say(embed=embed)
                      
@client.command(pass_context=True)
async def removerole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            role = discord.utils.get(ctx.message.server.roles, name=name)
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
                embed.add_field(name=":x: Error", value="Please specify a user!", inline=False)
                embed.set_footer(text=f"Error Created by: {author.name}")
                await client.say(embed=embed)
                return
            if role is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
                embed.add_field(name=":x: Error", value=f"You made an mistake! Makes sure you specify the role exactly how it's named. ```Error: No role called; {name}```")
                await client.say(embed=embed)
                return
            await client.remove_roles(user, role)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role removed")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing the following permission: ```Manage Roles```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="An error had occured!")
        embed.add_field(name=":x: Error", value="I'm missing the following permission: ```Manage Roles```", inline=False)
        await client.say(embed=embed)
 
@client.command(pass_context=True)
async def mute(ctx, user: discord.Member = None):
    try:
        if ctx.message.author.server_permissions.mute_members:
            MutedRole = discord.utils.get(ctx.message.server.roles, name="Muted")
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error", value="Please specify a user!")
                await client.say(embed=embed)
                return
            if MutedRole is None:
                embed = discord.Embed(color=0xff0200)
                author = ctx.message.author
                embed.set_author(icon_url=author.avatar_url, name="Role not found")
                embed.add_field(name=":x: Error", value="Make sure you set up a role named 'Muted' with the right permission")
                await client.say(embed=embed)
                return
            await client.add_roles(user, MutedRole)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name=":white_check_mark: Sucessful!", value="User muted")
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            embed.add_field(name="User ID:", value=f"{user.id}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing the following permission: ```Mute Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
        embed.add_field(name=":x: Error", value="I'm missing the following permission: ```Mute Members```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry for thr inconvience, an unexpected error had occured ;-;")
        await client.say(embed=embed)
        
@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member = None):
    try:
        if ctx.message.author.server_permissions.mute_members:
            MutedRole = discord.utils.get(ctx.message.server.roles, name="Muted")
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error", value="Please specify a user!")
                await client.say(embed=embed)
                return
            
            if MutedRole is None:
                embed = discord.Embed(color=0xff0200)
                author = ctx.message.author
                embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
                embed.add_field(name=":x: Error", value="User dosen't have the 'Muted' role.")
                await client.say(embed=embed)
                return
            
            await client.remove_roles(user, MutedRole)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name=":white_check_mark: Sucessful!", value="User unmuted")
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            embed.add_field(name="User ID:", value=f"{user.id}", inline=False)
            await client.say(embed=embed)
            
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
            embed.add_field(name=":x: Error", value="You are missing the following permissiom: ```Mute Members```", inline=False)
            await client.say(embed=embed)
            
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="An error had occured ;-;")
        embed.add_field(name=":x: Error", value="I'm missing the following permission: ```Mute Members```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry for the inconvience. An unexpected error occured ;-;")
        await client.say(embed=embed)      
        
@client.command(pass_context=True)
async def kick(ctx, user: discord.Member = None, *, reason = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.kick_members or ctx.message.author.id == "365977869903593483":
            if ctx.message.author.bot:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error:", value="This command is blocked for bots.")
                embed.set_footer(icon_url=author.avatar_url, text="Error created by: {}".format(author.name))
                await client.say(embed=embed)
                return
            
            if author == user:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error: ", value="```You can't kick yourself```", inline=False)
                embed.set_footer(icon_url=author.avatar_url, text="| Moderation commands!")
                await client.say(embed=embed)
                return
            
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(name="Something went wrong ;-;")
                embed.add_field(name=":x: Error:", value="```Failed to specify a user```", inline=False)
                embed.set_footer(icon_url=author.avatar_url, text="| Moderation commands!")
                await client.say(embed=embed)
                return
            
            await client.kick(user)
            embed = discord.Embed(color=0x4e09ff)
            embed.set_author(name='Kicked {}'.format(user.name), inline=True)
            embed.add_field(name="User:", value=f"{user.mention}")
            embed.add_field(name="User ID:", value=f"**{user.id}**")
            embed.add_field(name='Reason:', value='{0}'.format(reason), inline=True)
            embed.set_footer(icon_url=user.avatar_url, text=f"Kicked by: {author.name}")
            await client.say(embed=embed)
            
        else:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(name="Something went wrong")
            embed.add_field(name=":x: Error", value="You are missing the following permission: ```Kick Members```", inline=False)
            await client.say(embed=embed)
            
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(name="Something went wrong ;-;")
        embed.add_field(name=":x: Error", value="I'm missing thr following permission: ```Kick Members```", inline=False)
        embed.set_footer(icon_url=author.avatar_url, text=f"Make sure my role is higher than {author.name}, that can be another error ;-;")
        await client.say(embed=embed)
        
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, I can't kick other bots at the moment ;-;")
        await client.say(embed=embed)
        
@client.command(pass_context=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    author = ctx.message.author
    server = ctx.message.server
    
    if ctx.message.author.server_permissions.ban_members or ctx.message.author.id == "365977869903593483":
        if user is None:
            embed = discord.Embed(color=0xff0000)
            embed.set_author(name='You made a error!')
            embed.add_field(name=' :no_entry_sign: **Error** :no_entry_sign:', value='Please specify a user!', inline=False)
            embed.set_footer(text='Try again')
            await client.say(embed=embed)
            return 
        
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name='Ban - Information')
            embed.add_field(name='Server:', value='**{}**'.format(server.name), inline=False)
            embed.add_field(name='Reason:', value='**{0}**'.format(reason), inline=True)
            embed.add_field(name='Admin:', value='**{}**'.format(author.name), inline=False)
            await client.send_message(user, embed=embed)
            await client.ban(user)
            #Sends the user a message when he is kicked!
            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name='Ban - Information')
            embed.add_field(name='Server:', value='**{}**'.format(server.name), inline=False)
            embed.add_field(name='Reason:', value='**{0}**'.format(reason), inline=True)
            embed.add_field(name='Admin:', value='**{}**'.format(author.name), inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            await client.say(embed=embed)
            return 
 
    else:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name=':no_entry_sign: **Error** :no_entry_sign:', value='You are missing the following permission: Ban member', inline=False)
        embed.set_footer(text='You cant use this command!')
        await client.say(embed=embed)
        return
        
@client.command(pass_context=True, hidden=True)
@commands.has_role("Owner")
async def debug(self, ctx, *, code : str):
    code = code.strip('` ')
    python = '```py\n{}\n```'
    result = None

    try:
        result = eval(code)
 
    except Exception as e:
        await client.say(python.format(type(e).__name__ + ': ' + str(e)))
        return
    
    if asyncio.iscoroutine(result):
        result = await result

    else:
        await client.say("Good job! No errors :D")
        
    await client.say(python.format(result))
        
starttime = datetime.utcnow()
client.loop.create_task(change_status())
client.run(os.environ.get('BOT_TOKEN'))
