from typing import Union
import discord
from discord.ext import commands
from discord import app_commands
from firebase_admin import db


class Voting(commands.Cog):
    """Voting / Nomination System"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # -------------------------
    # NOMINATE
    # -------------------------
    @commands.hybrid_command(name="nominate", with_app_command=True)
    async def nominate(self, ctx, member: discord.Member):
        """Add a person to the leaderboard"""

        ref = db.reference("votes")
        existing = ref.child(str(member.id)).get()

        if existing:
            await ctx.send(f"{member.display_name} is already nominated!", ephemeral=True)
            return

        ref.child(str(member.id)).set({
            "name": member.display_name,
            "votes": 0
        })

        await ctx.send(f"{member.display_name} has been nominated!", ephemeral=True)

    # -------------------------
    # NOMINEES (PRIVATE)
    # -------------------------
    @commands.hybrid_command(name="nominees", with_app_command=True)
    async def nominees(self, ctx):
        """Show all nominees (only visible to you)"""

        ref = db.reference("votes")
        data = ref.get()

        if not data:
            await ctx.send("No nominees yet!", ephemeral=True)
            return

        description = ""
        for user_id, info in data.items():
            description += f"{info['name']} — {info['votes']} votes\n"

        embed = discord.Embed(
            title="📜 Current Nominees",
            description=description,
            color=0x9fffff
        )

        await ctx.send(embed=embed, ephemeral=True)

    # -------------------------
    # NOMINEES TOP 10 (PUBLIC)
    # -------------------------
    @commands.hybrid_command(name="nominees10", with_app_command=True)
    async def nominees10(self, ctx):
        """Show top 10 nominees"""

        ref = db.reference("votes")
        data = ref.get()

        if not data:
            await ctx.send("No nominees yet!")
            return

        # Sort by votes descending
        sorted_users = sorted(
            data.items(),
            key=lambda x: x[1]["votes"],
            reverse=True
        )[:10]

        description = ""
        top_members = []

        for i, (user_id, info) in enumerate(sorted_users, start=1):
            description += f"**{i}.** {info['name']} — {info['votes']} votes\n"

            if i <= 3:
                member = ctx.guild.get_member(int(user_id))
                top_members.append(member if member else None)

        embed = discord.Embed(
            title="🏆 Top 10 Nominees",
            description=description,
            color=0xffd700
        )

        # 🥇 First place avatar
        if len(top_members) >= 1 and top_members[0]:
            embed.set_thumbnail(url=top_members[0].display_avatar.url)

        # 🥈🥉 Add fields
        medals = ["🥇", "🥈", "🥉"]
        for i, member in enumerate(top_members):
            if member:
                embed.add_field(
                    name=f"{medals[i]} {member.display_name}",
                    value=f"[Avatar]({member.display_avatar.url})",
                    inline=True
                )

        await ctx.send(embed=embed)

    # -------------------------
    # VOTE
    # -------------------------
    @commands.hybrid_command(name="vote", with_app_command=True)
    async def vote(self, ctx, member: discord.Member):
        """Vote for a nominee"""

        ref = db.reference("votes")
        user_ref = ref.child(str(member.id))
        data = user_ref.get()

        if not data:
            await ctx.send(f"{member.display_name} is not nominated!", ephemeral=True)
            return

        current_votes = data.get("votes", 0)

        user_ref.update({
            "votes": current_votes + 1
        })

        await ctx.send(f"You voted for {member.display_name}! (+1)", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voting(bot))
