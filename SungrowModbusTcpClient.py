from pymodbus.client.sync import ModbusTcpClient
from Crypto.Cipher import AES

priv_key = b'Grow#0*2Sun68CbE'
NO_CRYPTO1 = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
NO_CRYPTO2 = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
GET_KEY = b'\x68\x68\x00\x00\x00\x06\xf7\x04\x0a\xe7\x00\x08'
HEADER = bytes([0x68, 0x68])

class SungrowModbusTcpClient(ModbusTcpClient):
    def __init__(self, **kwargs):
        ModbusTcpClient.__init__(self, **kwargs)
        self.fifo = bytes()
        self.key = None

    def _getkey(self):
        self._send(GET_KEY)
        self.key_packet = self._recv(25)
        self.pub_key = self.key_packet[9:]
        if (self.pub_key != NO_CRYPTO1) and (self.pub_key != NO_CRYPTO2):
           self.key = bytes(a ^ b for (a, b) in zip(self.pub_key, priv_key))
           self.decipher = AES.new(self.key, AES.MODE_ECB)
           self._send = self._send_cipher
           self._recv = self._recv_decipher
        else:
           self.key = b'no encryption'

    def connect(self):
        result = ModbusTcpClient.connect(self)
        if result and not self.key:
           self._getkey()
        self.fifo = bytes()
        return result

    def close(self):
        ModbusTcpClient.close(self)
        self.key = None
        self.fifo = bytes()

    def _send_cipher(self, request):
        length = len(request)
        padding = 16 - (length % 16)
        self.transactionID = request[:2]
        request = HEADER + bytes(request[2:]) + bytes([0xff for i in range(0, padding)])
        crypto_header = bytes([1, 0, length, padding])
        encrypted_request = crypto_header + self.decipher.encrypt(request)
        return ModbusTcpClient._send(self, encrypted_request) - len(crypto_header) - padding

    def _recv_decipher(self, size):
        #print('*** size', size)
        if size is None:
           recv_size = 1
        else:
           recv_size = size

        if len(self.fifo) == 0:
            header = ModbusTcpClient._recv(self, 4)
            #print('*** header', header)
            if header and len(header) == 4:
               packet_len = int(header[2])
               padding = int(header[3])
               length = packet_len + padding
               #print('*** length', length, packet_len, padding)
               encrypted_packet = ModbusTcpClient._recv(self, length)
               #print('*** encrypted_packet', encrypted_packet)
               if encrypted_packet and len(encrypted_packet) == length:
                  packet = self.decipher.decrypt(encrypted_packet)
                  packet = self.transactionID + packet[2:]
                  #print('*** packet', packet)
                  self.fifo = self.fifo + packet[:packet_len]

        recv_size = min(recv_size, len(self.fifo))
        #print('*** recv_size', recv_size)
        result = self.fifo[:recv_size]
        self.fifo = self.fifo[recv_size:]
        #print('*** fifo', self.fifo)
        #print('*** result', result)
        return result
