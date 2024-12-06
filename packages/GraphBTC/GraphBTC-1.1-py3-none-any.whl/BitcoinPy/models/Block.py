"""Block object encapsulating all block and transaction data stored on the blockchain. For more
details, see BitcoinGraph white paper"""
from BitcoinPy.utils import block_util
from BitcoinPy.models.Transaction import Transaction
from BitcoinPy.models.BlockHeader import BlockHeader


class Block:
    """Block object encapsulating block and transaction data"""

    def __init__(self, blockchain):
        self.continue_parsing = True
        self.magic_number = 0
        self.block_size = 0
        self.block_header = ""
        self.tx_count = 0
        self.tx_list = []

        if self.has_length(blockchain, 8):
            self.magic_number = block_util.uint4(blockchain)
            self.block_size = block_util.uint4(blockchain)
        else:
            self.continue_parsing = False
            return

        if self.has_length(blockchain, self.block_size):
            self.set_header(blockchain)
            self.tx_count = block_util.varint(blockchain)
            self.tx_list = []

            for i in range(self.tx_count):
                tx = Transaction(blockchain)
                tx.sequence = i
                self.tx_list.append(tx)
        else:
            self.continue_parsing = False
        self.block_hash = block_util.raw_bytes_to_id(
            self.block_header.get_bytes_string())

    def get_block_size(self):
        return self.block_size

    def has_length(self, blockchain, size):
        current_position = blockchain.tell()
        blockchain.seek(0, 2)

        file_size = blockchain.tell()
        blockchain.seek(current_position)

        temp_block_size = file_size - current_position
        if temp_block_size < size:
            return False
        return True

    def set_header(self, blockchain):
        self.block_header = BlockHeader(blockchain)

    def get_object_dict(self):
        return {
            "_id": self.block_hash,
            "object": "BLOCK",
            "magic number": self.magic_number,
            "block size": self.block_size,
            "version": self.block_header.version,
            "previous hash": block_util.hash_string(self.block_header.previous_hash),
            "merkle root": block_util.hash_string(self.block_header.merkle_hash),
            "timestamp": self.block_header.decode_time(self.block_header.time),
            "difficulty": self.block_header.bits,
            "nonce": self.block_header.nonce,
            "transaction count": self.tx_count,
            "transaction list": [tx.get_object_dict() for tx in self.tx_list],
            "transaction id list": [tx.txid for tx in self.tx_list]
        }
