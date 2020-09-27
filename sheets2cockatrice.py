import urllib.request, csv, re

print("Enter the ids/urls of the sheets:")

def getURLs():
    out = []
    while True:
        tmp = input("Next sheet: ")
        if tmp == "": return out
        out.append(tmp.strip())

def writeCard(card, url = "https://raw.githubusercontent.com/jdbener/Project-Delta-Playtesting-Files/master/Images/", setCode = "pd"):
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
    # CMC
    cmc = 0
    result = re.findall("([ROYGBPXZC_]|1?[0-9])", card["Cost"])
    for r in result:
        try:
            if str(r).isdigit(): cmc += int(r)
            else: cmc += 1
        except: pass
    # Color
    color = "\n <color>"+card['Color'].upper().replace("GENERIC", "C")[0]+"</color>"
    if color == "\n <color>C</color>": color = ""
    # related
    related = ""
    result = re.findall("<i>([\S\s]*?)<\\/i>", card["Rules"])
    for r in result:
        if any(bad in r.lower() for bad in ["\"", ")", "as", "strength in numbers", "symmetry", "enrage"]): continue
        related += "\n <related>" + r.strip(" \t\n'") + "</related>"
        #print(r)
    if "<u>Doubt" in card['Rules']: related += "\n <related>Doubt</related>"
    if "<u>Warrent" in card['Rules']: related += "\n <related>Incarceration</related>"

    return "\n"+"<card>"\
        +"\n "+"<name>"+card['Name'].replace(",", "")+"</name>"\
        +"\n "+"<set picURL=\""+url+card['Slot']+"_001.png\">"+setCode+"</set>"\
        + color\
        +"\n "+"<manacost>"+card['Cost']+"</manacost>"\
        +"\n <cmc>" + str(cmc) + "</cmc>"\
        +"\n "+"<type>"+type+"</type>"\
        + pt\
        + transient\
        + related\
        +"\n "+"<tablerow>"+str(row)+"</tablerow>"\
        +"\n "+"<text>"+card["Rules"].replace("][", "").replace("<p>", "\n\n<p>").replace("<br>", "\n").replace("</br>", "\n").replace("<br/>", "\n").replace("~@", card['Name'].split(",")[0]).replace("~", card['Name'])+"</text>"\
        +"\n"+"</card>"

urls = getURLs()
out = r'''<?xml version="1.0" encoding="UTF-8"?>
<cockatrice_carddatabase version="3">
 <sets>
  <set>
   <name>pd</name>
   <longname>Project Delta</longname>
   <settype>Custom</settype>
   <releasedate>2020-09-19</releasedate>
  </set>
 </sets>
<cards>'''
for sheet in urls:
    sheet = sheet.replace("https://docs.google.com/spreadsheets/d/","").split("/")[0]
    sheet = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/" + sheet + "/gviz/tq?tqx=out:csv")\
        .read().decode('utf-8').replace(" (0-4 = common, 5-8 = uncommon, 9-10 = rare)", "")
    
    reader = csv.DictReader(sheet.splitlines())
    for card in reader:
        if len(card['Slot']):
            try: 
                if not (card['Name'] == 'R' or card['Name'] == 'U' or card['Name'] == 'C'): out += writeCard(card)
            except:
                print("card parsing failed.")
                continue
out += "\n</cards>\n</cockatrice_carddatabase>"
#print(out)

f = open("cards.xml", "w")
f.write(out)
f.close()
