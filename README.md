# Message Exchanger

## Description

A simple server and client for exchanging text messages via HTTP. The server supports storing messages in queues, and the client can send and retrieve messages from these queues.

## Requirements

- Python 3.x
- Python libraries: `requests` and `pytest`

## Installation

1. Clone the repository or download and unzip the ZIP archive.
2. Open the terminal and navigate to the project directory.
3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    or if `requirements.txt` is not available:

    ```bash
    pip install requests pytest
    ```

## Usage

### Running the Server

Open the terminal and execute:

```bash
python server.py
```
### Running the Client

Open another terminal and execute one of the following commands:

- To send a message:

    ```bash
    python client.py --post "Your message"
    ```

- To retrieve a message:

    ```bash
    python client.py --get
    ```

### Testing

To run the tests, execute:

```bash
pytest test_suite.py
```
### Additional Information

- You can specify a queue alias when sending or retrieving a message by adding the `--queue` flag:

    ```bash
    python client.py --post "Your message" --queue 1
    ```

    ```bash
    python client.py --get --queue 1
    ```

- The server uses port 8000 by default. You can change it by adding the `--port` argument when running `server.py`.

### Author

Oleksandr Sotnichenko
