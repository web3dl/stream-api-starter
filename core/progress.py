import time


class ProgressTracker:

    def __init__(self, update_interval: int = 1000):
        self.update_interval = update_interval
        self.start_time = time.time()
        self.num_blocks = 0
        self.num_bytes = 0

    def update(self, record):
        block_number, data = record["block_number"], record["data"]
        self.num_blocks += 1
        self.num_bytes += len(data)
        if self.num_blocks % self.update_interval == 0:
            total_took = time.time() - self.start_time
            blocks_per_second = self.num_blocks / total_took
            mb_per_second = self.num_bytes / total_took / 1024 / 1024
            print(
                f"[{total_took:.2f}s] "
                f"[Block-{block_number}] "
                f"Blocks/s: {blocks_per_second:.2f} "
                f"MB/s: {mb_per_second:.2f}"
            )
