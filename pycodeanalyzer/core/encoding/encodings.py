import magic


class Encoding:
    def __init__(self):
        self.magic = magic.Magic(
            mime_encoding=True,
        )

    def getFileEncoding(self, file):
        return self.magic.from_file(file)
