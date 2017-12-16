import logging, os, discord, asyncio?SYS
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from PIL import Image

FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'
GECKODRIVER_PATH = r'C:\geckodriver.exe'
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
	#We need Firefox to be able to screenshot the selected element and add the binary to be able to hide the window
	os.environ['MOZ_HEADLESS'] = '1'
	binary = FirefoxBinary(FIREFOX_PATH, log_file=sys.stdout)
	binary.add_command_line_options('-headless')
	browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH,firefox_binary=binary)

	browser.get('http://db.vanillagaming.org/?item=' + itemID)
	browser.find_element_by_class_name('tooltip').screenshot(str(itemID) + '.png')
	browser.close()


def findplayer(playerName):
	realmPlayers = 'http://realmplayers.com/CharacterViewer.aspx?realm=Ely&player='
	return (realmPlayers + playerName)

client.run('token')
