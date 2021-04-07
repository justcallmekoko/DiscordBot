import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')

class ExplodingArrows():
	name = '!explodingarrows'

	desc = 'Arrows explode when they hit the ground'

	synt = '!explodingarrows <on|off|status>'

	looping = False

	admin = True
	
	cheer = 61
	
	cat = 'arrows'

	@loop(seconds = 0.1)
	async def loop_func(self):
		if self.looping:
			with MCRcon("127.0.0.1", PASSW) as mcr:
				resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run summon tnt')
				resp = mcr.command('/kill @e[type=arrow,nbt={inGround:1b}]')
				#print (resp)
				mcr.disconnect()
				
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
		if self.looping:
			print ('Running Exploding arrows off...')

			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say Exploding arrows disabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"exploding arrows disabled\",\"color\":\"red\"}]')
				#print (resp)
				mcr.disconnect()

			self.looping = False
			self.loop_func.stop()
			try:
				await message.channel.send(message.author.mention + ' !explodingarrows disabled')
			except:
				boop = False
			
	async def runCheer(self, user, amount):
		print ('Running lava arrows on...')
		with MCRcon("127.0.0.1", PASSW) as mcr:
			resp = mcr.command('/tellraw @a [{\"text\":\"' + user + ': exploding arrows enabled\",\"color\":\"green\"}]')
			mcr.disconnect()

		self.looping = True
		self.loop_func.start()
			
	async def run(self, message):
		#Cheer toggle
		try:
			if (' on' not in message.content) and (' off' not in message.content) and (' status' not in message.content):
				message.content = message.content + ' on'
		except:
			if (' on' not in message) and (' off' not in message) and (' status' not in message):
				message = message + ' on'
			
		if message.content.split(' ')[1].lower() == 'on' and not self.looping:
			print ('Running Exploding arrows on...')

			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say Exploding arrows enabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"exploding arrows enabled\",\"color\":\"green\"}]')
				#print (resp)
				mcr.disconnect()

			self.looping = True
			self.loop_func.start()
			await message.channel.send(message.author.mention + ' !explodingarrows enabled')
		elif message.content.split(' ')[1].lower() == 'off' and self.looping:
			await self.stop()
			
		elif message.content.split(' ')[1].lower() == 'status':
			if self.looping:
				await message.channel.send(message.author.mention + ' !explodingarrows is on')
			else:
				await message.channel.send(message.author.mention + ' !explodingarrows is off')

		else:
			await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
