import os
import glob
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove


def funca():
    file_path = 'main_imonlyhuman.sql'
    fh, abs_path = mkstemp()
    i = 0

    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line.startswith('('):
                    i += 1
                    line = list(line)
                    idx = f"{i:02}"
                    line[1], line[2] = idx[0], idx[1]
                    line = ''.join(line)
                new_file.write(line)

    copymode(file_path, abs_path)
    remove(file_path)
    move(abs_path, file_path)


if __name__ == '__main__':
    funca()
    print()