import struct
import requests
from typing import Iterator, Tuple, Optional
from .constants import WEB3DL_STREAM_API_URL


class StreamClient:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def stream(
        self, 
        chain: str, 
        table: str, 
        from_block: Optional[int] = None,
        until_block: Optional[int] = None,
        chunk_size: int = 8192
    ) -> Iterator[Tuple[int, bytes]]:
        """
        Stream records from the server and yield records as {'block_number': ..., 'data': ...} dicts.
        Args:
            chain: Chain identifier
            table: Table identifier  
            from_block: Starting block number (optional)
            until_block: Ending block number (optional)
            chunk_size: Size of HTTP chunks to read at a time
        Yields:
            dict: {'block_number': int, 'data': bytes}
        Raises:
            requests.RequestException: If HTTP request fails
            ValueError: If received data is corrupted or incomplete
        """
        url = f"{WEB3DL_STREAM_API_URL}/{chain}/{table}"
        params = {"apikey": self.api_key}
        if from_block is not None:
            params["gte:block_number"] = str(from_block)
        if until_block is not None:
            params["lte:block_number"] = str(until_block)

        with requests.get(url, params=params, stream=True, timeout=5) as response:
            if response.status_code != 200:
                raise requests.HTTPError(response.status_code, response.json())
            yield from self._parse_stream(response.iter_content(chunk_size=chunk_size))

    def _parse_stream(self, chunks: Iterator[bytes]) -> Iterator[dict]:
        """
        Parse the binary stream into records of the form {'block_number': ..., 'data': ...}.
        The protocol format for each record is:
        - 4 bytes: block_number (big-endian unsigned int)
        - 4 bytes: data_length (big-endian unsigned int)  
        - N bytes: data (where N = data_length)
        Args:
            chunks: Iterator of raw HTTP chunks
        Yields:
            dict: {'block_number': int, 'data': bytes}
        """
        buffer = b''
        for chunk in chunks:
            if not chunk:  # Skip empty chunks
                continue
            buffer += chunk
            # Process complete records from buffer
            while len(buffer) >= 8:  # Need at least 8 bytes for header
                try:
                    # Extract block_number and data_length from header
                    block_number, data_length = struct.unpack(">II", buffer[:8])
                    # Check if we have the complete record
                    total_record_size = 8 + data_length
                    if len(buffer) < total_record_size:
                        break  # Wait for more data
                    # Extract the data
                    data = buffer[8:total_record_size]
                    # Yield the parsed record as a dict
                    yield {"block_number": block_number, "data": data}
                    # Remove processed record from buffer
                    buffer = buffer[total_record_size:]
                except struct.error as e:
                    raise ValueError(f"Failed to unpack record header: {e}")
        # Check for incomplete data at end of stream
        if buffer:
            raise ValueError(f"Stream ended with incomplete record: {len(buffer)} bytes remaining")
