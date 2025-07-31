import os


class CSVSaver:

    def __init__(self, data_path: str, batch_size: int = 1000):
        self.data_path = data_path
        self.batch_size = batch_size
        self.lines = []
        self._create()

    def _create(self):
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, "w") as f:
            f.write("block_number,data\n")

    def save(self, record):
        if len(self.lines) >= self.batch_size:
            self.flush()
        else:
            self.lines.append(f"{record['block_number']},{record['data']}\n")

    def flush(self):
        with open(self.data_path, "a") as f:
            f.writelines(self.lines)
        self.lines = []
