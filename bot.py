import discord
import os
import random
import json
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

with open("car_data.json", "r") as f:
    car_data = json.load(f)

# Store current round info
current_car = None
timer_task = None


async def start_timer(channel, seconds):
    global current_car, timer_task
    await asyncio.sleep(seconds)

    # If timer finishes AND the car wasn't guessed
    if current_car is not None:
        answer = current_car["name"]
        await channel.send(f"⏰ Time's up! The correct answer was **{answer}**.")
        current_car = None
        timer_task = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(description="Start a new car guessing round")
async def car(ctx):
    global current_car, timer_task

    # Pick a random car
    car = random.choice(car_data)
    current_car = car

    # Send image + prompt
    await ctx.respond(
        file=discord.File(f"car_images/{car['image']}")
    )
    await ctx.send("Guess the car!")

    # Start timer (20 seconds — change if you want)
    if timer_task is not None:
        timer_task