import json;
import requests
import discord
from discord.ext import commands
import random


class Motivational(commands.Cog):
    """Fun Interactive Questions for the server!"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        return
    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        else:
            if any(word in message.content for word in sad_words):
                print("sad")
                await message.channel.send(random.choice(starter_encourougements))

    @commands.Cog.listener()
    async def sticker(self,message):
        match message.content:
            case "wrong answer":
                await message.channel.send("https://media.discordapp.net/attachments/877360429951778837/1073428823368007730/korra_with_a_gun.png?width=760&height=760")

    #commands
    @commands.command()
    async def quote(self, ctx):
        response = requests.get("https://api.adviceslip.com/advice")
        json_data = json.loads(response.text)
        advice = json_data["slip"]['advice']
        await ctx.send(advice)

    @commands.command()
    async def advice(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + "\n - ME"
        await ctx.send(quote)

    @commands.command()
    async def nya(self, ctx):
        await ctx.send("Did someone say nya nya?! ")
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        json_data = json.loads(response.text)
        cat_image = json_data[0]["url"]
        await ctx.send(cat_image)

    @commands.command(brief='Flip a Korra', description="It's like flipping a coin, but a bit better")
    async def flip(self,ctx):
    	await ctx.send("Flips a coin and...\n\n " + random.choice(["... lays on my back. Y-you can touch my tail", "...fidgets a little. I-I guess you can pet my head.", "...grabs it! Don't look at me like that. I need the money!", "...headbutts you! OWW! You've got such a hard head!", "...pins the tail on my little donkey... I MEAN YOU, YA DUTZ!", "...the coin keeps flipping and flipping and flipping and flipping and flipping and flipping...", "...shaves off all of your hair. Nya hahaha!", "...slaps you on the tooshie! Ji ji ji ji", "...lands on the edge! WOAH!", "...curls up on the top of your head. Yaaawn. What a good napping face.", "...booty bumps ya!", "...hands your a brush. Go ahead and brush my tail, why dontcha?"]))

    @commands.command()
    async def propose(self,ctx):
    	await ctx.send("You have to be at least as rich as me to propose!")

    @commands.command(brief="nya roll 25", description="Roll a number of you choosing. Or be default of 6.")
    async def roll(self,ctx, url=6):
        if (isinstance(url, int)):
            random_value = str(random.randrange(url)+1)
            await ctx.send(ctx.author.name + " rolled a " + random_value + ". Nya!")
            if (random_value == "1"):
                await ctx.send("oof...")
        else:
            await ctx.send("Use a real number, dum dum.")

sad_words = [" sad ", "depressed", "unhappy", "angry", "miserable", "depressing", " cry "]
starter_encourougements = [
"I'm here for you. Cry if you need to",
"I promise it will get better, maybe not now, but one day",
"I can go shopping with you later if that'll make you feel better?",
"I'll be there to cheer you up. Give me a bit."
"https://c.tenor.com/2lr9uM5JmPQAAAAC/hug-anime-hug.gif",
"*pat pat*",
"Cheer up! I believe in you!",
"Who cares",
"Remember you are special there is no one like you out there.",
"I had days like those too. I'm not good very good with words but maybe <@201184088118394880> can help?"
]

async def setup(bot: commands  .Bot) -> None:
    await bot.add_cog(Motivational(bot))
