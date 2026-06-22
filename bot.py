import discord
from discord.ext import commands

# إعداد الصلاحيات والنوايا الخاصة بالبوت ليعمل بشكل صحيح
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presence = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user.name} Is Online and Ready!")

# أمر بسيط للتجربة داخل الشات المخصص
@bot.command()
async def ping(ctx):
    await ctx.send("Components Loaded Successfully! 🏓")

# تشغيل البوت باستخدام التوكن الخاص بك
bot.run("MTUxODY1OTA5ODIxODg2MDcwNA.G9BpPC.B5S-cqW8sO6zL-gbHPq7RogOx1ihszmQteUmWE")
