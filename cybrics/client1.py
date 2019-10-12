import socket
import sys
import os
import struct

def read_exact(sock, elen):
    data = ''
    while len(data) < elen:
        data += sock.recv(elen-len(data))
    return data


def stor(sock):
    fname = raw_input("Path to uploaded file:")
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

def retr(sock):
    fname = raw_input("file you want to retreive:")
    try:
        sock.send('R')
        sock.send(struct.pack("<L", len(fname)))
        sock.send(fname)
    except:
        print "conn closed?"
        return False
    data = sock.recv(4)
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
    while still_run:
        still_run = process(s)

if __name__ == "__main__":
    main()
