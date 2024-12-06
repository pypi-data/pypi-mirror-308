"""Memory pool contains all Bitcoin transactions in "pending" state. For more details, see
BitcoinGraph white paper"""
from BitcoinPy.utils import block_util
from BitcoinPy.models.Transaction import Transaction


class Mempool:
    """Mempool class containing non-validated Bitcoin transactions"""

    def __init__(self, blockchain):
        self.version = block_util.uint8(blockchain)
        self.transaction_count = block_util.uint8(blockchain)
        self.transaction_list = []
        for _ in range(self.transaction_count):
            transaction = Transaction(blockchain)
            entry_time = block_util.uint8(blockchain)
            fee = block_util.uint8(blockchain)
            self.transaction_list.append({
                "transaction": transaction,
                "entry_time": entry_time,
                "fee": fee
            })

    def get_object_dict(self):
        return {
            "version": self.version,
            "object": "MEMPOOL",
            "transaction count": self.transaction_count,
            "transaction list": [tx.get_object_dict() for tx in self.transaction_list],
            "transaction id list": [tx.txid for tx in self.transaction_list]
        }
