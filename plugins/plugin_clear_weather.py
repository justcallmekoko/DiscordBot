import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')

class ClearWeather():
	name = '!clearweather'

	desc = 'Enable clear weather only'

	synt = '!clearweather <on|off|status>'

	looping = False

	admin = True
	
	cheer = 2
	
	cat = 'weather'

	@loop(seconds = 1)
	async def loop_func(self):
		if self.looping:
                        with MCRcon("127.0.0.1", PASSW) as mcr:
                                resp = mcr.command('/weather clear')
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
			
	async def runCheer(self, user, amount):
		print ('Running clear weather enabled on...')
		with MCRcon("127.0.0.1", PASSW) as mcr:
			resp = mcr.command('/tellraw @a [{\"text\":\"' + user + ': clear weather enabled\",\"color\":\"green\"}]')
			mcr.disconnect()

		self.looping = True
		self.loop_func.start()
								
	async def stop(self, message):
		if self.looping:
			print ('Running clear weather off...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say clear weather disabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"clear weather disabled\",\"color\":\"red\"}]')
				#print (resp)
				mcr.disconnect()
			self.looping = False
			self.loop_func.stop()
			try:
				await message.channel.send(message.author.mention + ' !clearweather disabled')
			except:
				this_fucking_thing_didnt_work = True

	async def run(self, message):
		#Cheer toggle
		try:
			if (' on' not in message.content) and (' off' not in message.content) and (' status' not in message.content):
				message.content = message.content + ' on'
		except:
			if (' on' not in message) and (' off' not in message) and (' status' not in message):
				message = message + ' on'
			
		if message.content.split(' ')[1].lower() == 'on' and not self.looping:
			print ('Running clear weather on...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say clear weather enabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"clear weather enabled\",\"color\":\"green\"}]')
				#print (resp)
				mcr.disconnect()
			self.looping = True
			self.loop_func.start()
			await message.channel.send(message.author.mention + ' !clearweather enabled')
		elif message.content.split(' ')[1].lower() == 'off' and self.looping:
			await self.stop()
			
		elif message.content.split(' ')[1].lower() == 'status':
			if self.looping:
				await message.channel.send(message.author.mention + ' !clearweather is on')
			else:
				await message.channel.send(message.author.mention + ' !clearweather is off')

		else:
			await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
