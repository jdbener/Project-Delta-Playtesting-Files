import urllib.request, csv, re

print("Enter the ids/urls of the sheets:")

def getURLs():
    out = []
    while True:
        tmp = input("Next sheet: ")
        if tmp == "": return out
        out.append(tmp.strip())

def writeCard(card, url = "https://raw.githubusercontent.com/jdbener/Project-Delta-Playtesting-Files/master/Images/", setCode = "pd"):
    # Set
    result = re.search("([\S]*?)_[0RrOoYyGgBbPpMmCc][CcUuRr]?_", card['Setted Slot'])
    if result:
        setCode = result.group(1).lower()
    # Type
    type = card['Type']
    if card['Subtype'] != "": type += " - " + card['Subtype']
    # Power/Health
    pt = ""
    if card["Has PH"] == "True": pt = "\n <pt>" + card["Attack Power"] + "/" + card["Health"] + "</pt>"
    # Tablerow
    row = 1
    if "Effect" in card["Type"]: row = 3
    elif "Generator" in card["Type"]: row = 0
    elif card["Has PH"] == "True": row = 2
    # Rarity
    rarity = "common"
    try:
        if 4 < int(card["Effectiveness"]) < 9: rarity = "uncommon"
        if int(card["Effectiveness"]) >= 9: rarity = "rare"
    except: pass
    # Token status
    transient = ""
    if "transient" in card['Subtype'].lower(): transient = "\n <token>1</token>"
    if card['Slot'][-1].isalpha(): transient = "\n <token>1</token>"    # All 001b, 001c, etc cards are marked as tokens
    #if "personal" in card['Subtype'].lower(): transient = "\n <token>1</token>"
    # CMC
    cmc = 0
    result = re.findall("([ROYGBPXZC_]|1?[0-9])", card["Cost"])
    for r in result:
        try:
            if str(r).isdigit(): cmc += int(r)
            else: cmc += 1
        except: pass
    # Color
    colors = [x[0] if len(x) > 0 else x for x in card['Color Calculator'].upper().split(" ")]
    colors += card['Color'].upper().replace("GENERIC", " ")[0]
    colors = list(set(colors))
    colors.sort()
    color = ""
    for x in colors: color += x + " "
    color = "\n <color>" + color.strip() + "</color>"
    if color == "\n <color></color>": color = ""
    # related
    relatedSrc = []
    result = re.findall("<i>([\S\s]*?)<\\/i>", card["Rules"])
    for r in result:
        if any(bad in r.lower() for bad in ["\"", ")", "as", "strength in numbers", "symmetry", "enrage"]): continue
        relatedSrc.append(r.strip(" \t\n'"))
        #print(r)
    if "<u>Doubt" in card['Rules']: relatedSrc.append("Doubt")
    if "<u>Warrent" in card['Rules']: relatedSrc.append("Incarceration")
    if "<i>'Tip" in card['Rules']: relatedSrc.append("Tip")
    related = ""
    relatedSrc = list(set(relatedSrc))
    relatedSrc.sort()
    for r in relatedSrc:
        related += "\n <related>" + r + "</related>"

    return "\n"+"<card>"\
        +"\n "+"<name>"+card['Name'].replace(",", "")+"</name>"\
        +"\n "+"<set picURL=\""+url+card['Setted Slot']+"_001.png\">"+setCode+"</set>"\
        + color\
        +"\n "+"<manacost>"+card['Cost']+"</manacost>"\
        +"\n <cmc>" + str(cmc) + "</cmc>"\
        +"\n "+"<type>"+type+"</type>"\
        + pt\
        + transient\
        + related\
        +"\n "+"<tablerow>"+str(row)+"</tablerow>"\
        +"\n "+"<text>"+card["Rules"].replace("][", "").replace("<p>", "\n\n<p>").replace("<br>", "\n").replace("</br>", "\n").replace("<br/>", "\n").replace("~@", "<i>" + card['Name'].split(",")[0] + "</i>").replace("~", "<i>" + card['Name'] + "</i>").strip("\n ")+"</text>"\
        +"\n"+"</card>"

def getCardSets(reader):
    sets = []
    for card in reader:
        result = re.search("([\S]*?)_[0RrOoYyGgBbPpMmCc][CcUuRr]?_", card['Setted Slot'])
        if result:
            sets.append(result.group(1).lower())
            sets = list(set(sets))
    sets.sort()
    return sets




urls = getURLs()
print("Processessing...")
outHeader = r'''<?xml version="1.0" encoding="UTF-8"?>
<cockatrice_carddatabase version="3">
 <sets>
  <set>
   <name>pd</name>
   <longname>Project Delta</longname>
   <settype>Custom</settype>
   <releasedate>2020-09-19</releasedate>
  </set>'''
out = ""
cardSets = []
alreadyPrintedCards = []
for sheet in urls:
    sheet = sheet.replace("https://docs.google.com/spreadsheets/d/","").split("/")[0]
    sheet = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/" + sheet + "/gviz/tq?tqx=out:csv")\
        .read().decode('utf-8').replace(" (0-4 = common, 5-8 = uncommon, 9-10 = rare)", "")

    reader = csv.DictReader(sheet.splitlines())
    for x in getCardSets(reader): cardSets.append(x)
    reader = csv.DictReader(sheet.splitlines())
    for card in reader:
        if len(card['Setted Slot']) and card['Setted Slot'] != '0':
            try:
                # Confirm that the card hasn't already been processed
                if not (card['Name'] in alreadyPrintedCards):
                    if not (card['Name'] == 'R' or card['Name'] == 'U' or card['Name'] == 'C'): out += writeCard(card)
                    alreadyPrintedCards.append( str(card['Name']) )
                else:
                    print("card: ", card['Name'], " already found in card database... skipping.")

            except:
                print("card parsing failed.")
                raise
out += "\n</cards>\n</cockatrice_carddatabase>"
# Different set for each set we found while scanning through the database files
for s in set(cardSets):
    setMap = {"rt": "Rising Tensions", "rs": "Rising Spirits"}
    if s in setMap.keys(): outHeader += '\n  <set>\n   <name>' + s + '</name>\n   <longname>' + setMap[s] + '</longname>\n   <settype>Custom</settype>\n   <releasedate>2020-09-19</releasedate>\n  </set>'
    else: outHeader += '\n  <set>\n   <name>' + s + '</name>\n   <longname>' + s.upper() + '</longname>\n   <settype>Custom</settype>\n   <releasedate>2020-09-19</releasedate>\n  </set>'
outHeader += '''
 </sets>
<cards>'''
out = outHeader + out
#print(out)

f = open("cards.xml", "w")
f.write(out)
f.close()
