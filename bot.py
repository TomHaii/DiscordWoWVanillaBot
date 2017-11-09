import logging, os, discord, asyncio
from selenium import webdriver
from PIL import Image

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
	print('logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')

@client.event
async def on_message(message):
	if message.content.startswith('!help'):
		await client.send_message(message.channel, 'Screenshotting item - "!finditem #VANILLAGAMINGITEMID" - Example -> !finditem 18402')
		await client.send_message(message.channel, 'Finding player - "!findplayer #NAME"')
	elif (message.content.startswith('!finditem')):
		await client.send_message(message.channel, 'Looking for item...')
		foundFile = False
		try:
			newArgs = message.content.split(' ')
			print (newArgs)
			if (len(newArgs) == 2):
				takeimage(newArgs[1])
				try:
					with open(str(newArgs[1]) + '.png', 'rb') as f:
						await client.send_file(message.channel, f)
						foundFile = True
				except:
					await client.send_message(message.channel, 'Error Finding Item, make sure you pass the right item ID')
			else:
				await client.send_message(message.channel, 'Command Error')
		except ValueError:
			await client.send_message(message.channel, 'Error Finding Item, make sure you passed the right parameters')
		if foundFile:
			os.remove(str(newArgs[1]) + '.png')
	elif (message.content.startswith('!findplayer')):
		await client.send_message(message.channel, 'Looking for Player...')
		try:
			newArgs = message.content.split(' ')
			if (len(newArgs) == 2):
				try:
					await client.send_message(message.channel, findplayer(newArgs[1]))
				except:
					await client.send_message(message.channel, "Couldn't find player")
		except:
			await client.send_message(message.channel, "Couldn't find player")


def takeimage(itemID):
	browser = webdriver.Chrome('C:\chromedriver.exe')
	#browser.maximize_window()
	browser.get('http://db.vanillagaming.org/?item=' + itemID)
	browser.get_screenshot_as_file(str(itemID) + 'Web.png')
	img = Image.open(str(itemID) + 'Web.png')
	picBluePixelsCount = 0
	img = img.convert("RGBA")
	pixdata = img.load()
	width, height = img.size
	widthOffset = 90
	heightOffset = 280
	for y in range(height):
		for x in range(width):
			if pixdata[x, y] == (36, 36, 36, 255):
				pixdata[x, y] = (255, 255, 255, 0)
	#counting blue pixels in order to determine image size
	for newY in range(height):
		if pixdata[130, newY] == (8, 13, 33, 255):
			picBluePixelsCount += 1
	print (str(picBluePixelsCount) + ' Blue Pixels')
	try:
		img2 = img.crop((widthOffset, heightOffset, 500, (picBluePixelsCount * 1.7) + heightOffset))
		img2.save(str(itemID) + '.png', "PNG")
	except:
		if(os.path.isfile(str(itemID) + '.png')):
			os.remove(str(itemID) + '.png')
			print('Error Saving Image')
	os.remove(str(itemID) + 'Web.png')
	browser.close()


def findplayer(playerName):
	realmPlayers = 'http://realmplayers.com/CharacterViewer.aspx?realm=Ely&player='
	return (realmPlayers + playerName)

client.run('token')