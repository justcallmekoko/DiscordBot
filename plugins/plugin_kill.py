import os
from random import randint
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')
HOST_USER = os.getenv('HOST_USER')

class Kill():
	name = '!kill'

	desc = 'Kill player '

	synt = '!kill'

	looping = False

	admin = True
	
	cheer = 503
	
	cat = 'character'
	
	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False

	
	def checkBits(self, bits):
		if bits == self.cheer:
			return True
		else:
			return False
								
	async def stop(self, message):
		self.looping = False
		
	async def runCheer(self, user, amount):
		print ('Killing...')
		
		
				
		with MCRcon("127.0.0.1", PASSW) as mcr:
			# Minecraft command to spawn X near player
			#resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run summon tnt')
			resp = mcr.command('/kill ' + str(HOST_USER))

			# Minecraft command to post notification text in the game
			resp = mcr.command('/tellraw @a [{\"text\":\"' + user + ': Killed ' + str(HOST_USER) + '\",\"color\":\"green\"}]')
			mcr.disconnect()
			

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
