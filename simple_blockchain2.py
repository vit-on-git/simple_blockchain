import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print("Current block hash is invalid!")
                return False

            if current_block.previous_hash != previous_block.hash:
                print("Previous block hash is invalid!")
                return False

        return True

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        new_block = Block(len(self.chain), "", time.time(), self.pending_transactions)
        self.add_block(new_block)
        self.pending_transactions = []

# Example usage
if __name__ == "__main__":
    my_blockchain = Blockchain()

    print("Creating transactions...")
    my_blockchain.create_transaction("Transaction 1")
    my_blockchain.create_transaction("Transaction 2")

    print("Mining block 1...")
    my_blockchain.mine_pending_transactions()

    print("Creating more transactions...")
    my_blockchain.create_transaction("Transaction 3")
    my_blockchain.create_transaction("Transaction 4")

    print("Mining block 2...")
    my_blockchain.mine_pending_transactions()

    print("\nBlockchain valid?", my_blockchain.is_chain_valid())

    print("\nBlockchain:")
    for block in my_blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Transactions: {block.transactions}")