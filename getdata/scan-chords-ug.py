import urllib.request as rq

url = "https://tabs.ultimate-guitar.com/y/yazoo/mr_blue_crd.htm"

page = rq.urlopen(url)
page_str = str(page.read())
page_str = page_str[page_str.find("<pre class=\"js-tab-content\">")+28:]
page_str = page_str[:page_str.find("</pre>")]

# print(page_str)


lines = page_str.split("\\n")[1:]
chords = []
for line in lines:
    # chord_raw = chord_raw[:chord_raw.find("</span>")]
    if (len(line) > 0 and line[0] == "<"):
        line = line.strip()
        line = line.replace("<span>","")
        line = line.replace("</span>","")
        line = line.replace("\\r","")
        chords.append(line)
        print(line)

# for chord_raw in chords:
# while 1 == 1:
