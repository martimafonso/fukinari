import discord
from discord.ext import commands

class admin(commands.Cog):
#Eventos
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print(r"[Modulo admin carregado]")
		print("\n\n")
#Comandos
	@commands.command()
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		try:
			await member.kick(reason=reason)
		except discord.Forbidden as dsError:
			embed = discord.Embed(
 		        color = discord.Color.from_rgb(144, 12, 63)
    			)
			embed.add_field(name=f"Error {dsError}", value="Eu nao posso fazer isso (#-#)")
			await ctx.send(embed=embed)
			

def setup(client):
	client.add_cog(admin(client))