from fuzzywuzzy import process
import logging, os, discord, asyncio,sys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from PIL import Image

FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'
GECKODRIVER_PATH = r'C:\geckodriver.exe'
cachefolder = os.getcwd() + '\cache\\'
cachetrigger = False;
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
		await client.send_message(message.channel, 'Finding player :\n- "!findplayer #NAME"')
	elif (message.content.startswith('!finditem')):
		await client.send_message(message.channel, 'Looking for item...')
		foundFile = False
		delete = True
		try:
			newArgs = message.content.split(' ')
			print (newArgs)
			if (len(newArgs) >= 2):
				if (len(newArgs) == 2):
					if newArgs[1].isdigit():
						itemid = newArgs[1]
					else:
						itemid = finditemidfromname(newArgs[1])
				else:
					name = ''
					for i in range(1, len(newArgs)):
						name += newArgs[i]
						if i  != len(newArgs):
							name += ' '
					itemid = finditemidfromname(name)
				if findimagefromcache(itemid):
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
			print(str(itemid) + '.png removed ')
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
		print('Tooltip for item id : %s found at %s\nSaved at %s' % (itemID, str('http://db.vanillagaming.org/?item=' + str(itemID)), str(cachefolder+ str(itemID) + '.png')))
	except:
		print('Tooltip for item id : %s not found at %s' % (itemID, str('http://db.vanillagaming.org/?item=' + str(itemID))))
	browser.close()


def findplayer(playerName):
	realmPlayers = 'http://realmplayers.com/CharacterViewer.aspx?realm=Ely&player='
	return (realmPlayers + playerName)

def findimagefromcache(itemID):
	filename = itemID + '.png'
	print('Trying to find ' + filename)
	for files in os.walk(cachefolder):
		for file in files:
			if filename in file:
				print('Item found in cache folder')
				return True
	print('Item not found in cache folder')
	return False

if __name__ == '__main__':
	myargs = sys.argv
	if '-c' in myargs:
		cachetrigger = True
		if not os.path.exists(os.path.dirname(cachefolder)):
		    try:
		        os.makedirs(os.path.dirname(cachefolder))
		    except:
		        print('Error while creating the cache folder')
	print('Cache is {0}'.format(cachetrigger))
	print(myargs)

def finditemidfromname(name):
	items = {}
	with open('items.csv', 'r') as f:
		for line in f:
			if line == '\n':
				continue
			data = line.split(',')
			items[data[1]] = data[0]
		return items[process.extractOne(name, items.keys())[0]]

client.run('token')
