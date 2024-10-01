import discord, json, requests, asyncio, io, os
from characterai import aiocai
from discord.ext import commands



bot = commands.Bot(command_prefix = 'th.', intents=discord.Intents.all())


config = json.load(open('config.json'))
chats = json.load(open('chats.json'))
char = config['cai-char-id']
token = config['cai-token']
voiceid = config['voice-id']
client = aiocai.Client(config['cai-token'])



slock = False
niggasaidx = []
namelocklist = {}
banished = []



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')




@bot.command()
async def banish(ctx, user: discord.Member):
    if ctx.author.id in config['whitelisted-users']:
        if user not in banished:
            banished.append(user)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def unbanish(ctx, user: discord.Member):
    if ctx.author.id in config['whitelisted-users']:
        if user in banished:
            banished.remove(user)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def say(ctx, *, message):
    if ctx.author.id in config['whitelisted-users']:
        await ctx.message.delete()
        await ctx.send(message)
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")


@bot.command()
async def csay(ctx, channel: discord.TextChannel, *, message):
    if ctx.author.id in config['whitelisted-users']:
        try:
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('✅')
        await channel.send(message)
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def lock(ctx):
    global slock
    if ctx.author.id in config['whitelisted-users']:
        if not slock:
            slock = True
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def unlock(ctx):
    global slock
    if ctx.author.id in config['whitelisted-users']:
        if slock:
            slock = False
            await ctx.message.add_reaction('✅')
        if not slock:
            await ctx.message.add_reaction('❌')
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")
@bot.command()
async def listchat(ctx):
    if ctx.author.id in config['whitelisted-users']:
        embed = discord.Embed(title="chats")
        

        await ctx.reply(f"There are currently {len(chats)} chats 😈🚬")
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def newchat(ctx, id):
    if ctx.author.id in config['whitelisted-users']:
        me = await client.get_me()
        async with await client.connect() as chat:
            response, answer = await chat.new_chat(char, me.id)
        chats[str(id)] = response.chat_id
        json.dump(chats, open('chats.json', 'w'))
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def niggasaid(ctx, user: discord.User):
    global niggasaidx
    if ctx.author.id in config['whitelisted-users']:
        
        niggasaidx.append(user)
        await ctx.message.delete()
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")
@bot.command()
async def unniggasaid(ctx, user:discord.User):
    global niggasaidx
    if ctx.author.id in config['whitelisted-users']:
        
        niggasaidx.remove(user)
        await ctx.message.delete()
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def niggasaidlist(ctx):
    if ctx.author.id in config['whitelisted-users']:
        userstring = ""
        if niggasaidx and len(niggasaidx) > 0:
            for i in niggasaidx:
                username = i.mention
                if len(niggasaidx) > 1:
                    userstring = userstring + username + ", "
                else:
                    userstring = userstring + username + " "

            await ctx.reply(f"I say nigga said to {userstring}")
        else:
            await ctx.reply("Ion say nigga said to nobody")
        
quotex = []
emojix = ""
@bot.command()
async def quote(ctx, user: discord.User, emoji = ""):
    global quotex
    global emojix
    if ctx.author.id in config['whitelisted-users']:
        
        quotex.append(user)
        emojix = emoji
        await ctx.message.delete()
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")
@bot.command()
async def unquote(ctx, user:discord.User):
    global quotex
    if ctx.author.id in config['whitelisted-users']:
        
        quotex.remove(user)
        await ctx.message.delete()
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")


reactx = {}
@bot.command()
async def react(ctx, user: discord.User, emoji = ""):
    if ctx.author.id in config['whitelisted-users']:
        
        reactx[user.id] = emoji
        await ctx.message.delete()
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")


@bot.command()
async def unreact(ctx, user: discord.User, emoji = ""):
    if ctx.author.id in config['whitelisted-users']:
        
        reactx.pop(user.id)
        await ctx.message.delete()
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def namelock(ctx, member: discord.Member, *, nick):
    if ctx.author.id in config['whitelisted-users']:
        try:
            namelocklist[str(member.id)] = nick
            await member.edit(nick=nick)
            await ctx.message.delete()
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def unnamelock(ctx, member: discord.Member):
    if ctx.author.id in config['whitelisted-users']:
        try:
            # remove user from namelock list
            namelocklist.pop(str(member.id))
            await member.edit(nick=member.name)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def panic(ctx):
    global niggasaidx
    global quotex
    global reactx
    if ctx.author.id in config['whitelisted-users']:
        try:
            niggasaidx = []
            quotex = []
            reactx = []
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❌')

    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

vcblock = []

@bot.command()
async def vcban(ctx, user: discord.Member):
    global vcblock
    if ctx.author.id in config['whitelisted-users']:
        try:
            if user.voice is not None and user.voice.channel is not None:
                await user.move_to(None)
                
            
            if user.id in vcblock or user.id in config['whitelisted-users']:
                await ctx.message.add_reaction('❌')
                return
            vcblock.append(user.id)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)

    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")


@bot.command()
async def unvcban(ctx, user: discord.Member):
    global vcblock
    if ctx.author.id in config['whitelisted-users']:
        try:
            
                
            
            if user.id not in vcblock:
                await ctx.message.add_reaction('❌')
                return
            vcblock.remove(user.id)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)

    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

vcdisabled = False

@bot.command()
async def togglevc(ctx):
    if ctx.author.id in config['whitelisted-users']:
                
        global vcdisabled
        vcdisabled = not vcdisabled
        
        await ctx.message.add_reaction('✅')
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()
       
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.event
async def on_voice_state_update(member, before, after):
    global vcblock
    if before.channel is None and after.channel is not None:
        if member.id in vcblock:
            await member.move_to(None)


@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        if str(before.id) in namelocklist.keys():
            await before.edit(nick=namelocklist[str(before.id)])

softbanx = []

@bot.command()
async def softban(ctx, user: discord.Member):
    global softbanx
    if ctx.author.id in config['whitelisted-users']:
        try:
                         
            
            if user.id in softbanx or user.id in config['whitelisted-users']:
                await ctx.message.add_reaction('❌')
                return
            softbanx.append(user.id)
            vcblock.append(user.id)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)

    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

@bot.command()
async def unsoftban(ctx, user: discord.Member):
    global softbanx
    if ctx.author.id in config['whitelisted-users']:
        try:
                         
            
            if user.id not in softbanx or user.id in config['whitelisted-users']:
                await ctx.message.add_reaction('❌')
                return
            softbanx.remove(user.id)
            vcblock.remove(user.id)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)

    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")

def cleanup():
    os.remove('output.mp3')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    start = False
    refmsgc = None
    global vcdisabled
    

   
       
    try: 
        if (not slock or message.author.id in config['whitelisted-users']) and not message.author.voice and not message.author in banished and not message.author in niggasaidx and not message.author in quotex and not message.author == bot: 
            
            
            if message.reference:
                xmessage = await message.channel.fetch_message(message.reference.message_id)
                if xmessage.author.id == bot.user.id:
                    start = True
                refmsgc = xmessage.content
            if bot.user.mention in message.content:
                start = True


            if start:
                me = await client.get_me()
                ctx = await bot.get_context(message)
                if str(message.author.id) not in chats.keys():
                        async with await client.connect() as chat:
                            response, answer = await chat.new_chat(char, me.id)
                        chats[str(message.author.id)] = response.chat_id
                        json.dump(chats, open('chats.json', 'w'))       

                async with ctx.typing(): 
                    ms = message.content
                    if "<@993061478414438400>" in ms:
                        ms = ms.replace("<@993061478414438400>", "trap house lover")
                    if refmsgc: 
                        ms = f'"{refmsgc}"' + " " + ms
                    
                    
                    
                    image_url = None
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            if attachment.content_type and attachment.content_type.startswith('image/'):
                                image_url = attachment.url
                                                            
                                break

                    async with await client.connect() as chat:
                        message2 = await chat.send_message(
                            char=char, chat_id=chats[str(message.author.id)], text=ms, image=image_url
                        )

                await message.reply(message2.text)


        
        if niggasaidx:
            if message.author in niggasaidx:
                msga = message.content + " "
                if message.attachments:
                    
                    for attachment in message.attachments:
                        msga += attachment.filename + " "
                    
                await message.reply(f"nigga said {msga}")

        if quotex:
            if message.author in quotex:
                msga = message.content + " "
                if message.attachments:
                    
                    for attachment in message.attachments:
                        msga += attachment.filename + " "
                    
                await message.reply(f'"{msga}" {emojix}')

        if softbanx:
            if message.author.id in softbanx:
                await message.delete()

        if reactx:
            await message.add_reaction(reactx[message.author.id])


        if message.author.voice and message.author.voice.channel and not message.author in banished and not message.author in niggasaidx and not vcdisabled:
            ctx = await bot.get_context(message)    

            if message.reference:
                xmessage = await message.channel.fetch_message(message.reference.message_id)
                if xmessage.author.id == bot.user.id:
                    start = True
                refmsgc = xmessage.content
            if bot.user.mention in message.content:
                start = True
            
            if start:
                voice_state = message.author.voice
                voice_channel = voice_state.channel
                if not ctx.voice_client:
                    await voice_channel.connect()

            
            
                

                async with ctx.typing(): 
                    await message.add_reaction('👂')
                    me = await client.get_me()
                    if str(message.author.id) not in chats.keys():
                            print("not in chat key")
                            async with await client.connect() as chat:
                                response, answer = await chat.new_chat(char, me.id)
                            chats[str(message.author.id)] = response.chat_id
                            json.dump(chats, open('chats.json', 'w'))

                    

                    mc = message.content

                    if "<@993061478414438400>" in mc:
                            mc = mc.replace("<@993061478414438400>", "trap house lover")
                    if refmsgc: 
                            mc = f'"{refmsgc}"' + " " + mc


                    
                    image_url = None
                    if len(message.attachments) > 0:
                        print("has image")
                        for attachment in message.attachments:
                            if attachment.content_type and attachment.content_type.startswith('image/'):
                                image_url = attachment.url
                                                            
                                break
                            
                    async with await client.connect(token) as chat:
                        datax = await chat.send_message(
                                    char=char, chat_id=chats[str(message.author.id)], text=mc, image=image_url
                                )
                        text = datax.text
                        datax = datax.model_dump()
                        audio = requests.post("https://neo.character.ai/multimodal/api/v1/memo/replay", headers={"Authorization": f"Token {token}"}, json={"roomId":datax['turn_key']['chat_id'], "turnId":datax['turn_key']['turn_id'], "candidateId":datax['candidates'][0]['candidate_id'], "voiceId":voiceid})
                        
                ctx.voice_client.play(discord.FFmpegPCMAudio(audio.json()["replayUrl"]))
                        
                await message.reply(text)
    except Exception as e:
        print(e)


                


bot.run(config['discord-token'])
