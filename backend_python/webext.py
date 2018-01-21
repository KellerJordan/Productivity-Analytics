import sys
import json
import struct

class Messenger(object):
    _lengthSize = 4

    def __init__(self):
        self._msgQueue = []

    def listen(self):
        """
           Waits for a message to appear on the stream and adds it
           to the message queue.
        """
        msgLength = self._getMsgLength()

        if msgLength == -1:
            return False

        msgBody = self._readMsg(msgLength)

        self._msgQueue.append(msgBody)

        return True

    def receive(self):
        """
            Returns the next message in the message queue. If there are
            no messages on the queue this function will block until there
            is.
        """
        if len(self._msgQueue) == 0:
            self.listen()

        return self._msgQueue.pop(0)

    def send(self, data):
        """
            Sends a collection of data through the channel.
        """
        jsonStr = json.dumps(data).encode('utf-8')

        self._write(jsonStr)

    def _read(self, numBytes):
        return sys.stdin.buffer.read(numBytes)

    def _write(self, msgBytes):
        packedLength = struct.pack('@I', len(msgBytes))

        sys.stdout.buffer.write(packedLength)
        sys.stdout.buffer.write(msgBytes)
        sys.stdout.buffer.flush()

    def _getMsgLength(self):
        lengthData = self._read(Messenger._lengthSize)

        # The stream has reached EOF, there is no more data to be read.
        if len(lengthData) == 0:
            return -1

        if len(lengthData) != Messenger._lengthSize:
            raise BufferError('Reached EOF before size could be read.')

        return struct.unpack('@I', lengthData)[0]

    def _readMsg(self, numBytes):
        rawData = self._read(numBytes)

        if len(rawData) != numBytes:
            raise BufferError('Prematurely reached EOF.')

        return json.loads(rawData.decode('utf-8'))
