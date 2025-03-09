import hashlib
import time
import json
from flask import Flask, jsonify, request

class Block:
    """
    Represents a block in the blockchain.
    """
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index  # Block index in the chain
        self.previous_hash = previous_hash  # Hash of the previous block
        self.timestamp = timestamp or time.time()  # Timestamp of block creation
        self.transactions = transactions  # Transactions stored in this block
        self.nonce = 0  # Used for mining (Proof-of-Work)
        self.hash = self.calculate_hash()  # Hash of the current block

    def calculate_hash(self):
        """
        Calculates the SHA-256 hash of the block content.
        """
        block_content = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        Implements Proof-of-Work by finding a hash with leading zeros.
        """
        target = "0" * difficulty  # Required prefix for valid hash
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} successfully mined! Hash: {self.hash}")

class Blockchain:
    """
    Represents the blockchain, managing blocks and transactions.
    """
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty  # Difficulty level for mining
        self.pending_transactions = []  # Transactions waiting to be added to a block

    def create_genesis_block(self):
        """
        Creates the first block in the blockchain.
        """
        return Block(0, "0", "Genesis Block")

    def get_latest_block(self):
        """
        Returns the most recently added block in the chain.
        """
        return self.chain[-1]

    def add_block(self, transactions):
        """
        Adds a new block to the blockchain with given transactions.
        """
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def add_transaction(self, transaction):
        """
        Adds a new transaction to the pending transaction list.
        """
        self.pending_transactions.append(transaction)

    def chain_valid(self):
        """
        Validates the integrity of the blockchain.
        """
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block.previous_hash != previous_block.hash:
                return False

            previous_block = block
            block_index += 1

        return True

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    """
    Mines a new block containing pending transactions.
    """
    previous_block = blockchain.get_latest_block()
    transactions = blockchain.pending_transactions if blockchain.pending_transactions else "No transactions"
    blockchain.add_block(transactions)
    blockchain.pending_transactions = []  # Clear transactions after mining
    return jsonify({"message": "New block mined", "block": blockchain.get_latest_block().__dict__}), 200

@app.route('/get_chain', methods=['GET'])
def display_chain():
    """
    Returns the current state of the blockchain.
    """
    response = {"chain": [block.__dict__ for block in blockchain.chain], "length": len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    """
    Checks if the blockchain is valid.
    """
    return jsonify({"message": "Blockchain is valid" if blockchain.chain_valid() else "Blockchain is not valid"}), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """
    Adds a transaction to the blockchain.
    """
    data = request.get_json()
    if not data or "transaction" not in data:
        return jsonify({"message": "Invalid transaction data"}), 400
    blockchain.add_transaction(data["transaction"])
    return jsonify({"message": "Transaction added", "transaction": data["transaction"]}), 201

if __name__ == "__main__":
    app.run()
