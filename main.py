
import discord
from discord.ext import commands
import json
import uuid
import os

def load_data():
    if not os.path.exists("whitelist.json"):
        with open("whitelist.json", "w") as f:
            json.dump([], f)
    if not os.path.exists("blacklist.json"):
        with open("blacklist.json", "w") as f:
            json.dump([], f)
    if not os.path.exists("keys.json"):
        with open("keys.json", "w") as f:
            json.dump([], f)

    with open("whitelist.json", "r") as f:
        whitelist = json.load(f)
    with open("blacklist.json", "r") as f:
        blacklist = json.load(f)
    with open("keys.json", "r") as f:
        keys = json.load(f)

    return whitelist, blacklist, keys

whitelist, blacklist, keys = load_data()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

ADMIN_ID = 1119698372853514381  # Replace with your Discord ID

@bot.command()
async def createkey(ctx):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("You do not have permission to create keys.")
        return
    new_key = str(uuid.uuid4())
    keys.append({"key": new_key, "redeemed": False})
    with open("keys.json", "w") as f:
        json.dump(keys, f)
    await ctx.send(f"New key created: {new_key}")

@bot.command()
async def redeem(ctx, key: str):
    if ctx.author.name in blacklist:
        await ctx.send("You are blacklisted and cannot redeem a key.")
        return
    for item in keys:
        if item["key"] == key and not item["redeemed"]:
            item["redeemed"] = True
            whitelist.append(ctx.author.name)
            with open("keys.json", "w") as f:
                json.dump(keys, f)
            with open("whitelist.json", "w") as f:
                json.dump(whitelist, f)
            await ctx.send(f"{ctx.author.name} has been whitelisted!")
            return
    await ctx.send("Invalid or already redeemed key.")

@bot.command()
async def blacklist(ctx, username: str):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("You do not have permission to blacklist users.")
        return
    if username in blacklist:
        await ctx.send(f"{username} is already blacklisted.")
        return
    blacklist.append(username)
    with open("blacklist.json", "w") as f:
        json.dump(blacklist, f)
    await ctx.send(f"{username} has been blacklisted.")

@bot.command()
async def check(ctx):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("You do not have permission to check the whitelist.")
        return
    await ctx.send("Whitelisted users:")

" + "
".join(whitelist))

import os
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
