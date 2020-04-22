import mutagen
import mutagen.id3
import mutagen.flac
import os.path


def printTags(files):
    for fileName in files:
        ext = os.path.splitext(fileName)[1].lower()
        if ext == ".mp3":
            print("############################################################")
            print(fileName)
            try:
                tags = mutagen.id3.ID3(fileName)
            except mutagen.id3.ID3NoHeaderError:
                pass
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, value) in tags.items():
                # if isinstance(getattr(value, "text", [None])[0], str):
                print(key + ":", value)
        elif ext == ".flac":
            print(fileName)
            try:
                tags = mutagen.flac.FLAC(fileName)
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, value) in tags.items():
                # if isinstance(getattr(value, "text", [None])[0], str):
                print(key + ":", value)

def printRating(files):
    for fileName in files:
        ext = os.path.splitext(fileName)[1].lower()
        b = False
        if ext == ".mp3":
            try:
                tags = mutagen.id3.ID3(fileName)
            except mutagen.id3.ID3NoHeaderError:
                pass
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, value) in tags.items():
                if str(key).startswith("POPM:"):
                    if not b:
                        print("############################################################")
                        print(fileName)
                        b = True
                    print(key + ":", value)
        elif ext == ".flac":
            try:
                tags = mutagen.flac.FLAC(fileName)
            except Exception as err:
                print("Error: {0} on open file {1}".format(str(err), fileName))
            for (key, value) in tags.items():
                if str(key).startswith("rating:"):
                    if not b:
                        print("############################################################")
                        print(fileName)
                        b = True
                    print(key + ":", value)
