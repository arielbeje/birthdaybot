from discord.ext import tasks, commands
from datetime import date, datetime
import json
import dateparser

BASE_YEAR = 1000 # used for when years are 'undefined'

def ordinals(n: str) -> str:
    """appends ordinals on numerals"""
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def parse_date(date: str) -> datetime:
    """Having the base set like this still allows for parsing for 'today' etc, while defaulting year and time"""
    today = datetime.now()
    base = datetime(BASE_YEAR, today.month, today.day, 0, 0, 0)

    return dateparser.parse(date, settings={'RELATIVE_BASE': base})

def humanize_date(date: datetime) -> str:
    """converts datetime to human readable date. (only includes year if set)"""
    if date.year == BASE_YEAR:
        strft = "%B %d"
    else:
        strft = f"%B {ordinals(date.day)} %Y"
    
    return date.strftime(strft)

def load_birthdays() -> dict:
    pass

def save_birthdays(birthdays: dict):
    pass

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.birthday_sender.start()

    @commands.command()
    async def birthday(self, ctx, option=None, *, target=None):
        import dateparser
        if option:
            if option == "set":
                try:
                    date = parse_date(target)
                    date_humanized = humanize_date(date)
                    await ctx.send(f"{ctx.author.name}'s birthday is now '{date_humanized}'")
                except:
                    await ctx.send(f"{target} is an invalid date :(")
            elif option == "clear":
                try:
                    await ctx.send(f"{ctx.author.name} removed their previous birthday. <OLD HUMANIZED DATE GOES HERE>")
                except:
                    await ctx.send(f"{ctx.author.name} has not set a birthday, nothing to remove!")
            elif option == "info":
                if target:
                    if target == "me":
                        try:
                            await ctx.send(f"{ctx.author.name}'s birthday is <HUMANIZED DATE GOES HERE>")
                        except:
                            await ctx.send(f"{ctx.author.name} has not set a birthday.")
                    else:
                        try:
                            member = await commands.MemberConverter().convert(ctx=ctx, argument=target)
                        except:
                            member = None
                        if member:
                            try:
                                await ctx.send(f"{member.name}'s birthday is <HUMANIZED DATE GOES HERE>")
                            except:
                                await ctx.send(f"{target} has not set a birthday.")
                        else:
                            await ctx.send(f"{target} is not a user on this server.")

                else:
                    await ctx.send(f"To see someones birthday, you must define who.")
        else:
            await ctx.send("birthday info")

    def cog_unload(self):
        """stops the loop when unloaded"""
        self.birthday_sender.cancel()

    @tasks.loop(hours=24.0)
    async def birthday_sender(self):
        """send birthday notifications daily, if any"""
        pass
    
    @birthday_sender.before_loop
    async def before_printer(self):
        """waits for the bot to start before initilizing the loop"""
        await self.bot.wait_until_ready()