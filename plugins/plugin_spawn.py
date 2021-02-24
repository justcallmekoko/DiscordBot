import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')

class ClearWeather():
	name = '!spawn'

	desc = 'Spawn a(n) '

	synt = '!spawn'

	looping = False

	admin = True
	
	cheer = 21
								
	async def stop(self, message):
		self.looping = False

	async def run(self, message):			
		print ('Spawning...')
		with MCRcon("127.0.0.1", PASSW) as mcr:
			# Minecraft command to spawn X near player
			resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run summon tnt')

			# Minecraft command to post notification text in the game
			try:
				resp = mcr.command('/tellraw @a [{\"text\":\"' + message + ': Spawned a(n) \",\"color\":\"green\"}]')
			except Exception as e:
				resp = mcr.command('/tellraw @a [{\"text\":\"Spawned a(n) \",\"color\":\"green\"}]')
			mcr.disconnect()
			
		# Post notification message in discord server if this is from discord command
		try:
			await message.channel.send(message.author.mention + ' Spawned a(n)')
		except Exception as e:
			did_not_send = True
