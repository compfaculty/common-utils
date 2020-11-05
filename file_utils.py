"""Misc file utils"""

import os, sys
from multiprocessing import Array, Process
from ctypes import c_char_p
from pathlib import Path

def split_file(filepath: str, lines_per_file=50):
    """ Splits a large text file into smaller ones, based on line count

    Original is left unmodified.

    Resulting text files are stored in the same directory as the original file.

    Useful for breaking up text-based logs or blocks of login credentials.

    """

    path, filename = os.path.split(filepath)
    counter = 0
    with open(filepath, 'r') as fd:
        name, ext = os.path.splitext(filename)
        try:
            w = open(os.path.join(path, '{}_{}{}'.format(name, 0, ext)), 'w')
            for i, line in enumerate(fd):
                if not i % lines_per_file:
                    # possible enhancement: don't check modulo lpf on each pass
                    # keep a counter variable, and reset on each checkpoint lpf.
                    w.close()
                    filename = os.path.join(path, '{}_{}{}'.format(name, counter, ext))
                    w = open(filename, 'w')
                    counter += 1
                w.write(line)
        finally:
            w.close()


def split_by(path, chunks=10):
    """Split file to many files by chunks of lines

    :param path: file to split
    :param chunks: the number of lines to write per file
    :return: None
    """

    def _split(sarr, fname, start, end):
        curpath = fname.with_name(f"{fname.stem}_{start}{fname.suffix}")
        with curpath.open("w") as new_fd:
            new_fd.writelines([s.decode("utf-8") for s in sarr[start:end]])
    try:
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError("Not a file")
        if p.stat().st_size == 0:
            return
        with p.open('r') as fd:
            lines = [line.encode("utf-8") for line in fd.readlines() if line != '\n']

        shared_lines = Array(c_char_p, lines, lock=False)
        workers = []
        for i in range(0, len(lines), chunks):
            workers.append(Process(target=_split, args=(shared_lines, p, i, i + chunks)))
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(len(workers)*60)
    except (Exception,) as ex:
        sys.stderr.write(f"Error: {ex}")
        return 1
    else:
        print("OK")
        return 0


if __name__ == "__main__":
    split_by("/home/alexg/projects/bash.txt", 50)
