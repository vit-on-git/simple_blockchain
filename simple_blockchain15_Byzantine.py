import hashlib
import time
import random

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, validator):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.validator}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.validators = ["Alice", "Bob", "Charlie"]  # List of validators
        self.primary = self.validators[0]  # Primary validator
        self.f = 1  # Maximum number of faulty nodes (for 3 validators, f=1)

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "System")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, validator):
        new_block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions, validator)
        self.chain.append(new_block)
        self.pending_transactions = []

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

    def pbft_consensus(self):
        # Phase 1: Pre-Prepare (Primary proposes a block)
        print(f"Primary {self.primary} is proposing a new block...")
        proposed_block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions, self.primary)

        # Phase 2: Prepare (Validators vote on the proposed block)
        print("Validators are preparing to vote on the proposed block...")
        prepare_votes = []
        for validator in self.validators:
            if validator != self.primary:
                # Simulate voting (in a real system, validators would sign their votes)
                if random.random() < 0.9:  # 90% chance of voting yes (simulating honest nodes)
                    prepare_votes.append(validator)
                    print(f"Validator {validator} voted YES on the proposed block.")
                else:
                    print(f"Validator {validator} voted NO on the proposed block.")

        # Check if enough validators agreed (2f + 1)
        if len(prepare_votes) >= 2 * self.f:
            # Phase 3: Commit (Validators commit the block)
            print("Enough validators agreed. Committing the block...")
            commit_votes = []
            for validator in self.validators:
                if validator != self.primary:
                    if random.random() < 0.9:  # 90% chance of committing (simulating honest nodes)
                        commit_votes.append(validator)
                        print(f"Validator {validator} committed the block.")
                    else:
                        print(f"Validator {validator} did not commit the block.")

            # Check if enough validators committed (2f + 1)
            if len(commit_votes) >= 2 * self.f:
                # Add the block to the blockchain
                self.add_block(self.primary)
                print(f"Block added by primary validator: {self.primary}")
            else:
                print("Not enough validators committed the block. Block not added.")
        else:
            print("Not enough validators agreed on the block. Block not added.")

# Example usage for a decentralized social media platform
if __name__ == "__main__":
    my_blockchain = Blockchain()

    print("Creating social media posts...")
    my_blockchain.create_transaction("User1: 'Decentralized networks empower freedom!'")
    my_blockchain.create_transaction("User2: 'Censorship-resistant social media is the future.'")

    print("Validating and adding posts to blockchain using PBFT...")
    my_blockchain.pbft_consensus()

    print("Creating more posts...")
    my_blockchain.create_transaction("User3: 'Blockchain ensures content integrity!'")
    my_blockchain.create_transaction("User4: 'Social media should be open-source and trustless.'")

    print("Validating and adding posts to blockchain using PBFT...")
    my_blockchain.pbft_consensus()

    print("\nBlockchain valid?", my_blockchain.is_chain_valid())
    
    print("\nSocial Media Blockchain Feed:")
    for block in my_blockchain.chain:
        print(f"Post ID: {block.index}, Content: {block.transactions}, Validator: {block.validator}")