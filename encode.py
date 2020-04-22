import mutagen.id3

def fix(files, enecode, decode):
    for fileName in files:
        if str(fileName).lower().endswith(".mp3"):
            id3 = mutagen.id3.ID3(fileName)
            for keyvalue in id3.items():
                key = keyvalue[0]
                value = keyvalue[1]
                if isinstance(getattr(value, "text", [None])[0], str) and value.encoding == 0:
                    try:
                        for i in range(len(value.text)):
                            value.text[i] = value.text[i].encode(enecode).decode(decode)
                        value.encoding = 3
                        # print("Changing: " + mp3file)
                        id3.save()
                    except UnicodeError:
                        pass
                    except Exception as err:
                        print("Error: {0} ----- Tag: [{1}] in file {2}".format(str(err), key, fileName))
                        # raise
