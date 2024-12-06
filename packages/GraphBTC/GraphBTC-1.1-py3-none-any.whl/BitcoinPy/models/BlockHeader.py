"""Block header file containing metadata describing each block in the blockchain. For more
details, see BitcoinGraph white paper"""
from datetime import datetime
from BitcoinPy.utils import block_util


class BlockHeader:
    """Block header class containing block metadata"""

    def __init__(self, blockchain):
        self.version = block_util.uint4(blockchain)
        self.previous_hash = block_util.hash32(blockchain)
        self.merkle_hash = block_util.hash32(blockchain)
        self.time = block_util.uint4(blockchain)
        self.bits = block_util.uint4(blockchain)
        self.nonce = block_util.uint4(blockchain)

    def get_object_dict(self):
        return {
            "version": self.version,
            "previous hash": block_util.hash_string(self.previous_hash),
            "merkle root": block_util.hash_string(self.merkle_hash),
            "timestamp": self.decode_time(self.time),
            "difficulty": self.bits,
            "nonce": self.nonce
        }

    def decode_time(self, time):
        utc_time = datetime.fromtimestamp(time)
        return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")

    def get_bytes_string(self):
        return block_util.hash_string(block_util.encode_uint4(self.version)) \
            + block_util.hash_string(self.previous_hash[::-1]) \
            + block_util.hash_string(self.merkle_hash[::-1]) \
            + block_util.hash_string(block_util.encode_uint4(self.time)) \
            + block_util.hash_string(block_util.encode_uint4(self.bits)) \
            + block_util.hash_string(block_util.encode_uint4(self.nonce))
