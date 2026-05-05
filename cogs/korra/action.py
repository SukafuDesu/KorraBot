from typing import Union

import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
import random
from firebase_admin import db

def randomizer(url, user="Person", author="Korra"):
    """ Randomizer: Find the first image from our database, and grab it!

        Args:
            ctx (commands.Context): _description_
    """

    # start assigning the names.
    if (not isinstance(user, str)):
        if(user.nick):
            user = user.nick
        else:
            user = user.name

        if(author.nick):
            author = author.nick
        else:
            author = author.name

    # handle the db reference.
    handle = db.reference(url)
    question = handle.order_by_key().get()
    
    # Get Random Number
    max = handle.child("count").get();
    random_value = str(random.randrange(max))
    image: str = handle.order_by_key().equal_to(random_value).get()[random_value]

    # Choose a message to generate
    title_message = f'💕 Hey {user} you got a {url} from {author}'
    if (user == author):
        title_message = f'Aww are you lonely?! {url} From yours truly!! <:korra_goodjob:1042878371828355082>'
    if (user == "Korra"):
        title_message = f'I guess you get a {url} from me!'
    if (user == "None") or (user == ""):
        title_message = f'If you need someone I will always be here. (probably)'        

    #Create the embed message
    embed_message = discord.Embed(
        title = title_message,
        color = 0x9fffff,
    )
    #set the image
    embed_message.set_image(url=image)
    return embed_message

class Action(commands.Cog):
    """Fun Interactive Questions for the server!"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.hybrid_command(name="kiss", with_app_command=True)
    async def kiss(self, ctx: commands.Context, member: discord.Member=None):
        """ Kiss on the haters

            Args:
                ctx (commands.Context): _description_
        """
        if(member):
            await ctx.send(embed=randomizer("kiss", member, ctx.author))
        else:
            await ctx.send(embed=randomizer("kiss", "None", ctx.author))


    @commands.hybrid_command(name="dab", with_app_command=True)
    async def dab(self, ctx: commands.Context, member: discord.Member=None):
        """ dab on the haters

            Args:
                ctx (commands.Context): _description_
        """
        if(member):
            await ctx.send(embed=randomizer("dab", member, ctx.author))
        else:
            await ctx.send(embed=randomizer("dab", "None", ctx.author))

    @commands.hybrid_command(name="hug", with_app_command=True)
    async def hug(self, ctx: commands.Context, member: discord.Member=None):
        """ hug on the haters

            Args:
                ctx (commands.Context): _description_
        """
        if(member):
            await ctx.send(embed=randomizer("hug", member, ctx.author))
        else:
            await ctx.send(embed=randomizer("hug", "None", ctx.author))

    @commands.hybrid_command(name="slap", with_app_command=True)
    async def slap(self, ctx: commands.Context, member: discord.Member=None):
        """ slap on the haters

            Args:
                ctx (commands.Context): _description_
        """
        if(member):
            await ctx.send(embed=randomizer("slap", member, ctx.author))
        else:
            await ctx.send(embed=randomizer("slap", "None", ctx.author))

async def setup(bot: commands  .Bot) -> None:
    await bot.add_cog(Action(bot))