#!/usr/bin/env python3
import os
import mutagen.id3

MUSICROOT = "./"
ENCCODE_FROM = "iso-8859-1"
DECODE_TO = "windows-1256"


def find_mp3(dir_path):
  for child in os.listdir(dir_path):
    child = os.path.join(dir_path, child)
    if os.path.isdir(child):
      for mp3 in find_mp3(child):
        yield mp3
    elif child.lower().endswith(".mp3"):
      yield child


for mp3file in find_mp3(MUSICROOT):
  id3 = mutagen.id3.ID3(mp3file)
  for keyvalue in id3.items():
    key = keyvalue[0]
    value = keyvalue[1]
    if isinstance(getattr(value, "text", [None])[0], str) and value.encoding == 0:
      try:
        for i in range(len(value.text)):
          value.text[i] = value.text[i].encode(ENCCODE_FROM).decode(DECODE_TO)
        value.encoding = 3
        #print("Changing: " + mp3file)
        id3.save()
      except UnicodeError:
        pass
      except Exception as err:
        print("Error: {0} ----- Tag: [{1}] in file {2}".format(str(err), key, mp3file))
        #raise