import urllib

URL = "http://www.vgmusic.com/music/console/nintendo/virtualboy/"

page = urllib.urlopen(URL)
page_str = str(page.read())

midi_place = 0
name_start = -1
song_list =[]
print (len(page_str))

while (midi_place != -1):
	# print (midi_place)
	midi_place += 5
	midi_place = page_str.find(".mid",midi_place)
	name_start = midi_place - 1
	char  = ""
	while (char != '"'):
		char = page_str[name_start]
		name_start -= 1;
	new_song = page_str[name_start+2: midi_place+4]
	print(new_song)
	song_list += [new_song]
print (song_list)

for i in range (len(song_list)-1):
	song=song_list[i]
	print (URL + song)
	print(song)
	urllib.urlretrieve (URL + song, song)
