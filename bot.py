import discord
import os
import random
import json
import os
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

with open("car_data.json", "r") as f:
    car_data = json.load(f)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == "!car":
        car = random.choice(car_data)
        await message.channel.send(file=discord.File(f"car_images/{car['image']}"))
        await message.channel.send("Guess the car!")

    if message.content.lower().startswith("guess "):
        guess = message.content[6:].lower()
        for car in car_data:
            if guess == car["name"].lower():
                await message.channel.send("Correct!")
                return
        await message.channel.send("Wrong guess!")

client.run(TOKEN)
