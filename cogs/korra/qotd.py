from typing import Union

import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://korra-tuner-default-rtdb.firebaseio.com/'})

class Qotd(commands.Cog):
    """Fun Interactive Questions for the server!"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="post", with_app_command=True)
    async def post(self, ctx: commands.Context):
        """Post the question of the day!

            Args:
                ctx (commands.Context): _description_
        """
        # Grab the DB Reference        
        handle = db.reference('question')
        question = handle.order_by_key().get()

        #Create The POST
        embed_message = discord.Embed(
            title = '❔❓ Question of the day! ❔❓',
            description = f' Question:  {list(question.items())[0][1]} ',
            color = 0x9fffff
        )
        embed_message.set_footer(text=f' Asked by: Korra! • {len(question)-1} Questions Left • Today at {datetime.now().strftime("%H:%M")}')
        
        #delete the post
        db.reference(f"question/{list(question.items())[0][0]}").delete()
        await ctx.send(f"Question Time", ephemeral=True)
        #Send the message
        await ctx.channel.send(embed=embed_message)

    @commands.hybrid_command(name="add", with_app_command=True)
    @commands.has_any_role("staff", "cutie")
    async def add(self, ctx: commands.Context, *, question: str):
        """ Sends the question of the day.

            Args:
                ctx (commands.Context): _description_
        """
        handle = db.reference('question')
        handle.push(question)
        await ctx.send(f"Question sent {ctx.author.nick}!", ephemeral=True)

    @commands.hybrid_command(name="mods", with_app_command=True)
    @commands.has_any_role("staff", "cutie")
    async def mods(self, ctx: commands.Context, *, message: str):
        """ Secret Mod Command. 

            Args:
                ctx (commands.Context): _description_
        """
        await ctx.send(f"fufufuf", ephemeral=True)
        await ctx.channel.send(message)

async def setup(bot: commands  .Bot) -> None:
    await bot.add_cog(Qotd(bot))
