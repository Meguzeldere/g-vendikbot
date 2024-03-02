import discord
from dc import auth
from colorama import Fore, Style, init
from discord.ext import commands

prefix = "!"

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True

kisi = "Kaan"
foto = "https://cdn.discordapp.com/attachments/1209061047084916807/1209087917566328872/sm3ynsk.jpg?ex=65e5a5df&is=65d330df&hm=3539ae1e984cf536d0b1742933902645f9abc1cb865c3465bd6eefb46d135f66&"


bot = commands.Bot(command_prefix=prefix, intents=intents)

# Örnek bir ayar değişkeni
otomatik_sistem = False

@bot.event
async def on_ready():
    print(f' {bot.user} Sistemi Aktif!!')
    print("!Siz Terminali Kapatana Kadar Bot Aktif Kalır!")
    await bot.change_presence(activity=discord.Game(name="!yardım"))

@bot.command()
async def deneme(ctx):
    """
    Bu komut, kullanıcıya doğrulama mesajını gönderir ve fotoğrafı ekler.
    """
    message = await ctx.send(f"Bu fotoğraftaki {kisi} kişisini onaylıyor musunuz?")

    embed = discord.Embed(title="Doğrulama", description="Bu fotoğraftaki kişiyi onaylıyor musunuz?")
    embed.set_image(url=f"{foto}")
    message = await ctx.send(embed=embed)

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="✅", style=discord.ButtonStyle.green, custom_id="onayla"))
    view.add_item(discord.ui.Button(label="❌", style=discord.ButtonStyle.red, custom_id="reddet"))

    await message.edit(view=view)

@bot.event
async def on_button_click(interaction):
    """
    Butonlara tıklama işlemi.
    """
    if interaction.custom_id == "onayla":
        await interaction.response.send_message("Kilit Açıldı 🔓", ephemeral=True)
    elif interaction.custom_id == "reddet":
        await interaction.response.send_message("Sistem Kilitlendi Kolluk Kuvvetlerine Haber Gönderildi 🔒", ephemeral=True)

@bot.command()
async def ayarlar(ctx):
    """
    Botun mevcut ayarlarını gösterir ve otomatik sistem ayarını değiştirmenizi sağlar.
    """
    global otomatik_sistem
    embed = discord.Embed(title="Ayarlar", description="Botun mevcut ayarları")
    embed.add_field(name="Otomatik Sistem", value="Açık" if otomatik_sistem else "Kapalı", inline=False)
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Aç", style=discord.ButtonStyle.green, custom_id="ac"))
    view.add_item(discord.ui.Button(label="Kapat", style=discord.ButtonStyle.red, custom_id="kapat"))

    await ctx.send(embed=embed, view=view)

@bot.event
async def on_button_click(interaction):
    """
    Butonlara tıklama işlemi.
    """
    global otomatik_sistem
    if interaction.custom_id == "ac":
        otomatik_sistem = True
        await interaction.response.send_message("Otomatik Sistem Açıldı", ephemeral=True)
    elif interaction.custom_id == "kapat":
        otomatik_sistem = False
        await interaction.response.send_message("Otomatik Sistem Kapatıldı", ephemeral=True)

@bot.command()
async def yardım(ctx):
    """
    Botun tüm komutlarını ve açıklamalarını gösterir.
    """
    help_embed = discord.Embed(title="Yardım", description="Tüm komutlar ve açıklamaları")
    for command in bot.commands:
        help_embed.add_field(name=f"{prefix}{command.name}", value=command.help, inline=False)
    await ctx.send(embed=help_embed)

# Botu başlatmak için tokeni girin
bot.run(auth)
