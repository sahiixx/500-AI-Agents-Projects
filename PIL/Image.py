"""Lightweight stand-in for :mod:`PIL.Image`.

The real Pillow package cannot be installed in the execution environment,
so this module provides just enough functionality for the repository tests.
Only the operations exercised by the tests are implemented:

* :func:`open` returning a context-managed image object
* exposure of :attr:`format` and :attr:`size`
* a :meth:`verify` method that re-parses the file

The implementation intentionally focuses on PNG and JPEG files because those
are the formats used in the fixture images.
"""

from __future__ import annotations

from dataclasses import dataclass
import builtins
import os
import struct
from typing import IO, Iterator, Tuple, Union

__all__ = ["ImageFile", "UnidentifiedImageError", "open"]

PathType = Union[str, "os.PathLike[str]"]


class UnidentifiedImageError(ValueError):
    """Raised when an image cannot be identified."""


@dataclass
class ImageFile:
    """Simplified representation of a Pillow :class:`Image.Image`."""

    path: str
    format: str
    size: Tuple[int, int]

    def __enter__(self) -> "ImageFile":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()

    def verify(self) -> None:
        """Re-parse the file to ensure it remains readable."""
        _ = _load_image_metadata(self.path)

    def close(self) -> None:
        """Included for API compatibility; no persistent resources."""
        return None


def open(fp: PathType | IO[bytes], mode: str | None = None) -> ImageFile:
    """Open an image file.

    Parameters mirror :func:`PIL.Image.open` for the limited subset needed by
    the tests.  Only path-like inputs are supported; attempting to open an
    already open file object raises :class:`TypeError` to signal unsupported
    usage.
    """

    if mode not in (None, "r"):
        raise ValueError("Only read mode is supported in the lightweight stub")

    if hasattr(fp, "read"):
        raise TypeError("File-object inputs are not supported in the lightweight stub")

    path = os.fspath(fp)
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    fmt, size = _load_image_metadata(path)
    return ImageFile(path=path, format=fmt, size=size)


# -- Internal helpers -----------------------------------------------------

JPEG_MARKERS_WITH_SIZE = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


def _load_image_metadata(path: str) -> Tuple[str, Tuple[int, int]]:
    with builtins.open(path, "rb") as fp:
        signature = fp.read(8)
        if signature.startswith(b"\x89PNG\r\n\x1a\n"):
            return _read_png(fp)
        if signature.startswith(b"\xFF\xD8"):
            fp.seek(0)
            return _read_jpeg(fp)
        raise UnidentifiedImageError(f"Unsupported image format in {path}")


def _read_png(fp: IO[bytes]) -> Tuple[str, Tuple[int, int]]:
    # After the signature, the first chunk must be IHDR containing
    # the width and height as big-endian unsigned integers.
    chunk_header = fp.read(8)
    if len(chunk_header) != 8:
        raise UnidentifiedImageError("Incomplete PNG header")
    length, chunk_type = struct.unpack(">I4s", chunk_header)
    if chunk_type != b"IHDR" or length < 8:
        raise UnidentifiedImageError("PNG missing IHDR chunk")
    data = fp.read(length)
    if len(data) != length:
        raise UnidentifiedImageError("Truncated PNG IHDR data")
    width, height = struct.unpack(">II", data[:8])
    return "PNG", (width, height)


def _iter_jpeg_segments(fp: IO[bytes]) -> Iterator[Tuple[int, bytes]]:
    data = fp.read()
    if not data.startswith(b"\xFF\xD8"):
        raise UnidentifiedImageError("Invalid JPEG signature")
    offset = 2
    end = len(data)
    while offset < end:
        if data[offset] != 0xFF:
            raise UnidentifiedImageError("Malformed JPEG marker")
        # Skip fill bytes (0xFF padding)
        while offset < end and data[offset] == 0xFF:
            offset += 1
        if offset >= end:
            break
        marker = data[offset]
        offset += 1
        if marker == 0xD9:  # EOI
            break
        if marker == 0xDA:  # Start of Scan
            if offset + 2 > end:
                raise UnidentifiedImageError("Truncated JPEG scan header")
            length = struct.unpack(">H", data[offset : offset + 2])[0]
            offset += 2 + length
            break
        if offset + 2 > end:
            raise UnidentifiedImageError("Truncated JPEG segment length")
        length = struct.unpack(">H", data[offset : offset + 2])[0]
        offset += 2
        segment_data = data[offset : offset + length - 2]
        if len(segment_data) != length - 2:
            raise UnidentifiedImageError("Incomplete JPEG segment")
        yield marker, segment_data
        offset += length - 2


def _read_jpeg(fp: IO[bytes]) -> Tuple[str, Tuple[int, int]]:
    for marker, segment in _iter_jpeg_segments(fp):
        if marker in JPEG_MARKERS_WITH_SIZE:
            if len(segment) < 5:
                raise UnidentifiedImageError("JPEG SOF segment too short")
            height, width = struct.unpack(">HH", segment[1:5])
            return "JPEG", (width, height)
    raise UnidentifiedImageError("Could not determine JPEG dimensions")
