import urllib
import os

URL = "http://www.vgmusic.com/music/console/nintendo/wiiu/"
FILE_TYPE = ".mid"
PATH = "/Users/vaasu/Desktop/musicfiles/"

page = urllib.urlopen(URL)
page_str = str(page.read())

midi_place = 0
name_start = -1
song_list =[]
files_downloaded = 0
print (len(page_str))

while (midi_place != -1):
	# print (midi_place)
	midi_place += 5
	midi_place = page_str.find(FILE_TYPE,midi_place)
	name_start = midi_place - 1
	char  = ""
	while (char != '"'):
		char = page_str[name_start]
		name_start -= 1;
	new_song = page_str[name_start+2: midi_place+4]
	# print(new_song)
	song_list += [new_song]
	files_downloaded += 1
	print (files_downloaded)
# print (song_list)

for i in range (len(song_list)-1): # -1 just in case. We don't need every song, and we don't want errors
	song=song_list[i]
	song_name = os.path.join(PATH, song)
	urllib.urlretrieve (URL + song, song_name)
