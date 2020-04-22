#!/usr/bin/env python3
import sys
import os
import encode
import rating
import split
import all
import info

def findFiles(dir: str):
    for child in os.listdir(dir):
        child = os.path.join(dir, child)

        if os.path.isdir(child):
            for mp3 in findFiles(child):
                yield mp3
        else:
            yield child


if len(sys.argv) == 2:
    operation = str(sys.argv[0]).lower()
    path = str(sys.argv[1])
elif len(sys.argv) >= 3:
    operation = str(sys.argv[1]).lower()
    path = str(sys.argv[2])
else:
    print("the arguments most is opration path")
    exit(1)

print(operation)
print(path)
print("Operation: {0} in Path: {1}".format(operation, path))

if operation == "encode":
    encode.fix(findFiles(path), "iso-8859-1", "windows-1256")
    exit()

if operation == "rating":
    # rating.printEmails(findFiles(path))
    # rating.printFiles(findFiles(path))
    rating.changeEmail(findFiles(path), "daneshvar.ho", ["daneshvar.hu", "Windows Media Player 9 Series",
                                                         "Daneshvar.Hu", "banshee", "Banshee", "quodlibet@lists.sacredchao.net", "no@email", "MusicBee"])
    exit()

if operation == "split":
    split.gener(findFiles(path), [";", "/", ","])
    exit()

if operation == "all":
    all.fix(findFiles(path), [";", "/", ","], [";", "/", "//", "&"])
    exit()

if operation == "info":
    info.printTags(findFiles(path))
    exit()

if operation == "info-rating":
    info.printRating(findFiles(path))
    exit()
