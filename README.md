# stream-api-starter

A minimal example demonstrating how to use **[Stream API](https://github.com/web3dl#stream-api)** to download data.

To run the example, execute `main.py` after completing the [installation](#installation) steps. By default, it downloads Ethereum blocks from block 0 to 100,000. You can easily modify the code to download data from a different chain or table.

`main.py` will:

- Use the [StreamClient](#stream-client) convenience class to stream data from the Stream API.
- Downlaod Ethereum blocks between block 0 and 100,000.
- Save data to: `./data/dump.csv`.
- Report download progress.

The Stream API is the fastest way to download data from the data lake.

## Project Structure

```
├── core/
│   ├── client.py      # `StreamClient` implementation
│   ├── constants.py   # Configuration and environment variables
│   ├── progress.py    # Progress tracking utilities
│   └── saver.py       # CSV data persistence
├── main.py            # Example usage script
└── requirements.txt   # Python dependencies
```

## Usage

Run the main script to start downloading Ethereum block data:

```bash
python main.py
```

The script will:

- Stream blocks 0 to 100,000 from Ethereum mainnet
- Save data to `./data/dump.csv`
- Display progress updates every 25 blocks

Before running main.py, make sure to follow all the steps in the **Installation** section to set up the required dependencies and environment.

### Customizing the Stream

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

- **Python 3.X** (any Python 3 version will work)
- Web3DL API key

### Setup

1. **Install Python** (if not already installed):
   - Download from [python.org](https://python.org)
   - Verify installation: `python --version`

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ethereum-block-streaming
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
