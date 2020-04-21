#!/usr/bin/env python3
import sys
import os
import mutagen
import mutagen.id3
import mutagen.flac
import rating

ENCCODE_FROM = "iso-8859-1"
DECODE_TO = "windows-1256"


def findFiles(dir: str):
    for child in os.listdir(dir):
        child = os.path.join(dir, child)

        if os.path.isdir(child):
            for mp3 in findFiles(child):
                yield mp3
        else:
            yield child


def fixEncode(dirPath):
    for fileName in findFiles(dirPath):
        if str(fileName).lower().endswith(".mp3"):
            id3 = mutagen.id3.ID3(fileName)
            for keyvalue in id3.items():
                key = keyvalue[0]
                value = keyvalue[1]
                if isinstance(getattr(value, "text", [None])[0], str) and value.encoding == 0:
                    try:
                        for i in range(len(value.text)):
                            value.text[i] = value.text[i].encode(ENCCODE_FROM).decode(DECODE_TO)
                        value.encoding = 3
                        # print("Changing: " + mp3file)
                        id3.save()
                    except UnicodeError:
                        pass
                    except Exception as err:
                        print("Error: {0} ----- Tag: [{1}] in file {2}".format(str(err), key, fileName))
                        # raise


if len(sys.argv) == 2:
    operation = str(sys.argv[0]).lower()
    path = str(sys.argv[1])
elif len(sys.argv) == 3:
    operation = str(sys.argv[1]).lower()
    path = str(sys.argv[2])
else:
    print("the arguments most is opration path")
    exit(1)

print(operation)
print(path)
print("Operation: {0} in Path: {1}".format(operation, path))

if operation == "encode":
    fixEncode(path)
    exit()

if operation == "rating":
    # rating.printEmails(findFiles(path))
    # rating.printFiles(findFiles(path))
    rating.changeEmail(findFiles(path), "daneshvar.ho", ["daneshvar.hu", "Windows Media Player 9 Series",
                                                         "Daneshvar.Hu", "banshee", "Banshee", "quodlibet@lists.sacredchao.net", "no@email", "MusicBee"])
    exit()
