#insert shebang here
from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import find
from discord import FFmpegPCMAudio
import random

#setup
TOKEN = "yep this is a token"
client = commands.Bot(command_prefix = '.', help_command=None, description='.help for commands', case_insensitive=True)
@client.event
async def on_ready():
    activity = discord.Activity(name="You Say Run", type=discord.ActivityType.listening, url="https://open.spotify.com/track/0hHc2igYYlSUyZdByauJmB?si=a04cc63d22ab4f8c")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("{0.user} Online.".format(client))

#when join server
@client.event
async def on_guild_join(ctx):
    await ctx.create_role(name="yousayrun",colour=discord.Colour(0x5cf3c6))
    channel = discord.utils.get(ctx.text_channels, name="general")
    general_id = channel.id
    general = client.get_channel(general_id)
    #general = find(lambda x: x.name == 'general', discord.TextChannel)
    # if general and general.permissions_for(server.me).send_messages:
    await general.send("Bot for playing you say run and pretty much only that (seemed funnier in my head).\nAnnoying features if you have the yousayrun role.\n.help for commands")

#main help command
@client.group(name='help', invoke_without_command=True, case_insensitive=True)
async def help(ctx):
    await ctx.send("```Commands:\n.join - join voice channel\n.leave - leave voice channel\n.hi - says 'Yo'\n.play - plays yousayrun\n.stop - stops yousayrun\n.pause - pauses yousayrun\n.resume - resumes yousayrun\n.yousayrun - gives yousayrun role\n.yousayrun remove - removes yousayrun role\n.help [command] for more help```")

#hi
@client.command()
async def hi(ctx):
    await ctx.send("Yo")
@help.command()
async def hi(ctx):
    await ctx.send("`.hi - just hi why would you need help`")

#join        
@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        # source = FFmpegPCMAudio('Accumula Town - Orchestrated.mp3')
        # voice.play(source)
    else: await ctx.send("You are not in a vc :(")
@help.command(pass_context = True)
async def join(ctx):
    await ctx.send("`.join - bot joins voice channel when you are in a vc`")
    
#leave
@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else: await ctx.send("Not in a vc :(")
@help.command()
async def leave(ctx):
    await ctx.send("`.leave - bot leaves voice channel when bot is in a vc`")




#music
#play music
@client.command(pass_context = True)
async def play(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    source = FFmpegPCMAudio('You Say Run.mp3')
    voice.play(source)
@help.command()
async def play(ctx):
    await ctx.send("`.play - plays yousayrun when bot is in a vc`")
    
#stop music
@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("No music playing :(")
@help.command()
async def stop(ctx):
    await ctx.send("`.stop - stops music when bot is playing music`")
        
#resume music
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No music paused :(")
@help.command()
async def resume(ctx):
    await ctx.send("`.resume - resumes music when bot music is paused`")
    
#pause music
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No music playing :(")
@help.command()
async def pause(ctx):
    await ctx.send("`.pause - pauses music when bot is playing music`")
    
#you say run?
@client.group(name='yousayrun', invoke_without_command=True, case_insensitive=True)
async def yousayrun(ctx):
    role = discord.utils.get(ctx.guild.roles,name="yousayrun")
    user = ctx.message.author
    if role in user.roles:
        await ctx.reply(f"you already have the yousayrun role")
    else: 
        await user.add_roles(role)
        await ctx.reply(f"you now have the yousayrun role")
@yousayrun.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles,name="yousayrun")
    user = ctx.message.author
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.reply(f"removed yousayrun role")
    else: 
        await ctx.reply(f"you do not have the yousayrun role")
@help.command()
async def yousayrun(ctx):
    await ctx.send("```.yousayrun - gives yousayrun role\n.yousayrun remove - removes yousayrun role```")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("you") or message.content.startswith("You") or message.content.startswith("say") or message.content.startswith("Say") or message.content.startswith("run") or message.content.startswith("Run"):
        if discord.utils.get(message.guild.roles,name="yousayrun") in message.author.roles:
                await message.channel.send("You say run?")
                if message.author.voice:
                    if discord.utils.get(client.voice_clients, guild=message.author.guild) is not None:
                        print("hi")
                        voice = discord.utils.get(client.voice_clients,guild=message.author.guild)
                        source = FFmpegPCMAudio('You Say Run.mp3')
                        voice.play(source)
                    channel = message.author.voice.channel
                    voice = await channel.connect()
                    source = FFmpegPCMAudio('You Say Run.mp3')
                    voice.play(source)
                elif (discord.utils.get(client.voice_clients, guild=message.author.guild)).is_connected():
                    voice = discord.utils.get(client.voice_clients,guild=message.author.guild)
                    source = FFmpegPCMAudio('You Say Run.mp3')
                    voice.play(source)
        else: await client.process_commands(message)
    # elif message.content == "you" or message.content == "You" or message.content == "say" or message.content == "Say" or message.content == "run" or message.content == "Run":
    #     await message.channel.send("You say run?")
    elif discord.utils.get(message.guild.roles,name="yousayrun") in message.author.roles:
        a = random.SystemRandom().randint(0 , 160)
        print(a)
        print(len(message.content))
        if a <= len(message.content):
            if message.author.voice:
                if discord.utils.get(client.voice_clients, guild=message.author.guild) is not None:
                    voice = discord.utils.get(client.voice_clients,guild=message.author.guild)
                    source = FFmpegPCMAudio('You Say Run.mp3')
                    voice.play(source)
                channel = message.author.voice.channel
                voice = await channel.connect()
                source = FFmpegPCMAudio('You Say Run.mp3')
                voice.play(source)
            elif (discord.utils.get(client.voice_clients, guild=message.author.guild)).is_connected():
                voice = discord.utils.get(client.voice_clients,guild=message.author.guild)
                source = FFmpegPCMAudio('You Say Run.mp3')
                voice.play(source)
            else: await client.process_commands(message)
        else: await client.process_commands(message)
    else: await client.process_commands(message)
   
  if __name__ == "__main__":
    client.run(TOKEN)
