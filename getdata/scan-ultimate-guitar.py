"""
* scan-ultimate-guitar.py
for each artist in 'artists', scans chord chart index, compiles list of chord
chart urls, and scans each chord chart for chords, outputting as text file and
printing to the console.
"""
import urllib.request as rq

artists = [
# "a-ha",
# "depeche_mode",
# "duran_duran",
# "eurythmics",
"gary_numan",
# "michael_jackson",
# "new_order",
# "soft_cell",
# "tears_for_fears",
# "the_human_league",
# "ultravox",
# "yazoo"
]

chordurls = []
for artist in artists:
    url = "https://www.ultimate-guitar.com/tabs/"+artist+"_tabs.htm"
    print(url)
    while 1 == 1: # loop until there are no more pages for this artist
        page = rq.urlopen(url)
        page_str = str(page.read())
        page_str = page_str[page_str.find("<!-- tabs -->"):]

        chordpages = page_str.split("<tr")[3:]
        for cp in chordpages:
            # filter out <a href=" and ">
            url = cp[cp.find("<a href")+9:cp.find("crd.htm\">")+7]
            if (len(url) > 0):
                chordurls.append(url)

        # if there is another page listing chord charts, go to that page
        next_index = page_str.find("Next")
        if (next_index > 0):
            url = "https://www.ultimate-guitar.com"+page_str[page_str.rfind("<a href=", 0, next_index)+9:next_index-13]
            print(url)
        # else, go to next artist
        else:
            print("last page")
            break

url_file = open("chord-urls.txt", "w")

for url in chordurls:
    print(url)
    url_file.write(url + '\n')
print("found " + str(len(chordurls)) + " chord charts")
url_file.close()

chords_file = open("chords.txt", "w")

chords = []
for url in chordurls:
    page = rq.urlopen(url)
    page_str = str(page.read())
    page_str = page_str[page_str.find("<pre class=\"js-tab-content\">")+28:]
    page_str = page_str[:page_str.find("</pre>")]

    print(url)

    chords.append("new_song")
    chords.append('\n')
    chords_file.write("\n\n\nnew song: " + url + "\n\n")

    # filter out clutter characters
    page_str = page_str.replace("["," ")
    page_str = page_str.replace("]"," ")
    page_str = page_str.replace("."," ")
    page_str = page_str.replace("\""," ")
    page_str = page_str.replace("\\r","\n")
    page_str = page_str.replace("\\t","    ")
    page_str = page_str.replace("\\\\","\\")
    page_str = page_str.replace(","," ")
    lines = page_str.split("\\n")[1:]
    for line in lines:
        # only use lines starting with a chord (i.e. "<span>")
        # or with a section header, e.g. "verse", "CHORUS"
        if (len(line) > 0 and line[0] == "<"):
            line = line.strip()
            line = line.replace("<span>","")
            line = line.replace("</span>","")
            chords.extend(line.split(" "))
            chords.append('\n')
            chords_file.write(line + '\n')
        elif (len(line) < 10 and (
                line.find("chorus") > -1 or
                line.find("Chorus") > -1 or
                line.find("CHORUS") > -1)):
            chords.append("chorus")
            chords.append('\n')
            chords_file.write("chorus\n")
        elif (len(line) < 10 and (
                line.find("verse") > -1 or
                line.find("Verse") > -1 or
                line.find("VERSE") > -1)):
            chords.append("verse")
            chords.append('\n')
            chords_file.write("verse\n")
        elif (len(line) < 10 and (
                line.find("bridge") > -1 or
                line.find("Bridge") > -1 or
                line.find("BRIDGE") > -1)):
            chords.append("bridge")
            chords.append('\n')
            chords_file.write("bridge\n")
    chords_file.write("\nend of song\n")
    chords.append("song_end")
    chords.append('\n')
    chords.append('\n')

chords_file.close()
for chord in chords:
    if (chord.find('\n') > -1):
        print()
    elif (len(chord) > 0):
        print(chord, end=" ")
