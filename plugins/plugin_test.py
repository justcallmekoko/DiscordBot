class Test():
	name = '!test'

	desc = 'Run Test plugin'

	synt = '!test'

	async def run(self, message):
		await message.channel.send(message.author.mention + ' Hello from Test plugin')
