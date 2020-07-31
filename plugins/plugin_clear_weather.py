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

	@loop(seconds = 1)
	async def loop_func(self):
		if self.looping:
                        with MCRcon("127.0.0.1", PASSW) as mcr:
                                resp = mcr.command('/weather clear')
                                #print (resp)
                                mcr.disconnect()

	async def run(self, message):
		if message.content.split(' ')[1].lower() == 'on' and not self.looping:
			print ('Running clear weather on...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
                                resp = mcr.command('/say clear weather enabled')
                                #print (resp)
                                mcr.disconnect()
			self.looping = True
			self.loop_func.start()
		elif message.content.split(' ')[1].lower() == 'off' and self.looping:
			print ('Running clear weather off...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
                                resp = mcr.command('/say clear weather disabled')
                                #print (resp)
                                mcr.disconnect()
			self.looping = False
			self.loop_func.stop()
		elif message.content.split(' ')[1].lower() == 'status':
			if self.looping:
				await message.channel.send(message.author.mention + ' !clearweather is on')
			else:
				await message.channel.send(message.author.mention + ' !clearweather is off')

		else:
			await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
