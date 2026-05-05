import json
import requests
from discord.ext import commands
import random
index_num = 1
class Huggingface(commands.Cog):
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
            if self.bot.user.mentioned_in(message):
                print("i was mentioned")
                await message.channel.send(query(message=message.content[21:], i=index_num))

async def setup(bot: commands  .Bot) -> None:
    await bot.add_cog(Huggingface(bot))

##################################################################################

API_TOKEN = json.load(open('config.json'))["HUGGING_FACE_API_TOKEN"]
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

JsonData = {
"past_user_inputs" : [
                    "What is your name?",
                    "What is your favorite Food?",
                    "Do you believe in Magic?",
                    "Dab?",
                    "I have liquor.",
                    "Can I borrow money?"
                    ],
"generated_responses" : [
                    "My name is Korra",
                    "Fish",
                    "I'm already magical",
                    "Watch me dab.",
                    "I can't drink alcohol",
                    "I don't have money."
                    ],
"text": "Hello"
}

def query(message, i):
    print("in message")
    add_conversation(message , i)
    inputs = {"inputs": JsonData}
    data = json.dumps(inputs)
    print(data)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    i = i+1
    response_text = json.loads(response.content.decode("utf-8"))["generated_text"]
    add_generated_response(response_text, i)
    return(response_text)

def add_conversation(message: str , index):
    JsonData["past_user_inputs"][index]=message
    JsonData["text"]=message
    if (index>=4):
        index=1

def add_generated_response(response: str, index):
    JsonData["generated_responses"][index]=response

