import os
import re
import sys
import asyncio
import discord
import time
import socket
import threading
from string import printable
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
import random
import pkgutil

sys.dont_write_bytecode = True

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

global TWITT
global twitch_server
global sock

load_dotenv()
TWITT = os.getenv('TWITCH_TOKEN')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PASSW = os.getenv('RCON_PASSWORD')

twitch_server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'willstunforfood'
channel = '#willstunforfood'

global obj_list
obj_list = []

path = os.path.join(os.path.dirname(__file__), "plugins")
modules = pkgutil.iter_modules(path=[path])

sock = socket.socket()

sock.connect((twitch_server, port))

sock.send(f"PASS {TWITT}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# Functions to work with twitch
def threaded_twitch():
	global sock
	global obj_list
	
	bad_chars = 'abcdefghijklmnopqrstuvwxyzABZDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()`~-_=+[{]}\|;:\'",<.>/?'
	
	print('Waiting for twitch shit...')

	while True:
		resp = sock.recv(2048).decode('utf-8')

		print(resp)
		
		contained_cheer = False
		
		cheer_amount = 0
		
		#Parse cheers
		
		for resp_sub in resp.split(' '):
			if 'Cheer' in str(resp_sub):
				raw_cheer_amount = resp_sub.replace(':51\r\n', '').replace('Cheer', '').replace('\n', '').replace(':', '')
				cheer_amount = ''.join(char for char in raw_cheer_amount if char in printable)
				contained_cheer = True
				print('Cheer amount: ' + str(cheer_amount))
		
		#for sub in str(resp).split(' '):
		#	if 'Cheer' in sub:
		#		#cheer_amount = int(float(sub.replace('Cheer', '').replace(':51\r\n', '')))
		#		cheer_amount = re.sub("[^0-9]", "", sub)
		#		contained_cheer = True
		#		print('Cheer amount: ' + str(cheer_amount))
		#		break
		
		bad_char_found = False
		
		for i in list(bad_chars):
			if str(i) in str(cheer_amount):
				bad_char_found = True
				
		if ((not re.search('[a-zA-Z]', str(cheer_amount))) and (not bad_char_found)):
			cheer_amount = re.sub("[^0-9]", "", str(cheer_amount))
			if (contained_cheer) and (int(cheer_amount) > 0):
				# Get bot category
				for obj in obj_list:
					if obj.checkBits(int(cheer_amount)):
						cat = obj.cat
						
				# Stop all plugins with same category
				for obj in obj_list:
					if obj.checkCat(cat):
						print('Stopping: ' + str(obj.name))
						run_stop = asyncio.run(obj.stop(resp))
					#await obj.stop(resp)
					
				# Find the plugin with the cheer amount
				for obj in obj_list:
					if obj.checkBits(int(cheer_amount)):
						found = True
						print('Found plugin: ' + obj.name)
						#if obj.admin and not admin:
						#	await message.channel.send(message.author.mention + ' ' + str(cmd) + ' only admins may run this command')
						#	break
						
						run_run = asyncio.run(obj.runCheer(obj.name + ' ' + str(resp).split('!')[0], int(cheer_amount)))
						#await obj.run(obj.name)
						break
		else:
			print('Cheer not valid: ' + str(cheer_amount))

class CustomClient(discord.Client):
	global obj_list

	# Loop that will just run in the background
#	@loop(seconds = 0.1)
#	async def main(self):
#		for obj in obj_list:
#			if obj.loop:
#				print ('Executing ' + str(obj.name))
#				await obj.run('loop on')
#			else:
#				print ('Not executing ' + str(obj.name))

#		with MCRcon("127.0.0.1", PASSW) as mcr:
#			resp = mcr.command('/weather clear')
#			print (resp)
		

	# Bot connects to discord server
	async def on_ready(self):
		print (f'{self.user} has connected to Discord!')

		for guild in client.guilds:
			if guild.name == GUILD:
				break

		print(
			f'\n{client.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})\n'
		)

		members = '\n - '.join([member.name for member in guild.members])
		print (f'Guild Members:\n - {members}\n')

		print ('Guild Roles:')
		for role in guild.roles:
			print('\t' + role.name)

		print ()



	# Member joins the discord server
	async def on_member_join(self, member):
		await member.create_dm()
		await member.dm_channel.send(
			f'Hi {member.name}, welcome to the server.'
		)

	# Bot received a message on discord server
	async def on_message(self, message):
		admin = False

		output = ''

		for guild in client.guilds:
                        if guild.name == GUILD:
                                break

		if message.author == client.user:
			return

		try:
			for role in message.author.roles:
				output = output + '['

				if (role.permissions.administrator) and (role.guild.id == guild.id):
					admin = True
					output = output + T
				else:
					output = output + W

				output = output + role.name + W + ']'
		except Exception as e:
			output = output + '[' + str(e) + ']'

		output = output + ' ' + message.author.name + ': ' + message.content

		print (output)

		# Work response
		if client.user.mentioned_in(message):
			await message.channel.send(message.author.mention + ' Don\'t talk to me')

		if message.content == '!muster':
                        await message.channel.send(message.author.mention + ' Here')

		# Check plugins
		found = False

		# Check if multipart command
		if ' ' in str(message.content):
			cmd = str(message.content).split(' ')[0]
		else:
			cmd = str(message.content)

		# Start reponse
		response = message.author.mention + '\n'

		# Check if general help
		if str(message.content) == '!help':
			found = True
			for obj in obj_list:
				response = response + str(obj.name) + '\t- ' + str(obj.desc) + '\n'

			await message.channel.send(response)
		elif '!help ' in str(message.content):
			found = True
			for obj in obj_list:
				if str(message.content).split(' ')[1] == str(obj.name):
					response = response + str(obj.synt)
			await message.channel.send(response)

		for obj in obj_list:
			if cmd == obj.name:
				found = True
				if obj.admin and not admin:
					await message.channel.send(message.author.mention + ' ' + str(cmd) + ' only admins may run this command')
					break
				await obj.run(message)
				break

		if list(str(cmd))[0] == '!' and not found:
			await message.channel.send(message.author.mention + ' ' + str(cmd) + ' is not a recognized command')



def get_class_name(mod_name):
	output = ""

	words = mod_name.split("_")[1:]

	for word in words:
		output += word.title()
	return output

for loader, mod_name, ispkg in modules:
	if mod_name not in sys.modules:

		loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])

		class_name = get_class_name(mod_name)
		loaded_class = getattr(loaded_mod, class_name)

		instance = loaded_class()
		obj_list.append(instance)

t = threading.Thread(target=threaded_twitch)
t.start()

client = CustomClient()
client.run(TOKEN)
client.main.start()