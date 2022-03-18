import magic


class Encoding:
    def __init__(self) -> None:
        self.magic = magic.Magic(
            mime_encoding=True,
        )

    def getFileEncoding(self, file: str) -> str:
        return self.magic.from_file(file)
