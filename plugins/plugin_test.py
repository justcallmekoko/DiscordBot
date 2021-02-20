class Test():
	name = '!test'

	desc = 'Run Test plugin'

	synt = '!test'

	loop = False

	admin = False
	
	cheer = 2

	async def run(self, message):
		await message.channel.send(message.author.mention + ' Hello from Test plugin')
		
	async def stop(self, message):
		self.loop = False
