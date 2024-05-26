import discord, json, requests, asyncio
from characterai import aiocai
from discord.ext import commands



bot = commands.Bot(command_prefix = 'th.', intents=discord.Intents.all())


config = json.load(open('config.json'))
chats = json.load(open('chats.json'))
char = config['cai-char-id']
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
    if user not in banished:
        banished.append(user)
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('❌')

@bot.command()
async def unbanish(ctx, user: discord.Member):
    if user in banished:
        banished.remove(user)
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('❌')


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
        for i in chats.keys():
            embed.add_field(name=i, value=chats[i], inline=False)

        await ctx.send(embed=embed)
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
async def namelock(ctx, member: discord.Member, *, nick):
    if ctx.author.id in config['whitelisted-users']:
        try:
            namelocklist[str(member.id)] = nick
            await member.edit(nick=nick)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('❌')
            print(e)
    else:
        await ctx.message.reply("Get your perms up lil nigga 👺")


@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        if str(before.id) in namelocklist.keys():
            await before.edit(nick=namelocklist[str(before.id)])
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    start = False
    
    

    if (not slock or message.author.id in config['whitelisted-users']) and not message.author.voice and not message.author in banished:
        
        
        if message.reference:
            xmessage = await message.channel.fetch_message(message.reference.message_id)
            if xmessage.author.id == bot.user.id:
                start = True
        elif bot.user.mention in message.content:
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
                    ms.replace("<@993061478414438400>", "trap house lover")
                    
                async with await client.connect() as chat:
                    message2 = await chat.send_message(
                        char, chats[str(message.author.id)], ms
                    )

            await message.reply(message2.text)


    
    if niggasaidx:
        if message.author in niggasaidx:
            await message.reply(f"nigga said {message.content}")


    if message.author.voice and message.author.voice.channel and not message.author in banished:
        msx = message.content
        ctx = await bot.get_context(message)    
        
        if "<@993061478414438400>" in msx:
            voice_state = message.author.voice
            voice_channel = voice_state.channel
            if not ctx.voice_client:
                await voice_channel.connect()

            await message.add_reaction('👂')


            me = await client.get_me()
            if str(message.author.id) not in chats.keys():
                    async with await client.connect() as chat:
                        response, answer = await chat.new_chat(char, me.id)
                    chats[str(message.author.id)] = response.chat_id
                    json.dump(chats, open('chats.json', 'w'))

            if "<@993061478414438400>" in message.content:
                    msx.replace("<@993061478414438400>", "trap house lover")
                    
            async with await client.connect() as chat:
                message2 = await chat.send_message(
                    char, chats[str(message.author.id)], msx
                )

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{config['elevenlabs-voice-id']}"

            headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config["elevenlabs-api-key"]
            }

            data = {
            "text": message2.text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
            }

            response = requests.post(url, json=data, headers=headers)
            with open('output.mp3', 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            ctx.voice_client.play(discord.FFmpegPCMAudio('output.mp3'))




            
            






bot.run(config['discord-token'])