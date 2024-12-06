""" Document Dataclass Module. """

from __future__ import annotations
from pathlib import Path
from typing import Union
from dataclasses import dataclass, asdict
import base64


@dataclass
class Document:
    """Dataclass for the ANT Document object. Use this object to parse
    and encode documents for up- and downloading to ANT CDE.
    
    Attributes:
        name (str): Name of the document.
        extension (str): Extension of the document.
        data (str): Base64 encoded document data.
    """

    name: str
    extension: str
    data: str

    @staticmethod
    def _read(document_path: Union[Path, str]) -> bytes:
        """Read a document file."""
        with open(document_path, "rb") as file:
            content = file.read()
        return content

    @staticmethod
    def _parse(content_bytes: bytes) -> bytes:
        """Parse a document to a base64 encoded string."""
        return base64.b64encode(content_bytes)

    @classmethod
    def parse_from_path(cls, document_path: Path | str) -> Document:
        """Parse a document to a Document object with encoded to base64 content.

        Parameters
        ----------
        document_path : Path | str
            Path to the document.

        Returns
        -------
        Document
            Document object.

        Raises
        ------
        Exception
            If document cannot be found or opened, or content is not in utf-8 format
        """
        if isinstance(document_path, str):
            document_path = Path(document_path)

        content_bytes = cls._read(document_path)
        encoded_file = cls._parse(content_bytes)
        return cls(
            name=document_path.stem,
            extension=document_path.suffix,
            data=encoded_file.decode("utf-8"),
        )

    def encode_to_file(self, file_path: Path | str = "") -> None:
        """Encode the document data object to a file.

        Args:
            file_path (Path | str, optional): Path to document. Defaults to ''.

        Raises:
            TypeError: Error saving file from ANT.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        full_path = file_path / f"{self.name}{self.extension}"

        try:
            with open(full_path, "wb+") as file:
                file.write(base64.b64decode(self.data.encode("utf-8")))
        except Exception as e:
            raise TypeError(f"Error saving file from ANT: {e}")

    def as_dict(self) -> dict:
        """Return the document object as a dictionary."""
        return asdict(self)
