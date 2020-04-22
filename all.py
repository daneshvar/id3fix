import mutagen
import mutagen.id3
import mutagen.flac
import os.path
import re

def fix(files, genreSep, peopleSep):
    genreSep = "|".join(genreSep)
    peopleSep = "|".join(peopleSep)

    for fileName in files:
        ext = os.path.splitext(fileName)[1].lower()
        try:
            if ext == ".mp3" or ext == ".flac":
                file = mutagen.File(fileName, easy=True)
            if not file:
                continue
            # if ext == ".mp3":
            #     file = mutagen.id3.ID3(fileName)
            # elif ext == ".flac":
            #     tags = mutagen.flac.FLAC(fileName)
        except mutagen.id3.ID3NoHeaderError:
            pass
        except Exception as err:
            print("Error: {0} on open file {1}".format(str(err), fileName))

        # print(fileName)
        # for k, _ in file.items():
        #     print(k)

        s = False
        s = s or fixTag(file, "genre", genreSep)
        s = s or fixTag(file, "artist", peopleSep)
        s = s or fixTag(file, "composer", peopleSep)
        s = s or fixTag(file, "lyricist", peopleSep)
        s = s or fixTag(file, "album")
        s = s or fixTag(file, "title")
        s = s or fixTag(file, "albumartist")
        # s = s or setComment(file, "comment", comment)

        if s:
            try:
                file.save()
            except Exception as err:
                print("Error: {0} on save file {1}".format(str(err), fileName))

def fixTag(file, name, sep=""):
    try:
        tag = file.get(name)
        if tag:
            values = []
            for s in tag:
                if sep == "":
                    values.append(str(s).strip().title())
                else:
                    items = re.split(sep, str(s).strip())
                    for item in items:
                        values.append(str(item).strip().title())
            values = list(dict.fromkeys(values))
            if set(values) != set(tag):
                file[name] = values
                return True
    except Exception as err:
        print("Error: {0} in file {1}".format(str(err), file.filename))
    return False
