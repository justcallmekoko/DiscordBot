import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')

class TorchArrows():
	name = '!torcharrows'

	desc = 'Arrows place torches when they hit the ground'

	synt = '!torcharrows <on|off|status>'

	looping = False

	admin = True
	
	cheer = 51

	@loop(seconds = 0.1)
	async def loop_func(self):
		if self.looping:
			with MCRcon("127.0.0.1", PASSW) as mcr:
				resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run setblock ~0 ~0 ~0 torch')
				resp = mcr.command('/kill @e[type=arrow,nbt={inGround:1b}]')
				#print (resp)
				mcr.disconnect()
				
	async def stop(self, message):
		if self.looping:
			print ('Running torch arrows off...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say torch arrows disabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"torch arrows disabled\",\"color\":\"red\"}]')
				#print (resp)
				mcr.disconnect()

			self.looping = False
			self.loop_func.stop()
			await message.channel.send(message.author.mention + ' !torcharrows disabled')

	async def run(self, message):
		#Cheer toggle
		if (' on' not in message.content) and (' off' not in message.content) and (' status' not in message.content):
			message.content = message.content + ' on'
			
		if message.content.split(' ')[1].lower() == 'on' and not self.looping:
			print ('Running torch arrows on...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say torch arrows enabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"torch arrows enabled\",\"color\":\"green\"}]')
				#print (resp)
				mcr.disconnect()

			self.looping = True
			self.loop_func.start()
			await message.channel.send(message.author.mention + ' !torcharrows enabled')
		elif message.content.split(' ')[1].lower() == 'off' and self.looping:
			await self.stop(message)
			
		elif message.content.split(' ')[1].lower() == 'status':
			if self.looping:
				await message.channel.send(message.author.mention + ' !torcharrows is on')
			else:
				await message.channel.send(message.author.mention + ' !torcharrows is off')

		else:
			await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
