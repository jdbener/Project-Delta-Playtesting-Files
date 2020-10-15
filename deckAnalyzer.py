import urllib.request, csv, re, untangle
from io import BytesIO
from PIL import Image

print("Enter the ids/urls of the sheets:")

def getURLs():
    out = []
    while True:
        tmp = input("Next sheet: ")
        if tmp == "": return out
        out.append(tmp.strip())
    return out

urls = getURLs()
db = {}
print("Building database")
for sheet in urls:
    sheet = sheet.replace("https://docs.google.com/spreadsheets/d/","").split("/")[0]
    sheet = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/" + sheet + "/gviz/tq?tqx=out:csv")\
        .read().decode('utf-8').replace(" (0-4 = common, 5-8 = uncommon, 9-10 = rare)", "")

    reader = csv.DictReader(sheet.splitlines())
    for card in reader:
        if len(card['Slot']):
            try:
                if not (card['Name'] == 'R' or card['Name'] == 'U' or card['Name'] == 'C'):
                    card['Name'] = card['Name'].replace(",", "")
                    db[card['Name']] = card
            except:
                print("card parsing failed.")
                continue
#print(out)

def getDeck():
    f = ""
    while isinstance(f, str):
        #try:
            tmp = input("Select deck: ")
            f = untangle.parse(tmp)
            #print(f)
        #except: continue
    return f
    
def imageIncrement(imageCount):
    imageCount[0] += 1
    if imageCount[0] >= 10:
        imageCount[0] = 0
        imageCount[1] += 1
    return imageCount

deck = getDeck()
mainPower = 0
totalPower = 0
imageCount = [0, 0]
image = Image.new('RGB', (1, 1), color = 'black')
print("Processing...")
for zone in deck.cockatrice_deck.zone:
    for card in zone.card:
        if(card['name'].strip() in db):
            # Deck Power
            if(zone['name'] == 'main'):
                mainPower += int(card['number']) * int(db[card['name']]['Effectiveness'])
            totalPower += int(card['number']) * int(db[card['name']]['Effectiveness'])
            
            # Images
            response = urllib.request.urlopen("https://raw.githubusercontent.com/jdbener/Project-Delta-Playtesting-Files/master/Images/"+db[card['name']]['Slot']+"_001.png")
            img = Image.open(BytesIO(response.read()))
            img = img.resize((int(512), int(512/img.size[0] * img.size[1])), Image.LANCZOS)
            if image.size == (1, 1): image = image.resize((img.size[0] * 10, img.size[1] * 7))
            
            for i in range(0, int(card['number'])):
                image.paste(img, (img.size[0] * imageCount[0], img.size[1] * imageCount[1]))
                imageCount = imageIncrement(imageCount)

image.save("deckImage.png")
print(image.size)
#image.show()            
            
print("Cards in deck: ", (imageCount[1] * 10 + imageCount[0]))
print("Main deck power: ", mainPower)
print("Total deck power: ", totalPower)
