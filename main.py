import subprocess
import sys
import os

# Function to install dependencies if not already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to check and install discord.py and requests
def check_and_install_dependencies():
    try:
        import discord
    except ImportError:
        print("discord.py not found, installing...")
        install("discord.py")

    try:
        import requests
    except ImportError:
        print("requests not found, installing...")
        install("requests")

# Ensure dependencies are installed before continuing
check_and_install_dependencies()

# Now proceed with importing the rest of the modules after installation
import discord
from discord.ext import commands
import time
import re
import asyncio

# Configuration
DISCORD_BOT_TOKEN = "MTMyMTA1MzM4MjMxMTU0MjgzNA.Gc2vvh.xZWpCwVl08RBKxhsbRHVXCzw6cqr_0FDxOPImA"
WEBHOOK_ONLINE = "https://discord.com/api/webhooks/1321363206324883476/k5a_f6M4Y4NePdH4r-mmKODvZphqN_W6lAyuoehyROLjVZ4wufCaf7E-gKBmD61hM0mp"
WEBHOOK_OFFLINE = "https://discord.com/api/webhooks/1321363318161674291/dwTv3tyQVx3C2iaLGR7kiTG2SOrLi4TWmGWxUVUv1o1nAl-KuPVXKktK9xjbabzQdMG8"
WEBHOOK_DELETED_ACCOUNT = "https://discord.com/api/webhooks/1314394635170484244/gYKV3DPJYZ8LEgvHLMhy78P3h5ty1LrlROajD2np1xOVyRA-ILbSAVsm-qEWf4kV5bIT"

# Define the updated stock files, including the new ccn.txt file
STOCK_FILES = [
    "microsoft.txt",
    "paypal.txt",
    "random.txt",
    "randomv1.txt",
    "roblox.txt",
    "twitter.txt",
    "valorant.txt",
    "ccn.txt"  # Changed from cnn.txt to ccn.txt
]

# Initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure this is enabled for reading message content

# Initialize the bot with the '.' prefix
bot = commands.Bot(command_prefix='.', intents=intents)

# Track bot uptime
bot_uptime = None

@bot.event
async def on_ready():
    global bot_uptime
    bot_uptime = time.time()  # Set the bot's uptime to the current time when it goes online

    # Calculate the uptime duration
    uptime_duration = time.time() - bot_uptime
    days, remainder = divmod(uptime_duration, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Prepare the webhook payload for online status
    data = {
        "content": "I DONT FEEL NO PAIN 👹 - Bot Status",
        "embeds": [
            {
                "title": "Bot is online and running.",
                "color": 0x00FF00,  # Green color
                "fields": [
                    {"name": "ONLINE STATUS", "value": "🟢", "inline": True},
                    {"name": "ONLINE DURATION", "value": f"Days: {int(days)} | Hours: {int(hours)} | Minutes: {int(minutes)} | Seconds: {int(seconds)}", "inline": True},
                    {"name": "Author", "value": "EL DIABLO FREE GEN", "inline": True}
                ]
            }
        ]
    }

    # Send the webhook for online status
    try:
        requests.post(WEBHOOK_ONLINE, json=data)
        print(f"Bot is online. Duration: {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s")
    except Exception as e:
        print(f"Failed to send webhook for online status: {e}")

@bot.event
async def on_disconnect():
    global bot_uptime

    # Calculate the uptime duration
    uptime_duration = time.time() - bot_uptime
    days, remainder = divmod(uptime_duration, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Prepare the webhook payload for offline status
    data = {
        "content": "Bot is offline.",
        "embeds": [
            {
                "title": "Bot is offline.",
                "color": 0xFF0000,  # Red color
                "fields": [
                    {"name": "OFFLINE STATUS", "value": "🔴", "inline": True},
                    {"name": "OFFLINE DURATION", "value": f"Days: {int(days)} | Hours: {int(hours)} | Minutes: {int(minutes)} | Seconds: {int(seconds)}", "inline": True},
                    {"name": "Author", "value": "EL DIABLO FREE GEN", "inline": True}
                ]
            }
        ]
    }

    # Send the webhook for offline status
    try:
        requests.post(WEBHOOK_OFFLINE, json=data)
        print(f"Bot is offline. Duration: {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s")
    except Exception as e:
        print(f"Failed to send webhook for offline status: {e}")

@bot.command()
async def gen(ctx, stock: str):
    """Generate an account for the given stock and DM the user."""
    try:
        stock_file = f"{stock}.txt"
        if stock_file not in STOCK_FILES:
            await ctx.reply(embed=make_error_embed(f"Invalid stock name. Available stocks are: {', '.join(STOCK_FILES)}"))
            return

        if not os.path.exists(stock_file):
            await ctx.reply(embed=make_error_embed(f"Stock file `{stock}.txt` not found."))  
            return

        with open(stock_file, "r") as file:
            available_stocks = [line.strip() for line in file if line.strip()]  # Remove empty lines

        if not available_stocks:
            await ctx.reply(embed=make_error_embed(f"No available accounts in `{stock}.txt`.")) 
            return

        # Select the first available account
        account = available_stocks.pop(0)

        # If the stock file is "ccn.txt", use the new format: card_number|month|year|cvv (no spaces)
        if stock_file == "ccn.txt":
            account_parts = account.split('|')
            if len(account_parts) == 4:
                card_number, month, year, cvv = account_parts
                account_info = (
                    f"Card Number: {card_number}\n"
                    f"Expiry Date: {month}/{year}\n"
                    f"CVV: {cvv}"
                )
            else:
                account_info = "Invalid account format in ccn.txt."
        elif stock_file == "roblox.txt":
            match = re.search(r"Username: (\S+)\s*\| Password: (\S+)", account)
            if match:
                username = match.group(1)
                password = match.group(2)
                account_info = f"Username: {username}\nPassword: {password}"
            else:
                account_info = "Invalid account format in roblox.txt."
        else:
            # Default format for other stocks: username:password
            account_info = f"Username: {account.split(':')[0]}\nPassword: {account.split(':')[1]}"

        # Update the stock file without the used account (write all accounts at once)
        with open(stock_file, "w") as file:
            file.writelines(f"{item}\n" for item in available_stocks)

        # Send a webhook to notify that the account has been deleted
        send_deleted_account_webhook(account, stock)

        # Log the command usage with username, user ID, and timestamp
        os.makedirs("res/logs", exist_ok=True)
        with open("res/logs/genLogs.txt", "a") as file:
            log_message = f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) generated {stock} at {time.ctime()}\n"
            file.write(log_message)

        # Send account details via DM
        embed = discord.Embed(
            title="Account Generated",
            description=f"Here are your account details for **{stock}**.",
            color=0xFF0000  # Red color in hexadecimal
        )
        embed.add_field(name="Account Details", value=account_info, inline=False)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

        # Use asyncio to send the DM and reply in the channel concurrently
        async def send_dm_and_reply():
            await ctx.author.send(embed=embed)
            embed_msg = discord.Embed(
                title="EL DIABLO FR",
                description=( 
                    "**CHECK YOUR DMs**\n"
                    f"**{ctx.author.mention}**\n"
                    "**If you do not receive the message, please unlock your private!**\n\n"
                    "**VOUCH**\n"
                    f"*If it works, kindly vouch us here*"
                    "<#1321125989002252299>\n"
                ),
                color=0xFF0000  # Red color in hexadecimal
            )
            await ctx.reply(embed=embed_msg)

        await asyncio.gather(send_dm_and_reply())  # Run both tasks concurrently

    except Exception as e:
        await ctx.reply(embed=make_error_embed(e))

def send_deleted_account_webhook(account, stock):
    """Send a webhook notification when an account is deleted."""
    data = {
        "content": "An account has been deleted from the stock.",
        "embeds": [
            {
                "title": f"Deleted Account from {stock}",
                "color": 0xFF0000,  # Red color
                "fields": [
                    {"name": "Account Details", "value": account, "inline": False},
                    {"name": "Stock", "value": stock, "inline": True},
                ]
            }
        ]
    }
    try:
        requests.post(WEBHOOK_DELETED_ACCOUNT, json=data)
    except Exception as e:
        print(f"Failed to send webhook for deleted account: {e}")

def make_error_embed(error):
    """Create an embed for error messages."""
    embed = discord.Embed(
        title="Error",
        description=f"An error occurred: {error}",
        color=0xFF0000  # Red color in hexadecimal
    )
    return embed

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
    
