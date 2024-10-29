import discord, requests, json, random, os
from discord.ext import commands
from dotenv import load_dotenv

intents=discord.Intents.default()
intents.members=True; intents.presences=True; intents.guild_messages=True; intents.message_content=True

load_dotenv()
discord_key= os.getenv('DISCORD_KEY')
rapid_key= os.getenv('RAPID_KEY')

client = commands.Bot(command_prefix='!', intents=intents)

def joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
     "X-RapidAPI-Key": rapid_key,
     "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
     }
    response = requests.get(url,headers=headers)
    data=json.loads(response.text)
    setup=data['body'][0]['setup']
    pun=data['body'][0]['punchline']
    joke=str(setup)+'\n'+str(pun)
    return joke

def rockpaper(c):
    c=c.lower()
    options=['rock','paper','scissors']
    r = random.choice(options)
    if c not in options:
        return('please enter one of "rock", "paper" or "scissors"')
    elif ((r=='rock' and c=='paper')or(r=='paper' and c=='scissors')or (r=='scissors' and c=='rock')):
        res=('You win!')
    elif r==c:
        res=('It\'s a tie')
    elif ((r=='rock' and c=='scissors')or(r=='paper' and c=='rock')or(r=='scissors' and c=='paper')):
        res=('You lose!')
    else:
        return ('unknown error, breaking.')
    return ('You picked {0}\nThe bot picked {1}\n{2}').format(c,r,res)
    
@client.event
async def on_ready():
    print('We are online.')
    print('Logged in as {0.user}.'.format(client))
    servernos=0
    for i in client.guilds:
        servernos+=1
    print('The bot is in',servernos,'servers.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='ME SHIT AND PISS AND CUM'))

@client.command(name='dad', help='dad jokes')
async def on_message(message):
    await message.channel.send(joke())

@client.command(name='test')
async def on_message(message):
    await message.channel.send('works')

@client.command(name='rps', help='write your choice after the command')
async def on_message(message,choice):
    await message.channel.send(rockpaper(choice))

@client.command(name='act', help='write the name of the activity after command to change')
async def on_message(message,change):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=change))
    await message.channel.send('switched activity status to '+str(change))

client.run(discord_key)