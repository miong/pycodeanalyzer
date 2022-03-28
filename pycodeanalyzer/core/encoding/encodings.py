import magic


class Encoding:
    """Encoding class.

    This class allow to deduce file encoding using libmagic.
    """

    def __init__(self) -> None:
        self.magic = magic.Magic(
            mime_encoding=True,
        )

    def getFileEncoding(self, file: str) -> str:
        return self.magic.from_file(file)
