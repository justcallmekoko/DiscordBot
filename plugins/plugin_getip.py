from requests import get

class Getip():
	name = '!getip'

	desc = 'Get public ip of minecraft bot'

	synt = '!getip'

	loop = False

	admin = True
	
	cheer = -1
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	async def run(self, message):
		ip = get('https://api.ipify.org').text
		await message.channel.send(message.author.mention + ' ' + str(ip))
		
	async def stop(self, message):
		self.loop = False
