token = ""
import discord
from discord.ext import commands
from discord import app_commands, ui 


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


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





bot.run(token)
