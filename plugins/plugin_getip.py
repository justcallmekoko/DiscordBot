from requests import get

class Getip():
	name = '!getip'

	desc = 'Get public ip of minecraft bot'

	synt = '!getip'

	async def run(self, message):
		ip = get('https://api.ipify.org').text
		await message.channel.send(message.author.mention + ' ' + str(ip))
