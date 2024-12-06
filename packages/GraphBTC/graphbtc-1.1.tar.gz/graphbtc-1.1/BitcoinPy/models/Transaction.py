"""Transactions contain inputs (spenders), outputs (receiver), and witnesses (similar to spenders).
For more details, see BitcoinGraph white paper"""
from BitcoinPy.utils import block_util
from BitcoinPy.models.TransactionInput import TransactionInput
from BitcoinPy.models.TransactionOutput import TransactionOutput
from BitcoinPy.models.TransactionWitness import TransactionWitness


class Transaction:
    """Transaction class for Bitcoin blockchain containing inputs, outputs, and witnesses"""

    def __init__(self, blockchain):
        self.version = block_util.uint4(blockchain)
        self.input_count = block_util.varint(blockchain)
        self.is_segwit = False
        if self.input_count == 0:
            self.is_segwit = True
            self.marker = 0
            self.flag = block_util.varint(blockchain)
            self.input_count = block_util.varint(blockchain)
        self.inputs, self.outputs, self.witnesses = [], [], []
        self.sequence = 1
        for _ in range(self.input_count):
            self.inputs.append(TransactionInput(blockchain))
        self.output_count = block_util.varint(blockchain)
        if self.output_count > 0:
            for _ in range(self.output_count):
                self.outputs.append(TransactionOutput(blockchain))
        if self.is_segwit:
            self.witnesses = []
            for _ in range(self.input_count):
                self.witnesses.append(TransactionWitness(blockchain))
        self.lock_time = block_util.uint4(blockchain)
        self.txid = block_util.raw_bytes_to_id(self.get_bytes_string())

    def get_bytes_string(self):
        return block_util.hash_string(block_util.encode_uint4(self.version)) \
            + block_util.compact_size(self.input_count) \
            + self.get_inputs_bytes_string() \
            + block_util.compact_size(self.output_count) \
            + self.get_outputs_bytes_string() \
            + block_util.hash_string(block_util.encode_uint4(self.lock_time))

    def get_inputs_bytes_string(self):
        return ''.join([input.get_bytes_string() for input in self.inputs])

    def get_outputs_bytes_string(self):
        return ''.join([output.get_bytes_string() for output in self.outputs])

    def get_witnesses_bytes_string(self):
        return ''.join([witness.get_bytes_string() for witness in self.witnesses])

    def get_object_dict(self):
        return {
            "txid": self.txid,
            "object": "TRANSACTION",
            "version": self.version,
            "sequence": self.sequence,
            "input count": self.input_count,
            "inputs": [tx.get_object_dict() for tx in self.inputs],
            "output count": self.output_count,
            "outputs": [tx.get_object_dict() for tx in self.outputs],
            "witnesses": [witness.get_object_dict() for witness in self.witnesses],
            "lock time": self.lock_time
        }
