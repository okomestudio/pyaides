from os import SEEK_END


def tail(stream, n=10, block_size=1024, ignore_ending_newline=False):
    lines = []
    eol = b"\n"
    suffix = b""
    stream.seek(0, SEEK_END)
    stream_length = stream.tell()
    seek_offset = 0

    while -seek_offset < stream_length:
        seek_offset -= block_size
        if -seek_offset > stream_length:
            # Limit if we ran out of file (can't seek backward from start)
            block_size -= -seek_offset - stream_length
            if block_size == 0:
                break
            seek_offset = -stream_length
        stream.seek(seek_offset, SEEK_END)
        buf = stream.read(block_size)

        # Search for line end.
        if ignore_ending_newline and seek_offset == -block_size and buf[-1] == eol:
            buf = buf[:-1]
        pos = buf.rfind(eol)
        if pos != -1:
            # Found line end.
            return buf[pos + 1 :] + suffix

        suffix = buf + suffix

    # One-line file
    lines.append(suffix)
    return eol.join(lines[::-1])
