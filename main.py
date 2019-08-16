import discord
from discord.ext import commands
from cogs import Birthday
from os import environ

ENVIORN = "BIRTHDAY_BOT_KEY" # change this to the name of your variable
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("The bot has started.")
    activity = discord.Activity(name='birthdaybot | ~help', type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)

def main():
    try:
        environ[ENVIORN]
    except:
        print(f"[Error]: The bot requires a token to run, None assigned to {ENVIORN}")
        exit()

    bot.add_cog(Birthday(bot))
    bot.run(environ[ENVIORN])

if __name__ == "__main__":
    main()