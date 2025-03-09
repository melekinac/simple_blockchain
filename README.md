# Simple Blockchain Implementation

This is a basic blockchain implementation using Python and Flask. The blockchain supports adding transactions, mining new blocks, and retrieving the chain state.

## Features

- Proof-of-Work mining mechanism
- SHA-256 hashing for blocks
- Simple blockchain validation
- Transaction handling

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/melekinac/simple_blockchain.git
   cd simple_blockchain
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install flask
   ```

4. Run the blockchain program:

   ```sh
   python main.py
   ```

## Code Structure

### `Block` Class

The `Block` class represents a single block in the blockchain.

- **Attributes:**
  - `index`: Position of the block in the chain.
  - `previous_hash`: Hash of the previous block, ensuring continuity.
  - `timestamp`: Time when the block was created.
  - `transactions`: Transactions stored in the block.
  - `nonce`: Number used for mining (Proof-of-Work).
  - `hash`: Hash of the current block.
- **Methods:**
  - `calculate_hash()`: Computes the SHA-256 hash of the block.
  - `mine_block(difficulty)`: Performs Proof-of-Work mining to find a valid hash.

### `Blockchain` Class

The `Blockchain` class manages the chain and transactions.

- **Attributes:**
  - `chain`: A list of `Block` objects.
  - `difficulty`: Defines the complexity of mining.
  - `pending_transactions`: List of transactions waiting to be included in a block.
- **Methods:**
  - `create_genesis_block()`: Creates the first block in the blockchain.
  - `get_latest_block()`: Returns the most recent block.
  - `add_block(transactions)`: Mines a new block with the given transactions and appends it to the chain.
  - `add_transaction(transaction)`: Adds a new transaction to the pending transactions list.
  - `chain_valid()`: Validates the integrity of the blockchain.

### Flask Endpoints

The blockchain is exposed via a Flask web application.

### 1. Add a Transaction

**Route:** `POST /add_transaction`

- Adds a new transaction to the pending transaction list.
- **Request Body:**
  ```json
  {
    "transaction": "Melek -> Alice: 10 BTC"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Transaction added",
    "transaction": "Angel -> Tom: 10 BTC"
  }
  ```

### 2. Mine a New Block

**Route:** `GET /mine_block`

- Mines a new block using Proof-of-Work and adds pending transactions.
- **Response:**
  ```json
  {
    "message": "New block mined",
    "block": {
      "index": 2,
      "previous_hash": "abc123...",
      "transactions": ["Melek -> Alice: 10 BTC"],
      "hash": "0000abcd...",
      "nonce": 2345
    }
  }
  ```

### 3. Get Blockchain State

**Route:** `GET /get_chain`

- Retrieves the current blockchain state.
- **Response:**
  ```json
  {
    "chain": [...],
    "length": 2
  }
  ```

### 4. Validate Blockchain

**Route:** `GET /valid`

- Checks if the blockchain is valid.
- **Response:**
  ```json
  {
    "message": "Blockchain is valid"
  }
  ```
