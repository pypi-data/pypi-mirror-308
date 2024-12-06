"""Transaction outputs are receivers of Bitcoin transactions. For more details, see
BitcoinGraph white paper"""
from BitcoinPy.utils import block_util


class TransactionOutput:
    """Output section of Bitcoin transactions"""

    def __init__(self, blockchain):
        self.amount = block_util.uint8(blockchain)
        self.script_length = block_util.varint(blockchain)
        self.pubkey_script = blockchain.read(self.script_length)
        self.pubkey_script_deciphered = block_util.decipher_script(
            self.pubkey_script)
        self.decode_script()

    def get_bytes_string(self):
        return block_util.hash_string(block_util.encode_uint8(self.amount)) + \
            block_util.compact_size(self.script_length) + \
            block_util.hash_string(self.pubkey_script)

    def get_object_dict(self):
        return {
            "amount": self.amount,
            "script length": self.script_length,
            "script pubkey": block_util.hash_string(self.pubkey_script),
            "script pubkey deciphered": self.pubkey_script_deciphered,
            "pubkey": self.pubkey,
            "script type": self.script_type,
            "address": self.address
        }

    def decode_script(self):
        try:
            if block_util.is_p2pk(self.pubkey_script_deciphered):
                self.pubkey = self.pubkey_script_deciphered[1]
                self.address = block_util.pubkey_to_address(self.pubkey)
                self.script_type = "P2PK"
            elif block_util.is_p2pkh(self.pubkey_script_deciphered):
                self.pubkey = self.pubkey_script_deciphered[3]
                self.address = block_util.hash_to_address(f"00{self.pubkey}")
                self.script_type = "P2PKH"
            elif block_util.is_p2ms(self.pubkey_script_deciphered):
                self.pubkey = None
                self.address = None
                self.script_type = "MULTISIG"
            elif block_util.is_p2sh(self.pubkey_script_deciphered):
                self.pubkey = self.pubkey_script_deciphered[2]
                self.address = block_util.hash_to_address(f"05{self.pubkey}")
                self.script_type = "P2SH"
            elif block_util.is_op_return(self.pubkey_script_deciphered):
                self.pubkey = self.pubkey_script_deciphered[2]
                self.address = None
                self.script_type = "OP_RETURN"
            elif block_util.is_p2wpkh(self.pubkey_script_deciphered):
                self.pubkey = self.pubkey_script_deciphered[2]
                self.address = block_util.segwit_hash_to_address(
                    f"0014{self.pubkey}")
                self.script_type = "P2WPKH"
            elif block_util.is_p2wsh(self.pubkey_script_deciphered):
                self.pubkey = self.pubkey_script_deciphered[2]
                self.address = block_util.segwit_hash_to_address(
                    f"0020{self.pubkey}")
                self.script_type = "P2WSH"
            else:
                self.pubkey = None
                self.address = None
                self.script_type = "NONSTANDARD"

        except Exception:
            self.pubkey = None
            self.address = None
            self.script_type = "NONSTANDARD"
