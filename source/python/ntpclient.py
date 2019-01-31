'''

(C) 2014 David Lettier.

http://www.lettier.com/

NTP client.

'''

from socket import AF_INET, SOCK_DGRAM # For setting up the UDP packet.
import sys
import socket
import struct, time # To unpack the packet sent back and to convert the seconds to a string.
import datetime

run_count = 0
fail_count = 0


def printlog(*argv):
    now = datetime.datetime.now()
    print now, argv


def getntptime():
    fail = False
    try:
        host = "pool.ntp.org"; # The server.
        port = 123; # Port.
        read_buffer = 1024; # The size of the buffer to read in the received UDP packet.
        address = ( host, port ); # Tuple needed by sendto.
        data = '\x1b' + 47 * '\0'; # Hex message to send to the server.

        epoch = 2208988800L; # Time in seconds since Jan, 1970 for UNIX epoch.

        client = socket.socket( AF_INET, SOCK_DGRAM ); # Internet, UDP
        client.settimeout(10)

        start = time.time()
        client.sendto( data, address ); # Aend the UDP packet to the server on the port.

        data, address = client.recvfrom( read_buffer ); # Get the response and put it in data and put the send socket address into address.
        end = time.time()

        if len(data) != 48:
            print("FAIL: Corrupt or incomplete packet")
            fail = True
        printlog(data, address)
        printlog("Time taken", end - start)

        t = struct.unpack( "!12I", data )[ 10 ]; # Unpack the binary data and get the seconds out.

        t -= epoch; # Calculate seconds since the epoch.

        printlog("Time = %s" % time.ctime( t )); # Print the seconds as a formatted string.
    except socket.error as msg:
        print("Socket error", msg)
        fail = True

    return not fail


def main(count=1, sleepseconds=1):
    global run_count
    global fail_count
    for i in range(count):
        if not getntptime():
            fail_count = fail_count + 1
        time.sleep(sleepseconds)
        run_count = run_count + 1


if __name__ == "__main__":
    global run_count
    global fail_count
    count = 1
    sleepseconds = 1
    try:
        if len(sys.argv) > 1:
            count = int(sys.argv[1])
        if len(sys.argv) > 2:
            sleepseconds = int(sys.argv[2])
        main(count, sleepseconds)
    except KeyboardInterrupt:
        printlog('Interrupted')
        exit(1)
    finally:
        pass
        printlog('Run count: ', run_count)
        printlog('Fail count: ', fail_count)
