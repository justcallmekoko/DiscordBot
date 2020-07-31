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

	@loop(seconds = 0.1)
	async def loop_func(self):
		if self.looping:
			with MCRcon("127.0.0.1", PASSW) as mcr:
				resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b}] run fill ~0 ~0 ~0 ~0 ~0 ~0 lava')
				resp = mcr.command('/kill @e[type=arrow,nbt={inGround:1b}]')
				#print (resp)
				mcr.disconnect()

	async def run(self, message):
		if message.content.split(' ')[1].lower() == 'on' and not self.looping:
			print ('Running lava arrows on...')
			self.looping = True
			self.loop_func.start()
			await message.channel.send(message.author.mention + ' !lavaarrows enabled')
		elif message.content.split(' ')[1].lower() == 'off' and self.looping:
			print ('Running lava arrows off...')
			self.looping = False
			self.loop_func.stop()
			await message.channel.send(message.author.mention + ' !lavaarrows disabled')
		elif message.content.split(' ')[1].lower() == 'status':
			if self.looping:
				await message.channel.send(message.author.mention + ' !lavaarrows is on')
			else:
				await message.channel.send(message.author.mention + ' !lavaarrows is off')

		else:
			await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
