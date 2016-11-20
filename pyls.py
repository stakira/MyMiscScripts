#!/usr/bin/python

# This script is designed to mimic Linux list command (ls), except it doesn't show the full
# list of files and directories. Instead, It will tell you how many more items are
# there after first 20 rows.

# With "cd" aliased to "cd \!*; ls", terminal can potentially be flooded. The purpose of
# this script is to resolve this problem.

# Credit: http://www.pixelbeat.org/talks/python/ls.py.html

import os
import sys
import stat

def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

def get_mode_info(mode, filename):
    perms="-"
    colour="default"
    link=""

    if stat.S_ISDIR(mode):
        perms="d"
        colour="blue"
    elif stat.S_ISLNK(mode):
        perms="l"
        colour="cyan"
        link = os.readlink(filename)
        if not os.path.exists(filename):
            colour="red"
    elif stat.S_ISREG(mode):
        if mode & (stat.S_IXGRP|stat.S_IXUSR|stat.S_IXOTH): #bitwise operators
            colour="green"
    mode=stat.S_IMODE(mode)
    for who in "USR", "GRP", "OTH":
        for what in "R", "W", "X":
            #lookup attribute at runtime using getattr
            if mode & getattr(stat,"S_I"+what+who):
                perms=perms+what.lower()
            else:
                perms=perms+"-"
    #return multiple bits of info in a tuple
    return (perms, colour, link)

def get_rows(files):
    if not files:
        return 0
    widths = map(len, files)
    term_w, term_h = getTerminalSize()
    numfiles = len(widths)
    rows = 0
    cols_width = []
    while (not cols_width or sum(cols_width) - 2 > term_w):
        rows += 1
        cols_width = []
        for i in xrange(0, numfiles, rows):
            cols_width.append(max(widths[i : i + rows]) + 2)
    cols_width[-1] -= 2
    return rows, cols_width

def pyls():
    colors = {  "default" : "",
                "blue"    : "\x1b[01;34m",
                "cyan"    : "\x1b[01;36m",
                "green"   : "\x1b[01;32m",
                "red"     : "\x1b[01;05;37;41m"}

    files = os.listdir(os.getcwd())
    files = sorted(list(filter(lambda x: not x.startswith("."), files)))
    items = []
    for filename in files:
        #if filename.startswith("."): continue;
        try:
            stat_info=os.lstat(filename)
        except:
            sys.stderr.write("%s: No such file or directory\n" % filename)
            continue
        perms, color, link = get_mode_info(stat_info.st_mode, filename)
        items.append((filename, colors[color]))
    
    if len(files) == 0: exit();
    rows, cols_width = get_rows(files)
    cols = len(cols_width)
    for i in xrange(rows):
        if i > 19:
            sys.stdout.write("    \x1b[1m... and %d more items\x1b[00m\n" % (len(files) - i * cols))
            return
        for j in xrange(cols):
            if j * rows + i < len(files):
                file = files[j * rows + i]
                sys.stdout.write(items[j * rows + i][1] + file + "\x1b[00m")
                sys.stdout.write(" " * (cols_width[j] - len(file)))
        sys.stdout.write("\n")

if __name__ == "__main__":
    pyls()
