from contextlib import contextmanager

import pickle
import socket
import zlib


default_key = b'0A6HGhX9ryi-3E8DCEYnAGc53ZRnjFXI1rqV0qz-90w476TYk8HGjpOeuRVKxDsshQV25swDj8rMoYx6RMSQrLxt7c7d4jSltszirkZAJ5FC_4t78piHDIJCYtcTG5BE9MFHbkzmpz-KbL_nfKdMaKlB_qc-BqRkYn7qkzpt9LrWFUGtKGurwDBintLuL_2tpSTZlCrK7GqwHjIDTntnMoGdwI1wy1TkMDI--C5dBiitYQ8-fc_DDdR1KtdYhW1fvIEGzoAWsgparnqM2YsmI96DvjCmlzC2mx72swNqSXbxRGgMiUGQ2nGZ4axYEYTLgQHw6T2bX7vNkvfmEshCHH4y5zoXgORz0PYQOdznUavF9gyQWuLT1lMT0B-4olF4FJbY7qu_NCGouz7gel4LF3pz_T6AgreHNijtAQ3vaAES6D2Faftn9XRtSsqsMqK1fYEyPgcYxZmUe7qqrGf9EClrMNvLpu0gpS1mEKbUcSScgRmuuPC_LoCEsl5wpoWbl3LYdEH3y0YFXP6L434240Ed6yw26mXiA-qsL11_nAZhoczsER3cUf6WFAJTAF2YkPYQXrDxoTeE-mcjR7yTfsNIaoVturrbfSeEBs4oK4a_8OZIgd_LTTHam0giSxN8P_31AB8qR4_oziZYxbbUaYZHbfY_97ksbzCz_5dLGOVR3yDsE3V8BD10A1Ue9JCkLaxyj5vhuzbILFgpxSA-4lbixad1JwjcNK3CnP6I4FOmYfVRdN5hxBKuO1Mqssh7-BtaP8GjyHTaDscL0qOuJjUaXaa2AQK6nfIvDjA3oXBia2N13mEE2yvtnkj8GD7TxDpcGst6OQragKpvg4Js50-JzAX0-x2Ov_mvg_Ng7PvDvaEwFPL0WGGgvCaFadBZI2V1Ow_K8G8iUy9YEIBdGqEXL_CrQ3NLiYujZRFsKp9EKKP3yGoBaWS_DgXz1DI4XgViR5XjM0KjDUswbn4V2TYJXAwQVT_eGWEwOrE2obct7S7qHzjY5oPlZcF0Zf97ovP2-lBd5_cacJpsL_rIHzl8L_oWXDk4UD7jeMrY8RqTzZM3OvAzJYxnduQUK7IuphSZk_3WxlrMaHPLRkxBzZd0IjHbLOPaanCxF2X-yM0Xc-p5_3v0D1kSVdRx1CkjTGSm3SBIV5eCIwgRnh7w-fTbrq6wFJJTi8UkbYbtpv5VOYCX0_9rTut_o_pB2N0Mb3VE5fAJYweVDNFkwvbmQtBWjGogqsGtW_XopseuMwVgT82pPSDH_8s2KasZstCNlyaU-ejoJP4DHUA2W2tBNHE8VUsejLhl8kCymJpm3iXUmctkFqPAZdbT0Iu1BBWIrmvmh62d5h5IbsRgiBr97A'


def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    key_repeated = (key * (len(data) // len(key) + 1))[: len(data)]

    return bytes([d ^ k for d, k in zip(data, key_repeated)])


class SPN_DATA:
    def __init__(self, data: bytes) -> None:
        self.data = data
    def crypto(self):
        self.data = xor_encrypt_decrypt(self.data, default_key)


class SPN_SOCK:
    def __init__(self, host, port, timeout=None, reuse_addr=True, reuse_port=True):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 10)

    @contextmanager
    def manage_connection(self):
        try:
            yield self.sock
        finally:
            self.close()

    def serving(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def accept(self):
        conn, addr = self.sock.accept()
        return conn, addr[0]

    def compress_data(self, data):
        obj = pickle.dumps(data)
        return zlib.compress(obj)

    def decompress_data(self, data):
        obj = zlib.decompress(data)
        return pickle.loads(obj)

    def send_data(self, conn, data):
        compressed_data = self.compress_data(data)
        conn.sendall(b"DT:" + compressed_data + b":END")

    def receive_data(self, conn):
        compressed_data = b""
        while True:
            chunk = conn.recv(1024)
            compressed_data += chunk
            if b":END" in chunk or chunk == b"":
                break
        return self.decompress_data(compressed_data[3 : len(compressed_data) - 4])

    def close(self):
        self.sock.close()

    def connect(self):
        self.sock.connect((self.host, self.port))