#!/usr/bin/env python3
import sys
import webext
import userscripts

msg = webext.Messenger()

def main():
    while msg.listen():
        message = msg.receive()

        results = userscripts.execute(message)
        response = {'messages': results}

        msg.send(response)

    return 0

if __name__ == '__main__':
    sys.exit(main())
