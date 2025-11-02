import discord
from discord.ext import commands
import asyncio
import threading
import random
import source_helper

TOKEN = source_helper.tf_token
CHANNEL = source_helper.ch_channel

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Required to access member join events
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.wait_until_ready()  # Await this function
    channel = bot.get_channel(CHANNEL)
    # if channel:
    #     await channel.send("Ooooh I'm the ghost of Kunihiro Yamada come to answer your questions...")
    # else:
    #     print("Channel not found.")

    for guild in bot.guilds:
        print(f"Guild: {guild.name}")
        for channel in guild.channels:
            print(f"Channel: {channel.name} - {channel.id}")
    # asyncio.create_task(func_select())

@bot.event
async def on_member_join(member):
    try:
        await bot.wait_until_ready()
        channel = bot.get_channel(1364062879271096414)
        if channel:
            await channel.send(f"Welcome, {member.name}. I will send you a DM shortly.")
        await member.send(f"Welcome to {member.guild.name}, {member.name}!  View the wordlists here: https://tksa.org")
        print(f"Sent a welcome message to {member.name}")
        role = discord.utils.get(member.guild.roles, name="Temporary Member")
        await member.add_roles(role)

    except Exception as e:
        print(f"Could not send DM to {member.name}: {e}")


@bot.command()
async def check_channel(ctx):
    await bot.wait_until_ready()
    channel = bot.get_channel(1364062879271096414)
    if channel:
        await ctx.send(f"Channel found: {channel.name}")
    else:
        await ctx.send("Channel not found.")

async def func_select():
    while True:
        selected_function = input("Select function\n" \
        "1 to send DM\n" \
        "2 to send message to selected channel: ")
        if selected_function == "1":
            await send_dm()
        elif selected_function == "2":
           await send_terminal_input()
        else:
            print("Invalid option.")

async def send_terminal_input():
    """ Continuously checks for terminal input and sends it to the channel. """
    while True:
        try:
            message = input("Enter a message to send: ")
            channel_select = input("Channel ID: ")
            if message:
                channel = bot.get_channel(channel_select)
                if channel:
                    await channel.send(message)
                else:
                    print(f"Channel with ID {channel_select} not found.")
        except Exception as e:
            print(f"Error sending message: {e}")


async def send_dm():
    """ Send a DM to a specific user by their ID. """
    while True:
        try:
            user_id = input("Enter the user ID to send a DM to: ")
            if user_id == "break".lower():
                break
            message = input("Enter the DM message: ")

            try:
                user = await bot.fetch_user(int(user_id))
                await user.send(message)
                print(f"Sent DM to {user.name}")
            except Exception as e:
                print(f"Error sending DM: {e}")

        except Exception as e:
            print(f"Error in DM input: {e}")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    print("Command serverinfo has been received")
    """Displays server information."""
    guild = ctx.guild  # The server (guild) where the command was invoked
    
    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.purple()
    )
    
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Member Count", value=guild.member_count)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Text Channels", value=len(guild.text_channels))
    embed.add_field(name="Voice Channels", value=len(guild.voice_channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    print("Command userinfo has been received")
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member.name}", color=discord.Color.blue())
    embed.add_field(name="User ID", value=member.id)
    embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="bothelp")
async def reply(ctx):
    print("Command help has been received")
    await ctx.message.reply("!userinfo for user info, \n" \
    "!serverinfo for server info.\n" \
    "!help for help (this message)\n"
    "!yamada for yamada\n"
    "!quote for quote\n"
    "!kytxt for a bit of information about Kunihiro Yamada\n")

@bot.command(name="yamada")
async def show_image(ctx):
    print("Command yamada has been received")
    file = discord.File("/home/server/Documents/yamada computer.png", filename="yamada computer.png")
    await ctx.send(file=file, content="Yamada")

@bot.command(name="kmtxt")
async def show_image(ctx):
    with open ("/home/server/Documents/kunihiroyamada.txt", "r") as file:
        contents = file.read()
        await ctx.channel.send(contents)


@bot.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == bot.user:
        return

    # Check if the bot is mentioned
    if bot.user in message.mentions:
        print("ping detected")
        await message.channel.send(f"Hello, {message.author.mention}! You pinged me?")
        await message.channel.send(f"Currently alive and well. Type !bothelp for commands.")

    if isinstance(message.channel, discord.DMChannel):
        dm_content = message.content
        await message.channel.send(f"You sent me a DM! {dm_content}")
        if dm_content in ["Kunihiro", "Yamada", "Kunihiro Yamada", "kunihiro", "yamada", "kunihiro yamada"]:
            with open ("/home/server/Documents/kunihiroyamada.txt", "r") as file:
                contents = file.read()
                await message.channel.send(contents)
    

    # Ensure other commands are processed
    await bot.process_commands(message)

@bot.command()
async def quote(ctx):
    await ctx.send(random.choice(quotes))


def start_terminal_input():
    asyncio.run(send_terminal_input())

def start_dm_input():
    asyncio.run(send_dm())

# Start the input functions in separate threads
# threading.Thread(target=start_terminal_input).start()
# threading.Thread(target=start_dm_input).start()

quotes = [
    "There is a treasure beyond infinity.",
    "Sorry. There is no treasure here. Look harder.",
    "My name is Kunihiro Yamada",
]


async def send_message_from_console(channel_id, message):
    channel = bot.get_channel(int(channel_id))
    if channel:
        await channel.send(message)
        print(f"Sent: {message}")
    else:
        print(f"Channel {channel_id} not found.")

def console_input_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        try:
            msg = input("Enter message: ")
            chan = input("Channel ID: ")
            asyncio.run_coroutine_threadsafe(
                send_message_from_console(chan, msg),
                bot.loop
            )
        except Exception as e:
            print(f"Error: {e}")

# Start thread
threading.Thread(target=console_input_thread, daemon=True).start()


bot.run(TOKEN)
