import os
from random import randint
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')
HOST_USER = os.getenv('HOST_USER')

class Spawn():
	name = '!spawn'

	desc = 'Spawn a(n) '

	synt = '!spawn'

	looping = False

	admin = True
	
	cat = 'spawn'
	
	cheer = [
		[3,'chicken'],
		[4,'sheep'],
		[5, 'bee'],
		[6,'cow'],
		[8,'evokation_illager'],
		[9,'skeleton_horse'],
		[10, 'horse'],
		[11,'zombie_villager'],
		[12,'vex'],
		[13,'spider'],
		[15,'creeper'],
		[16,'skeleton'],
		[17,'enderman'],
		[18,'silverfish'],
		[25,'blaze'],
		[50,'giant'],
		[55,'ender_crystal'],
		[75,'ghast'],
		[76,'polar_bear'],
		[100,'snow_golem'],
		[200,'witch'],
		[1000,'wither'],
		[2000,'ender_dragon']
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
		print ('Spawning...')
		
		found = False
		ent = ''
		
		for item in self.cheer:
			if int(amount) == int(item[0]):
				found = True
				ent = str(item[1])
				
		with MCRcon("127.0.0.1", PASSW) as mcr:
			# Minecraft command to spawn X near player
			#resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run summon tnt')
			#resp = mcr.command('/execute at ' + str(HOST_USER) + ' run summon ' + str(ent) + ' ~' + str(randint(1, 5)) + ' ~' + str(randint(1, 5)) + ' ~' + str(randint(1, 5)))
			resp = mcr.command('/execute at ' + str(HOST_USER) + ' run summon ' + str(ent) + ' ~ ~ ~')

			# Minecraft command to post notification text in the game
			resp = mcr.command('/tellraw @a [{\"text\":\"' + user + ': Spawned a(n) ' + str(ent) + '\",\"color\":\"green\"}]')
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
