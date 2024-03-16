import discord
import yaml
import colorama
import time
import json

from discord.ext import tasks
from pymongo import MongoClient
from colorama import Fore

config = yaml.safe_load(open("config.yml").read())
client = MongoClient(config["MONGODB"]["URI"])

bot = discord.Bot()

def parseMessage(message, modality, type):
    kitmap_db, hcf_db = "KitMap", "HCF"

    try:
        if modality == "KitMap":
            db = client[kitmap_db]

            if type == 1: # Factions Top
                collection = db["teams"]
                results = collection.find({})
                playerFactions = []

                for document in results:
                    if document["teamType"] == "PLAYER":
                        playerFactions.append(document)
                
                sorted_factions = sorted(playerFactions, key=lambda x: int(x['points']), reverse=True)
                ftop1 = sorted_factions[0]
                ftop2 = sorted_factions[1]
                ftop3 = sorted_factions[2]

                message = message.replace("[faction1_name]", ftop1["name"])
                message = message.replace("[faction2_name]", ftop2["name"])
                message = message.replace("[faction3_name]", ftop3["name"])

                message = message.replace("[faction1_points]", ftop1["points"])
                message = message.replace("[faction2_points]", ftop2["points"])
                message = message.replace("[faction3_points]", ftop3["points"])

                return message

            if type == 2: # Leaderboards
                collection = db["users"]
                results = collection.find({})
                players = []

                for document in results:
                    players.append(document)
                
                sorted_factions = sorted(players, key=lambda x: int(x['kills']), reverse=True)
                player1 = sorted_factions[0]
                player2 = sorted_factions[1]
                player3 = sorted_factions[2]

                message = message.replace("[player1_name]", player1["name"])
                message = message.replace("[player2_name]", player2["name"])
                message = message.replace("[player3_name]", player3["name"])

                message = message.replace("[player1_kills]", player1["kills"])
                message = message.replace("[player2_kills]", player2["kills"])
                message = message.replace("[player3_kills]", player3["kills"])

                return message

        if modality == "HCF":
            db = client[hcf_db]

            if type == 1: # Factions Top
                collection = db["teams"]
                results = collection.find({})
                playerFactions = []

                for document in results:
                    if document["teamType"] == "PLAYER":
                        playerFactions.append(document)
                
                sorted_factions = sorted(playerFactions, key=lambda x: int(x['points']), reverse=True)
                ftop1 = sorted_factions[0]
                ftop2 = sorted_factions[1]
                ftop3 = sorted_factions[2]

                message = message.replace("[faction1_name]", ftop1["name"])
                message = message.replace("[faction2_name]", ftop2["name"])
                message = message.replace("[faction3_name]", ftop3["name"])

                message = message.replace("[faction1_points]", ftop1["points"])
                message = message.replace("[faction2_points]", ftop2["points"])
                message = message.replace("[faction3_points]", ftop3["points"])

                return message

            if type == 2: # Leaderboards
                collection = db["users"]
                results = collection.find({})
                players = []

                for document in results:
                    players.append(document)
                
                sorted_factions = sorted(players, key=lambda x: int(x['kills']), reverse=True)
                player1 = sorted_factions[0]
                player2 = sorted_factions[1]
                player3 = sorted_factions[2]

                message = message.replace("[player1_name]", player1["name"])
                message = message.replace("[player2_name]", player2["name"])
                message = message.replace("[player3_name]", player3["name"])

                message = message.replace("[player1_kills]", player1["kills"])
                message = message.replace("[player2_kills]", player2["kills"])
                message = message.replace("[player3_kills]", player3["kills"])

                return message

    except Exception as e:
        pass    

    return "Unable to fetch data or there isn't enough users for showing up."

@tasks.loop(minutes=5)
async def faction_tops():
    kitmap_ftop_channel, kitmap_lb_channel = bot.get_channel(config["CHANNELS"]["FACTION_TOP"]["KITMAP"]["CHANNEL"]), bot.get_channel(config["CHANNELS"]["LEADERBOARDS_KILL"]["KITMAP"]["CHANNEL"])
    hcf_ftop_channel, hcf_lb_channel       = bot.get_channel(config["CHANNELS"]["FACTION_TOP"]["HCF"]["CHANNEL"]), bot.get_channel(config["CHANNELS"]["LEADERBOARDS_KILL"]["HCF"]["CHANNEL"])

    hcf_ftop_message, hcf_lb_message       = await hcf_ftop_channel.fetch_message(config["CHANNELS"]["FACTION_TOP"]["HCF"]["MESSAGE"]), await hcf_lb_channel.fetch_message(config["CHANNELS"]["LEADERBOARDS_KILL"]["HCF"]["MESSAGE"])
    kitmap_ftop_message, kitmap_lb_message = await kitmap_ftop_channel.fetch_message(config["CHANNELS"]["FACTION_TOP"]["KITMAP"]["MESSAGE"]), await kitmap_lb_channel.fetch_message(config["CHANNELS"]["LEADERBOARDS_KILL"]["KITMAP"]["MESSAGE"])

    # KitMap Faction Top

    embed_kitmap_ftop = discord.Embed(title=f"Faction Leaderboards | Next update <t:{str(round(time.time() + 300))}:R>", description=parseMessage("""
1. [faction1_name] ([faction1_points] points)
2. [faction2_name] ([faction2_points] points)
3. [faction3_name] ([faction3_points] points)
""".strip(), "KitMap", 1))
    

    # HCF Faction Top

    embed_hcf_ftop = discord.Embed(title=f"Faction Leaderboards | Next update <t:{str(round(time.time() + 300))}:R>", description=parseMessage("""
1. [faction1_name] ([faction1_points] points)
2. [faction2_name] ([faction2_points] points)
3. [faction3_name] ([faction3_points] points)
""".strip(), "HCF", 1))

    # KitMap Leaderboards

    embed_kitmap_lb = discord.Embed(title=f"Player Leaderboards | Next update <t:{str(round(time.time() + 300))}:R>", description=parseMessage("""
1. [player1_name] ([player1_kills] kills)
2. [player2_name] ([player2_kills] kills)
3. [player3_name] ([player3_kills] kills)
""".strip(), "KitMap", 2))

    # HCF Leaderboards

    embed_hcf_lb = discord.Embed(title=f"Player Leaderboards | Next update <t:{str(round(time.time() + 300))}:R>", description=parseMessage("""
1. [player1_name] ([player1_kills] kills)
2. [player2_name] ([player2_kills] kills)
3. [player3_name] ([player3_kills] kills)
""".strip(), "HCF", 2))

    # Set footers for embeds.

    embed_kitmap_ftop.set_footer(text="This embed is updated every 5 minutes.")
    embed_hcf_ftop.set_footer(text="This embed is updated every 5 minutes.")

    embed_kitmap_lb.set_footer(text="This embed is updated every 5 minutes.")
    embed_hcf_lb.set_footer(text="This embed is updated every 5 minutes.")

    if kitmap_ftop_message == None:
        kitmap_ftop_message = await kitmap_ftop_channel.send(embed=embed_kitmap_ftop)
        return
    
    if hcf_ftop_message == None:
        hcf_ftop_message = await hcf_ftop_channel.send(embed=embed_kitmap_ftop)
        return
    
    if kitmap_lb_message == None:
        kitmap_lb_message = await kitmap_lb_channel.send(embed=embed_kitmap_lb)
        return

    if hcf_lb_message == None:
        hcf_lb_message = await hcf_lb_channel.send(embed=embed_hcf_lb)
        return

    await kitmap_ftop_message.edit(embed=embed_kitmap_ftop)
    await hcf_ftop_message.edit(embed=embed_hcf_ftop)

    await kitmap_lb_message.edit(embed=embed_kitmap_lb)
    await hcf_lb_message.edit(embed=embed_hcf_lb)

@bot.event
async def on_ready():
    faction_tops.start()
    saveStorage.start()

    print(f"""{Fore.BLUE}
╭────────────────────────────────────────╮
│                                        │
│                  HCF                   │
│              Leaderboards              │
│                                        │
╰────────────────────────────────────────╯

{Fore.GREEN}» Loaded everything!
╭─
│
│  Connected to MongoDB: ✅
│  Loaded configuration: ✅
│
╰─{Fore.RESET}
""".strip())

bot.run(config["TOKEN"])
