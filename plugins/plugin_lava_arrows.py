import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')

class LavaArrows():
	name = '!lavaarrows'

	desc = 'Arrows turn into lava when they hit the ground'

	synt = '!lavaarrows <on|off|status>'

	looping = False

	admin = True
	
	cheer = 71
	
	cat = 'arrows'
	
	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False

	@loop(seconds = 0.1)
	async def loop_func(self):
		if self.looping:
			with MCRcon("127.0.0.1", PASSW) as mcr:
				resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run fill ~0 ~0 ~0 ~0 ~0 ~0 lava')
				resp = mcr.command('/kill @e[type=arrow,nbt={inGround:1b}]')
				#print (resp)
				mcr.disconnect()
				
	def checkBits(self, bits):
		if bits == self.cheer:
			return True
		else:
			return False
				
	async def stop(self, message):
		if self.looping:
			print ('Running lava arrows off...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say lava arrows disabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"lava arrows disabled\",\"color\":\"red\"}]')
				#print (resp)
				mcr.disconnect()
			self.looping = False
			self.loop_func.stop()
			try:
				await message.channel.send(message.author.mention + ' !lavaarrows disabled')
			except:
				boop = True
				
	async def runCheer(self, user, amount):
		print ('Running lava arrows on...')
		with MCRcon("127.0.0.1", PASSW) as mcr:
			resp = mcr.command('/tellraw @a [{\"text\":\"' + user + ': lava arrows enabled\",\"color\":\"green\"}]')
			mcr.disconnect()

		self.looping = True
		self.loop_func.start()
		
				
	# Function to activate loop
	async def toggle(self, message):
		print ('Running lava arrows on...')
		with MCRcon("127.0.0.1", PASSW) as mcr:
			#resp = mcr.command('/say lava arrows enabled')
			try:
				resp = mcr.command('/tellraw @a [{\"text\":\"' + message + ': lava arrows enabled\",\"color\":\"green\"}]')
			except Exception as e:
				resp = mcr.command('/tellraw @a [{\"text\":\"lava arrows enabled\",\"color\":\"green\"}]')
			#print (resp)
			mcr.disconnect()

		self.looping = True
		self.loop_func.start()
		
		try:
			await message.channel.send(message.author.mention + ' !lavaarrows enabled')
		except:
			boop = True

	async def run(self, message):
		#Check if this was executed with cheer
		did_run = False
		try:
			if (' on' not in message.content) and (' off' not in message.content) and (' status' not in message.content):
				message.content = message.content + ' on'
		except Exception as e:
			if (' on' not in message) and (' off' not in message) and (' status' not in message):
				#message = message + ' on'
				print('Running the shit')
				did_run = True
				await self.toggle(message.split(' ')[1])
				return
		try:	
			if message.content.split(' ')[1].lower() == 'on' and not self.looping:
				await self.toggle(message)
				
			elif message.content.split(' ')[1].lower() == 'off' and self.looping:
				await self.stop(message)
				
			elif message.content.split(' ')[1].lower() == 'status':
				if self.looping:
					await message.channel.send(message.author.mention + ' !lavaarrows is on')
				else:
					await message.channel.send(message.author.mention + ' !lavaarrows is off')

			else:
				await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
		except Exception as e:
			this_is_fucking_bullshit = True
