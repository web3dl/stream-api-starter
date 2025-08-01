# stream-api-starter

A minimal example demonstrating how to use **[Stream API](https://github.com/web3dl#stream-api)** to download data.

To run the example, execute `main.py` after completing the [installation](#installation) steps. By default, it downloads Ethereum blocks between `0 - 100,000`. You can easily modify the code to download data from a different chain or table over any block range.

The Stream API is the fastest way to download data from Web3DL.

## Repo Structure

```
├── core/
│   ├── client.py      # `StreamClient` implementation
│   ├── constants.py   # Repo constants
│   ├── progress.py    # Progress tracking class
│   └── saver.py       # CSV saver class
├── main.py            # Entry point
└── requirements.txt   # Python dependencies
```

## Usage

Run the main script to start downloading data:

```bash
python main.py
```

The script will:

- Use the [StreamClient](#streamclient) convenience class to stream data from the Stream API.
- Download Ethereum blocks between block 0 and 100,000.
- Save data to `./data/dump.csv`.
- Display download progress.

Before running `main.py`, make sure to follow all the steps in the [Installation](#installtion) section first.

### Downloading other data

Modify `main.py` to adjust parameters:

```python
client.stream(
    chain="eth",           # Chain identifier
    table="blocks",        # Data type
    from_block=1000000,    # Starting block (optional)
    until_block=2000000,   # Ending block (optional)
)
```

## Installation

### Prerequisites

- **Python 3.X** (Any Python 3 version will work)
- Web3DL API key (Get one here: https://t.me/web3datalake_auth_bot)

### Setup

1. **Install Python** (if not already installed):
   - Verify installation: `python --version`

2. **Clone the repository**:
   ```bash
   git clone https://github.com/web3dl/stream-api-starter.git
   cd stream-api-starter
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - **Linux/macOS**: `source venv/bin/activate`
   - **Windows**: `venv\Scripts\activate`

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   WEB3DL_API_KEY=your_api_key_here
   ```

## StreamClient

The `StreamClient` class is a convenience wrapper around the Web3DL **Stream API** that handles:

- **Connection Management**: Establishes and maintains HTTP streaming connections
- **Binary Protocol Parsing**: Decodes the Web3DL binary format automatically

### Protocol Details

The Web3DL Stream API uses a binary protocol where each record contains:

- 4 bytes: `block_number` (big-endian unsigned int)
- 4 bytes: `data_length` (big-endian unsigned int)  
- N bytes: `data` (where N = data_length)

The `StreamClient` parses this format and yields records as dictionaries:
```python
{
    "block_number": 12345,
    "data": b"..."  # Raw block data
}
```

### Usage Example

```python
from core.client import StreamClient

client = StreamClient(api_key="your_api_key")

for record in client.stream("eth", "blocks", from_block=100, until_block=200):
    block_num = record["block_number"]
    block_data = record["data"]
    # Process the block data...
```
