from core.constants import DATA_DIR, WEB3DL_API_KEY
from core.progress import ProgressTracker
from core.saver import CSVSaver
from core.client import StreamClient


def main():
    saver = CSVSaver(f"{DATA_DIR}/dump.csv")
    progress = ProgressTracker(update_interval=25)
    client = StreamClient(api_key=WEB3DL_API_KEY)

    for record in client.stream(
        chain="eth",
        table="blocks",
        from_block=0,
        until_block=100_000,
    ):
        saver.save(record)
        progress.update(record)

    saver.flush()


if __name__ == "__main__":
    main()
