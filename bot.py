# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('.env')
TOKEN = ""

bot = commands.Bot(command_prefix='!')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

#client = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    feedback = [
        'Lean back.',
        'You are slumping!',
        'Cool.'
    ]

    if message.content[:8] == '!posture' or message.content[:9]=='! Posture' or '!Posture':
        response = random.choice(feedback) #Temporarily giving random results until we integrate AI
        await message.channel.send(response)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def pic(ctx, img_url, arg=""):
	global pic_flag
	global gif_flag
	global convert_flag
	if pic_flag == 1 or gif_flag == 1 or convert_flag == 1:
		await ctx.send("Still working on the previous command, please wait for the result then resend!")
		return
	pic_flag = 1
	if ctx.message.attachments: 
		img_url = ctx.message.attachments[0].url
	response = requests.head(img_url)
	if 'content-length' in response.headers and int(response.headers['content-length']) < 5242880: #limit on file to 5MB to keep computations faster
		response = requests.get(img_url)	
		i = Image.open(BytesIO(response.content)) #downloading image
	if 'content-length' not in response.headers or int(response.headers['content-length']) >= 5242880:
		await ctx.send("Sorry, I only work on images with a size less than 5MB!")
		pic_flag = 0
		return
	await ctx.send("Ok let me work on that picture for you, please give me a moment!")	
	i.save("image.ppm") #converting image to ppm format for executable
	#
	#THIS IS THE PLACE FOR THE AI PART
	#
	result = "" #it's blank just for now
	await ctx.send("Here's the analysis!", str(result)) #sending the result
	os.remove("image.ppm") #cleanup
	os.remove("editedpic.ppm")
	print("Done removing files and executing command pic.")
	pic_flag = 0        
    

bot.run(TOKEN)

