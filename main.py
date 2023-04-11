import discord
from discord.ext import commands
from discord import app_commands, ui 
from discord import Game


secret = open("secret.txt", "r")
token = secret.read()


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=Game(name="run !helpp for help. Version: ALPHA "))


@bot.command()
async def ping(ctx):
    print(f"command ping ran")
    await ctx.send(f'UP: ```{round(bot.latency * 1000)}ms```')

@bot.command()
async def tweet(ctx, *,tweet_data = None):
    if tweet_data == None:
        await ctx.send("No tweet: /tweet [text]") 
    else:
        await ctx.message.delete()
        print(f"User: {ctx.author.display_name} tweeted, {tweet_data}")
        embed = discord.Embed(title=None, description=tweet_data, color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        if len(ctx.message.attachments) > 0:
            embed.set_image(url=ctx.message.attachments[0].url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


@bot.command()
async def leak(ctx, *, title_and_leak=None):
    if title_and_leak is None:
        await ctx.message.delete()
        await ctx.send("Missing 'title' and 'leak': !leak [title], [leak]")
    else:
        title, leak = title_and_leak.split(",", 1)  # Split the input into title and leak
        title = title.strip()  # Remove any leading/trailing whitespace from title
        leak = leak.strip()  # Remove any leading/trailing whitespace from leak
        if not title or not leak:  # Check if either title or leak is empty
            await ctx.message.delete()
            await ctx.send("Missing 'title' or 'leak': !leak [title], [leak]")
        else:
            await ctx.message.delete()
            print(f"User: {ctx.author.display_name} leaked, {leak}")
            embed = discord.Embed(title=title, description=leak, color=discord.Color.blue())
            if len(ctx.message.attachments) > 0:
                embed.set_image(url=ctx.message.attachments[0].url)
            msg = await ctx.send(embed=embed)



help = """

Welcome to the Politics & Twitter bot

!ping -> get bot response 
!tweet [tweet] -> send a tweet
!leak [title], [leak] -> send a leak use the , as a separator
"""

@bot.command()
async def helpp(ctx):
    await ctx.send(help)






bot.run(token)