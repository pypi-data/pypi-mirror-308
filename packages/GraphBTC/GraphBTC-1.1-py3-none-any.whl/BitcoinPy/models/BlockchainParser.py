"""Parser file for scraping entirety of the Bitcoin blockchain. For more details, see
BitcoinGraph white paper"""
from joblib import Parallel, delayed
from BitcoinPy.models.Mempool import Mempool
from BitcoinPy.models.Block import Block


class BlockchainParser:
    """Parser class for Bitcoin blockchain"""

    def __init__(self, blockchain_dir, blk_file_start, blk_file_end,
                 include_mempool=False, num_workers=16):
        self.num_workers = num_workers
        self.blockchain_dir = blockchain_dir
        self.include_mempool = include_mempool
        self.blk_file_start = int(blk_file_start)
        self.blk_file_end = int(blk_file_end)

    def parse_mempool(self):
        mempool = None
        filename = f"{self.blockchain_dir}/mempool.dat"
        with open(filename, 'rb') as blockchain:
            mempool = Mempool(blockchain)
        return mempool

    def parse_blockchain(self):
        blockchain_contents = Parallel(self.num_workers, prefer='processes')(
            delayed(self.parse_blk_file)(i) for i in range(self.blk_file_start, self.blk_file_end+1)
        )

        if self.include_mempool:
            blockchain_contents.append(self.parse_mempool())

        print(
            f"Parsed {self.blk_file_end - self.blk_file_start} raw block files")
        return blockchain_contents

    def parse_blk_file(self, i):
        block_number = 0xFF

        file_number = "{:05}".format(i)
        filename = f"{self.blockchain_dir}/blk{file_number}.dat"
        blk_contents = []

        try:
            with open(filename, 'rb') as blockchain:
                print(
                    f"Parsing blockchain head at file {filename.split('/')[-1]}")
                continue_parsing = True
                counter = 0
                while continue_parsing:
                    block = Block(blockchain)
                    continue_parsing = block.continue_parsing
                    if continue_parsing:
                        blk_contents.append(block.get_object_dict())
                    counter += 1
                    if counter >= block_number and block_number != 0xFF:
                        continue_parsing = False
                if len(blk_contents) % 10000:
                    print(f"Parsed {len(blk_contents)} blocks")
        except Exception as e:
            print(f"Error at file {filename}: {e}")
        return blk_contents
