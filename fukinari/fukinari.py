import discord
from discord.ext import commands, tasks
import asyncio
import time
import json
import os
from itertools import cycle
import datetime as DT 


activity = discord.Game
status = cycle(['Feito em python com muito stackoverflow', 'Use --help para obter suporte', 'Neko :3', 'Ferroxy#2071 melhor programador do mundo'])
token = input('Enter your token')


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
	print(f"\nLogado como {client.user}\n")

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


@client.command()
async def clear(ctx, amount=0):
	if amount == 0:
		await ctx.send("O limite nao pode ser igual ou menor que 0")
	await ctx.message.delete()
	await ctx.channel.purge(limit=amount)


@client.command()
async def load(ctx, extension):
	embed = discord.Embed(
        color = discord.Color.red()
    	)
	client.load_extension(f'cogs.{extension}')
	embed.add_field(name=f"Carregando modulo {extension}", value="Error")
	await ctx.send(embed=embed)

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	embed = discord.Embed(
        color = discord.Color.red()
    	)
	client.unload_extension(f'cogs.{extension}')
	embed.add_field(name=f"Descarregando modulo {extension}", value="Modulos")
	await ctx.send(embed=embed)

		

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')
	

client.run(token)	
