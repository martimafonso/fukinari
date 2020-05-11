import discord
import asyncio
import time
import json
import datetime as DT 
import os  
from discord.ext import commands, tasks
from itertools import cycle

#https://discord.com/oauth2/authorize?client_id=708369395931545710&scope=bot&permissions=8

status = cycle(['Feito em python com muito stackoverflow', 'Use --help para obter suporte', 'Neko :3', 'Ferroxy#2071 melhor programador do mundo'])
token = 'Paste your token here'
activity = discord.Game#(name="discord.py")


async def get_prefix(client, message):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(activity=activity(next(status)))


@client.event
async def on_ready():
	change_status.start()
	print(f"Logado como {client.user}\n")

@client.event
async def on_guild_join(guild):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	prefixes[str(guild.id)] = '--'

	with open('prefixes.json','w') as file:
		json.dump(prefixes, file, indent=4)

@client.event
async def on_guild_remove(guild):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	prefixes.pop(str(guild.id))
	with open('prefixes.json','w') as file:
		json.dump(prefixes, file, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	prefixes[str(ctx.guild.id)] = prefix

	with open('prefixes.json','w') as file:
		json.dump(prefixes, file, indent=4)
	
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color = discord.Color.red()
    )
    embed.set_author(name='Help')
    embed.add_field(name='logout', value='Shutdown bot', inline=False)	 
    embed.add_field(name='changeprefix', value='Changes bot prefix', inline=False)
    await author.send(embed=embed)

@client.command()
async def clear(ctx, amount=0):
	if amount == 0:
		await ctx.send("O limite nao pode ser igual ou menor que 0")
	await ctx.message.delete()
	await ctx.channel.purge(limit=amount)
	

client.run(token)	
