import mutagen
import mutagen.id3
import mutagen.flac
import os.path

def changeID3(tags: mutagen.id3.ID3, sep):
    try:
        tag = tags.get("TCON")
        if tag:
            values = str(tag).split(sep)
            if len(values) > 1:
                tags.add(mutagen.id3.TCON(encoding=mutagen.id3.Encoding.UTF8, text=values))
                return True
    except Exception as err:
        print("Error: {0} in file {1}".format(str(err), tags.filename))

    return False

def changeFLAC(tags: mutagen.flac.FLAC, sep):
    try:
        tag = tags.get("genre")
        if tag:
            values = []
            for g in tag:
                values.extend(str(g).split(sep))
            values = list(dict.fromkeys(values))
            if set(values) != set(tag):
                tags["genre"] = values
                return True
    except Exception as err:
        print("Error: {0} in file {1}".format(str(err), tags.filename))

    return False

def gener(files, seperators):
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
            for sep in seperators:
                s = s or changeID3(tags, sep)
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
            for sep in seperators:
                s = s or changeFLAC(tags, sep)
            if s:
                try:
                    tags.save()
                except Exception as err:
                    print("Error: {0} on save file {1}".format(str(err), fileName))
