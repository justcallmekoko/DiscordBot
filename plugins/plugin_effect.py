import os
from random import randint
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')
HOST_USER = os.getenv('HOST_USER')

class Effect():
	name = '!effect'

	desc = 'Give an effect '

	synt = '!effect'

	looping = False

	admin = True
	
	cat = 'character'
	
	cheer = [
		[91,'fire_resistance'],
		[102,'poison']
		]

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		found = False
		for item in self.cheer:
			if int(bits) == int(item[0]):
				found = True
				break

		if found:
			return True
		else:
			return False
								
	async def stop(self, message):
		self.looping = False
		
	async def runCheer(self, user, amount):
		print ('Giving effect...')
		
		found = False
		ent = ''
		
		for item in self.cheer:
			if int(amount) == int(item[0]):
				found = True
				ent = str(item[1])
				
		with MCRcon("127.0.0.1", PASSW) as mcr:
			# Minecraft command to spawn X near player
			#resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run summon tnt')
			resp = mcr.command('/effect give ' + str(HOST_USER) + ' ' + str(ent))

			# Minecraft command to post notification text in the game
			resp = mcr.command('/tellraw @a [{\"text\":\"' + user + ': Gave ' + str(ent) + '\",\"color\":\"green\"}]')
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
