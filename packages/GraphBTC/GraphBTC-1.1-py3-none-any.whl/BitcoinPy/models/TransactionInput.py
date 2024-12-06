"""Transaction inputs are spenders of Bitcoin transactions. For more details, see
BitcoinGraph white paper"""
from BitcoinPy.utils import block_util


class TransactionInput:
    """Input section of Bitcoin transactions"""

    def __init__(self, blockchain):
        self.prev_hash = block_util.hash32(blockchain)
        self.tx_out_id = block_util.uint4(blockchain)
        self.script_length = block_util.varint(blockchain)
        self.script_sig = blockchain.read(self.script_length)
        self.seq_no = block_util.uint4(blockchain)
        self.script_sig_deciphered = block_util.decipher_script(
            self.script_sig)

    def get_bytes_string(self):
        return block_util.str_to_little_endian(self.prev_hash) + \
            block_util.hash_string(block_util.encode_uint4(self.tx_out_id)) + \
            block_util.compact_size(self.script_length) + \
            block_util.hash_string(
                self.script_sig) + block_util.hash_string(block_util.encode_uint4(self.seq_no))

    def get_object_dict(self):
        return {
            "prev hash": block_util.hash_string(self.prev_hash),
            "tx out index": block_util.hash_string(block_util.encode_uint4(self.tx_out_id)),
            "script length": self.script_length,
            "script signature": block_util.hash_string(self.script_sig),
            "script signature deciphered": self.script_sig_deciphered,
            "sequence": self.seq_no
        }
