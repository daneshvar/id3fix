import mutagen
import mutagen.id3
import mutagen.flac
import os.path


def changeID3(tags: mutagen.id3.ID3, old, new):
    try:
        tag = tags.get("POPM:" + old)
        if tag:
            if tags.get("POPM:" + new):
                tags.pop("POPM:" + old)
            else:
                tag.email = new
                tags.add(tag)
            return True
    except Exception as err:
        print("Error: {0} in file {1}".format(str(err), tags.filename))

    return False

def changeFLAC(tags: mutagen.flac.FLAC, old, new):
    r = False

    try:
        tag = tags.get("rating:" + old)
        if tag:
            if not tags.get("rating:" + new):  # check duplicate
                tags["rating:" + new] = tag
            tags.pop("rating:" + old)  # remove duplicate
            r = True

        tag = tags.get("playcount:" + old)
        if tag:
            if not tags.get("playcount:" + new):  # check duplicate
                tags["playcount:" + new] = tag
            tags.pop("playcount:" + old)  # remove duplicate
            r = True
    except Exception as err:
        print("Error: {0} in file {1}".format(str(err), tags.filename))

    return r

def changeEmail(files, new, olds):
    for fileName in files:
        ext = os.path.splitext(fileName)[1].lower()
        if ext == ".mp3":
            try:
                tags = mutagen.id3.ID3(fileName)
            except mutagen.id3.ID3NoHeaderError:
                pass
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            s = False
            for old in olds:
                s = s or changeID3(tags, old, new)
            if s:
                try:
                    tags.save()
                except Exception as err:
                    print("Error: {0} on save file {1}".format(str(err), fileName))

        elif ext == ".flac":
            try:
                tags = mutagen.flac.FLAC(fileName)
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            s = False
            for old in olds:
                s = s or changeFLAC(tags, old, new)
            if s:
                try:
                    tags.save()
                except Exception as err:
                    print("Error: {0} on save file {1}".format(str(err), fileName))

def printEmails(files):
    l = []
    for fileName in files:
        ext = os.path.splitext(fileName)[1].lower()
        if ext == ".mp3":
            try:
                tags = mutagen.id3.ID3(fileName)
            except mutagen.id3.ID3NoHeaderError:
                pass
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, _) in tags.items():
                s = str(key)
                if s.startswith("POPM:"):
                    if not s in l:
                        l.append(s)

        elif ext == ".flac":
            try:
                tags = mutagen.flac.FLAC(fileName)
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, _) in tags.items():
                s = str(key)
                if s.startswith("rating:") or s.startswith("playcount:"):
                    if not s in l:
                        l.append(s)
    print(l)

def printFiles(files):
    for fileName in files:
        ext = os.path.splitext(fileName)[1].lower()
        if ext == ".mp3":
            print(fileName)
            try:
                tags = mutagen.id3.ID3(fileName)
            except mutagen.id3.ID3NoHeaderError:
                pass
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, values) in tags.items():
                s = str(key)
                if s.startswith("POPM:"):
                    print(s, values)

        elif ext == ".flac":
            print(fileName)
            try:
                tags = mutagen.flac.FLAC(fileName)
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, values) in tags.items():
                s = str(key)
                if s.startswith("rating:") or s.startswith("playcount:"):
                    print(s, values)
