import discord
from discord.ext import commands
from discord import Game, Embed
import requests


secret = open("secret.txt", "r")
token = secret.read()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.offline)
    await bot.change_presence(activity=Game(name="run !help for help. Version: ALPHA "))


@bot.command(name="ping")
async def ping(ctx):
    print(f"Command ping ran")
    await ctx.send(f'UP: {round(bot.latency * 1000)}ms')

@bot.command(name="tweet")
async def tweet(ctx, *, tweet_data):
    print(f"User: {ctx.author.display_name} tweeted, {tweet_data}")

    embed = discord.Embed(title=None, description=tweet_data, color=discord.Color.blue())
    embed.set_author(name=f"{ctx.author.display_name} ✅", icon_url=ctx.author.avatar)
    if len(ctx.message.attachments) > 0:
        embed.set_image(url=ctx.message.attachments[0].url)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@bot.command(name="leak")
async def leak(ctx, *, title_and_leak):
    title, leak = title_and_leak.split(",", 1)
    title = title.strip()
    leak = leak.strip()
    if not title or not leak:
        await ctx.send("Missing 'title' or 'leak': !leak [title], [leak]")
    else:
        print(f"User: {ctx.author.display_name} leaked, {leak}")
        embed = discord.Embed(title=title, description=leak, color=discord.Color.blue())
        if len(ctx.message.attachments) > 0:
            embed.set_image(url=ctx.message.attachments[0].url)
        msg = await ctx.send(embed=embed)


@bot.command(name="helpp")
async def help(ctx):
    await ctx.send("""
    Welcome to the Politics & Twitter bot
    
    !ping -> Get bot response
    !tweet [tweet_data] -> Send a tweet
    !leak [title], [leak] -> Send a leak (use ',' as a separator)
    !calc [numbers to calculate]
    !profile [displays public profile]
    """)


@bot.command(name="update")
async def update_app(ctx):
    update()
    await ctx.send("Politics & Twitter is updated!")
    print("[WARNING] Updated code and ready to redeploy")


def update():
    import requests

    url = 'https://raw.githubusercontent.com/blaze005/PoliticsAndTwitterBot/main/main.py'
    r = requests.get(url, allow_redirects=True)
    open('main.py', 'wb').write(r.content)


@bot.command(name="false_info")
async def false_info(ctx, *, tweet_data):
    print(f"Admin: {ctx.author.display_name} Stated, {tweet_data}")
    embed = discord.Embed(title="False Info", description=tweet_data, color=discord.Color.blue())
    msg = await ctx.send(embed=embed)


@bot.command(name="report")
async def report(ctx, user: discord.Member):
    reason_prompt = await ctx.send(f"Please provide a reason for reporting {user.mention}.")
    try:
        reason_msg = await bot.wait_for(
            "message",
            timeout=30,
            check=lambda message: message.author == ctx.author and message.channel == ctx.channel
        )
        reason = reason_msg.content
        report_embed = discord.Embed(
            title="User Report",
            description=f"Reported user: {user.mention}\nReporter: {ctx.author.mention}\nReason: {reason}",
            color=discord.Color.red()
        )
        report_channel = bot.get_channel("1057777518456881152")  # Replace with your report channel ID
        if report_channel is not None:
            try:
                await report_channel.send(embed=report_embed)
                await ctx.send(f"Thank you for reporting {user.mention}. Your report has been submitted.")
            except discord.Forbidden:
                await ctx.send("I don't have permission to send messages in the report channel.")
        else:
            await ctx.send("Report channel not found. Please make sure the ID is correct.")
    except asyncio.TimeoutError:
        await reason_prompt.delete()
        await ctx.send("Report cancelled. You took too long to provide a reason.")

@bot.command()
async def calc(ctx, user):
    try:
        result = eval(user)
        await ctx.send(f"```{result}```")
    except Exception as e:
        await ctx.send(e)


@bot.command(name="profile", description="Show a profile based on a mentioned user")
async def build_profile(ctx, user: discord.Member):
    avatar_url = str(user.avatar.url)

    embed = discord.Embed(title=f"Profile of {user.name}", color=discord.Color.blue())
    embed.set_author(name=user.display_name, icon_url=avatar_url)
    embed.add_field(name="Followers", value="1000")
    embed.add_field(name="Following", value="500")
    embed.add_field(name="Posts", value="100")

    follow_button = "Follow"
    view_button = "View Profile"

    embed.set_footer(text=f"Concept of User Profiles with Orbis Twitter Bot")

    message = await ctx.send(embed=embed)

    await message.add_reaction(follow_button)
    await message.add_reaction(view_button)

@bot.event
async def on_raw_reaction_add(payload):
    user_id = payload.user_id
    channel_id = payload.channel_id
    message_id = payload.message_id
    emoji = payload.emoji.name

    if emoji == "Follow":
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        user = message.guild.get_member(user_id)
        await message.channel.send(f"{user.mention} clicked the Follow button!")
    elif emoji == "View Profile":
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        user = message.guild.get_member(user_id)
        await message.channel.send(f"{user.mention} clicked the View Profile button!")


@bot.command()
async def check_va_steel(ctx):
    api_url = "https://politicsandwar.com/api/tradeprice/"
    resource = "steel"
    api_key = "66dd80abc7eb02"

    # Make the API request
    response = requests.get(api_url, params={"resource": resource, "key": api_key})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the price from the JSON response
        data = response.json()
        steel_price = data["avgprice"]
    else:
        await ctx.send("Failed to retrieve steel price. Status code: " + str(response.status_code))

    def calculate_stock_price(num_shares):
        # Data inputs
        world_price_per_ton = int(steel_price)
        tons_per_day = 650.02
        operating_days_per_year = 365
        num_steel_mills = 60
        cost_per_steel_mill = 45000
        operation_cost_steel_mill = 4000
        num_coal_mines = 82
        cost_per_coal_mine = 1000
        operation_cost_coal_mine = 400
        num_iron_mines = 89
        cost_per_iron_mine = 9500
        operation_cost_iron_mine = 1600

    # Calculate components
        annual_revenue = world_price_per_ton * tons_per_day * operating_days_per_year
        total_expenses = (num_steel_mills * operation_cost_steel_mill * operating_days_per_year) + \
                     (num_coal_mines * operation_cost_coal_mine * operating_days_per_year) + \
                     (num_iron_mines * operation_cost_iron_mine * operating_days_per_year)
        total_investment = (num_steel_mills * cost_per_steel_mill) + \
                       (num_coal_mines * cost_per_coal_mine) + \
                       (num_iron_mines * cost_per_iron_mine)

    # Calculate stock price per share
        stock_price_per_share = (annual_revenue - total_expenses) / total_investment

    # Calculate estimated stock price based on available shares
        estimated_stock_price = stock_price_per_share * num_shares

        return estimated_stock_price

    # Set the number of available shares
    num_available_shares = 300

    estimated_stock_price = calculate_stock_price(num_available_shares)
    await ctx.send(f"```Estimated stock price for Virginia Steel ( {str(num_available_shares)} total shares): ${str(round(estimated_stock_price, 2))}```")


bot.run(token)
