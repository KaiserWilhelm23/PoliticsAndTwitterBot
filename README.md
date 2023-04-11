# PoliticsAndTwitterBot

Welcome to the Politcs & Twitter Discord Bot Code. This will always be open source!!!! 


# How it works

The Politcs & Twitter Discord Bot uses Python, and the ```discord.py``` library to connect to discord API's. This bot does not record or keep any of your account information. 


# The Commands

```

- !ping -> get bot response 
- !tweet [tweet] -> send a tweet
- !leak [title], [leak] -> send a leak use the , as a separator

```


# Ping Code:
```
@bot.command()
async def ping(ctx):
    print(f"command ping ran")
    await ctx.send(f'UP: ```{round(bot.latency * 1000)}ms```')
    
```

# Tweet Code 
Uses ```discord.embed``` to "simulate" tweets. 

```
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
```

# Leak Code 

```
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


```         
