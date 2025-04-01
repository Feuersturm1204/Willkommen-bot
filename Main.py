import discord
import json
from discord.ext import commands

# Lade den Bot-Token aus einer separaten Datei
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    BOT_TOKEN = config.get("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)



# Konfigurationsoptionen
settings = {
    "welcome_channel": None,
    "leave_channel": None,
    "boost_channel": None,
    "welcome_message": "Willkommen {user}!",
    "leave_message": "{user} hat den Server verlassen.",
    "boost_message": "Danke {user} fürs Boosten!",
    "welcome_active": True,
    "leave_active": True,
    "boost_active": True,
    "embed_title": "",
    "embed_footer": "",
    "embed_thumbnail": None,
    "embed_image": None
}

# Setze Kanäle
@bot.command()
async def setchannel(ctx, channel_type: str, channel: discord.TextChannel):
    if channel_type in settings:
        settings[channel_type] = channel.id
        await ctx.send(f"{channel_type} gesetzt auf {channel.mention}")
    else:
        await ctx.send("Ungültiger Kanaltyp. Verfügbare Typen: welcome_channel, leave_channel, boost_channel")

# Setze Nachrichten
@bot.command()
async def setmessage(ctx, message_type: str, *, message: str):
    if message_type in settings:
        settings[message_type] = message
        await ctx.send(f"{message_type} Nachricht geändert!")
    else:
        await ctx.send("Ungültiger Nachrichtentyp. Verfügbare Typen: welcome_message, leave_message, boost_message")

# Setze Embed-Einstellungen
@bot.command()
async def setembed(ctx, embed_type: str, *, value: str):
    if embed_type in ["embed_title", "embed_footer", "embed_thumbnail", "embed_image"]:
        settings[embed_type] = value if value.lower() != "none" else None
        await ctx.send(f"{embed_type} gesetzt!")
    else:
        await ctx.send("Ungültiger Embed-Typ. Verfügbare Typen: embed_title, embed_footer, embed_thumbnail, embed_image")

# Aktivieren/Deaktivieren von Funktionen
@bot.command()
async def activate(ctx, feature: str):
    if feature + "_active" in settings:
        settings[feature + "_active"] = True
        await ctx.send(f"{feature} wurde aktiviert.")
    else:
        await ctx.send("Ungültige Funktion. Verfügbare Funktionen: welcome, leave, boost")

@bot.command()
async def deactivate(ctx, feature: str):
    if feature + "_active" in settings:
        settings[feature + "_active"] = False
        await ctx.send(f"{feature} wurde deaktiviert.")
    else:
        await ctx.send("Ungültige Funktion. Verfügbare Funktionen: welcome, leave, boost")

# Begrüßungsnachricht senden
@bot.event
async def on_member_join(member):
    if settings["welcome_active"] and settings["welcome_channel"]:
        channel = bot.get_channel(settings["welcome_channel"])
        if channel:
            embed = discord.Embed(title=settings["embed_title"], description=settings["welcome_message"].replace("{user}", member.mention), color=discord.Color.green())
            if settings["embed_footer"]:
                embed.set_footer(text=settings["embed_footer"])
            if settings["embed_thumbnail"]:
                embed.set_thumbnail(url=settings["embed_thumbnail"])
            if settings["embed_image"]:
                embed.set_image(url=settings["embed_image"])
            await channel.send(embed=embed)

# Verabschiedungsnachricht senden
@bot.event
async def on_member_remove(member):
    if settings["leave_active"] and settings["leave_channel"]:
        channel = bot.get_channel(settings["leave_channel"])
        if channel:
            embed = discord.Embed(title=settings["embed_title"], description=settings["leave_message"].replace("{user}", member.mention), color=discord.Color.red())
            if settings["embed_footer"]:
                embed.set_footer(text=settings["embed_footer"])
            if settings["embed_thumbnail"]:
                embed.set_thumbnail(url=settings["embed_thumbnail"])
            if settings["embed_image"]:
                embed.set_image(url=settings["embed_image"])
            await channel.send(embed=embed)

# Boost-Nachricht senden
@bot.event
async def on_member_update(before, after):
    if settings["boost_active"] and not before.premium_since and after.premium_since:
        if settings["boost_channel"]:
            channel = bot.get_channel(settings["boost_channel"])
            if channel:
                embed = discord.Embed(title=settings["embed_title"], description=settings["boost_message"].replace("{user}", after.mention), color=discord.Color.purple())
                if settings["embed_footer"]:
                    embed.set_footer(text=settings["embed_footer"])
                if settings["embed_thumbnail"]:
                    embed.set_thumbnail(url=settings["embed_thumbnail"])
                if settings["embed_image"]:
                    embed.set_image(url=settings["embed_image"])
                await channel.send(embed=embed)

# Bot starten
bot.run(BOT_TOKEN)
