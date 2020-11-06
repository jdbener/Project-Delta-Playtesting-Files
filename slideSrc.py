import glob

out = "var slides = [\n"

files = glob.glob("Images/*.png")
files.sort()
for f in files:
    out += "\t{\n\t\tsrc: 'https://raw.githubusercontent.com/jdbener/Project-Delta-Playtesting-Files/master/" + f + "', // path to image\n\t\tw: 1344, // image width\n\t\th: 1872, // image height\n\t\ttitle: '" + f.replace("Images/", "") + "'\n\t},\n"
out += "];"

print(out);
