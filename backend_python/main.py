#!/usr/bin/env python3
import sys
import webext

msg = webext.Messenger()

def main():
    counter = 0

    while msg.listen():
        message = msg.receive()

        counter += 1
        response = {'count': counter, 'value':message}

        msg.send(response)

    return 0

if __name__ == '__main__':
    sys.exit(main())
