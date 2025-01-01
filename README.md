
# CommServer

CommServer is a Python-based TCP client-server model designed for robust two-way communication, efficient multithreading for handling multiple clients, and seamless file repository access.

## Features

- **Multithreaded Server**: Supports concurrent connections for up to three clients simultaneously.
- **Two-Way Communication**: Reliable message exchange between clients and the server.
- **File Repository Access**:
  - `list`: View all available files in the server's repository.
  - `get [filename]`: Download specific files from the server.
- **Client Commands**:
  - `status`: Retrieve server-assigned client details.
  - `exit`: Safely terminate the connection and free server resources.
- **Reliable Data Transfer**: Uses headers to manage file sizes and ensure data integrity.
- **Error Handling**: Includes mechanisms to handle connection limits and invalid commands.

## Requirements

- Python 3.x
- Standard Python libraries: `socket`, `threading`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/CommServer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd CommServer
   ```

3. Ensure Python 3.x is installed on your system.

## Usage

### Starting the Server
1. Run the server script:
   ```bash
   python server.py
   ```
2. The server will start listening for client connections on the specified port.

### Connecting a Client
1. Run the client script:
   ```bash
   python client.py
   ```
2. Use the following commands to interact with the server:
   - `status`: Retrieve connection details.
   - `list`: View available files.
   - `get [filename]`: Download a file from the server.
   - `exit`: Disconnect from the server.

## Testing

### Functional Tests
- Verified server handles up to three simultaneous clients.
- Confirmed proper responses for commands such as `status`, `list`, and `exit`.
- Ensured reliable file transfers, even with large files.

### Stress Tests
- Attempted to connect more than three clients and observed appropriate error handling.
- Tested invalid commands and verified server stability.

## Future Improvements

- **Enhanced GUI**: Develop a user-friendly interface for the client.
- **Encryption**: Implement secure data transfer protocols.
- **Advanced Error Handling**: Address unhandled edge cases and improve resilience.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This project was developed as part of the CP372 Computer Networks course at Wilfrid Laurier University. 
