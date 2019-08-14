from os import SEEK_END


def tail(stream: "file", n: int = 10, block_size: int = 1024):
    """Output the last part of the file.

    Args:
        stream:

    Return:
        str: The last part of the file.
    """
    lines = []
    eol = b"\n"
    suffix = b""
    stream.seek(0, SEEK_END)
    stream_length = stream.tell()
    seek_offset = 0

    # From the end, move the offset by block size until the entire stream is covered
    while -seek_offset < stream_length:
        seek_offset -= block_size

        if -seek_offset > stream_length:
            # Adjust block size to avoid going past the first byte of the file
            block_size -= -seek_offset - stream_length
            if block_size == 0:
                # This happens when the offset is at the first byte already
                break
            # Set the offset to the first byte
            seek_offset = -stream_length

        stream.seek(seek_offset, SEEK_END)
        buf = stream.read(block_size)

        # Search for line end.
        # if ignore_ending_newline and seek_offset == -block_size and buf[-1] == eol:
        #    buf = buf[:-1]

        pos = buf.rfind(eol)
        if pos != -1:
            # EOL found
            suffix = buf[pos + 1 :] + suffix
            seek_offset = seek_offset + pos

            # If the line is empty and at the end of the file, skip until non-empty line
            # is found
            if len(lines) == 0 and suffix == b"":
                continue

            lines.append(suffix)
            suffix = b""
            n -= 1
            if n == 0:
                return eol.join(lines[::-1])
        else:
            suffix = buf + suffix

    # One-line file
    lines.append(suffix)
    return eol.join(lines[::-1])
