"""Witnesses are more secure unlocking mechanisms for Bitcoin transactions. For more details,
see BitcoinGraph white paper"""
from BitcoinPy.utils import block_util


class TransactionWitness:
    """Witness section of Bitcoin transactions"""

    def __init__(self, blockchain):
        self.stack_count = block_util.varint(blockchain)
        self.script_lengths, self.items, self.items_deciphered = [], [], []
        for _ in range(self.stack_count):
            script_length = block_util.varint(blockchain)
            stack_data = blockchain.read(script_length)
            self.script_lengths.append(script_length)
            self.items.append(block_util.hash_string(stack_data))
            self.items_deciphered.append(
                block_util.decipher_script(stack_data))

    def get_object_dict(self):
        return {
            "stack_count": self.stack_count,
            "script_lengths": self.script_lengths,
            "stack_items": self.items,
            "stack_items_deciphered": self.items_deciphered

        }

    def get_bytes_string(self):
        bytes_string = block_util.compact_size(self.stack_count)
        for i in range(self.stack_count):
            bytes_string += block_util.compact_size(self.script_lengths[i])
            bytes_string += block_util.hash_string(self.items[i])
        return bytes_string
