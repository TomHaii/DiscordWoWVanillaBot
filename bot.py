import logging, os, discord, asyncio,sys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from PIL import Image

FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'
GECKODRIVER_PATH = r'C:\geckodriver.exe'
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
cachefolder = r'\path\\'
cachetrigger = False;
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
		delete = True
		try:
			newArgs = message.content.split(' ')
			print (newArgs)
			if (len(newArgs) == 2):
				itemid = newArgs[1]
				if findimagefromcache(itemid):
					print('Found item in cache folder')
					delete = False
				else:
					print('Downloading File')
					takeimage(itemid)
				try:
					with open(cachefolder + itemid + '.png', 'rb') as f:
						await client.send_file(message.channel, f, content=str('http://db.vanillagaming.org/?item=' + str(itemid)))
						foundFile = True
				except:
					await client.send_message(message.channel, 'Error Finding Item, make sure you pass the right item ID')
			else:
				await client.send_message(message.channel, 'Command Error')
		except ValueError:
			await client.send_message(message.channel, 'Error Finding Item, make sure you passed the right parameters')
		#If cache argument has not passed, delete the item after sending it to Discord
		if delete and foundFile and cachetrigger is False: 
			os.remove(cachefolder + str(itemid) + '.png')
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
	try:
		browser.find_element_by_class_name('tooltip').screenshot(cachefolder + str(itemID) + '.png')
		print('Element at id : %s found' % itemID)
	except:
		print('Element at id : %s not found' % itemID)
	browser.close()


def findplayer(playerName):
	realmPlayers = 'http://realmplayers.com/CharacterViewer.aspx?realm=Ely&player='
	return (realmPlayers + playerName)

def findimagefromcache(itemID):
	filename = itemID + '.png'
	print('trying to find' + filename)
	for files in os.walk(cachefolder):
		for file in files:
			if filename in file:
				return True
	return False

if __name__ == '__main__':
	myargs = sys.argv
	if '-c' in myargs:
		cachetrigger = True
	print('Cache is {0}'.format(cachetrigger))
	print(myargs)


client.run('token')
