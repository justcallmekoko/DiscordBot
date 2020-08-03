import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop

PASSW = os.getenv('RCON_PASSWORD')

class FuArrows():
	name = '!fuarrows'

	desc = 'Arrows place Fuck You signs when they hit the ground'

	synt = '!fuarrows <on|off|status>'

	looping = False

	admin = True

	@loop(seconds = 0.1)
	async def loop_func(self):
		if self.looping:
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b,pickup:2b}] run setblock ~ ~ ~ minecraft:oak_sign[rotation=12]{Text1:\"\\"Fuck you\\"\"}')
				resp = mcr.command('/execute at @e[type=arrow,nbt={inGround:1b}] run fill ~-3 ~ ~-3 ~3 ~ ~3 minecraft:torch')
				resp = mcr.command('/kill @e[type=arrow,nbt={inGround:1b}]')
				#print (resp)
				mcr.disconnect()

	async def run(self, message):
		if message.content.split(' ')[1].lower() == 'on' and not self.looping:
			print ('Running fu arrows on...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say fu arrows enabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"fu arrows enabled\",\"color\":\"green\"}]')
				#print (resp)
				mcr.disconnect()

			self.looping = True
			self.loop_func.start()
			await message.channel.send(message.author.mention + ' !fuarrows enabled')
		elif message.content.split(' ')[1].lower() == 'off' and self.looping:
			print ('Running fu arrows off...')
			with MCRcon("127.0.0.1", PASSW) as mcr:
				#resp = mcr.command('/say fu arrows disabled')
				resp = mcr.command('/tellraw @a [{\"text\":\"fu arrows disabled\",\"color\":\"red\"}]')
				#print (resp)
				mcr.disconnect()

			self.looping = False
			self.loop_func.stop()
			await message.channel.send(message.author.mention + ' !fuarrows disabled')
		elif message.content.split(' ')[1].lower() == 'status':
			if self.looping:
				await message.channel.send(message.author.mention + ' !fuarrows is on')
			else:
				await message.channel.send(message.author.mention + ' !fuarrows is off')

		else:
			await message.channel.send(message.author.mention + ' ' + str(message.content) + ' is not a recognized command')
