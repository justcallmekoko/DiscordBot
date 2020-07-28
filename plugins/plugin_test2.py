class Test2():
	name = '!test2'

	desc = 'Run Test2 plugin'

	synt = '!test2'

	async def run(self, message):
		await message.channel.send(message.author.mention + ' Hello from Test2 plugin')
