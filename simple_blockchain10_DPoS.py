import hashlib
import time
import random

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, delegate):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.delegate = delegate
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.delegate}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.stakes = {}  # Stores stake amounts for each stakeholder
        self.delegates = []  # List of elected delegates
        self.votes = {}  # Votes received by each delegate candidate

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "System")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, delegate):
        new_block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions, delegate)
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

    def stake_coins(self, stakeholder, amount):
        if stakeholder in self.stakes:
            self.stakes[stakeholder] += amount
        else:
            self.stakes[stakeholder] = amount

    def vote_for_delegate(self, voter, delegate):
        if voter in self.stakes:
            if delegate in self.votes:
                self.votes[delegate] += self.stakes[voter]
            else:
                self.votes[delegate] = self.stakes[voter]
            print(f"{voter} voted for {delegate} with {self.stakes[voter]} staked coins.")
        else:
            print(f"{voter} has no staked coins to vote.")

    def elect_delegates(self):
        # Sort candidates by votes in descending order
        sorted_candidates = sorted(self.votes.items(), key=lambda x: x[1], reverse=True)
        # Select top 3 candidates as delegates
        self.delegates = [candidate[0] for candidate in sorted_candidates[:3]]
        print(f"Elected delegates: {self.delegates}")

    def select_delegate(self):
        if not self.delegates:
            print("No delegates elected!")
            return None
        # Rotate through the delegates for block production
        selected_delegate = self.delegates.pop(0)
        self.delegates.append(selected_delegate)
        return selected_delegate

    def validate_and_add_block(self):
        delegate = self.select_delegate()
        if delegate:
            self.add_block(delegate)
            print(f"Block added by delegate: {delegate}")

# Example usage for a decentralized social media platform
if __name__ == "__main__":
    my_blockchain = Blockchain()
    my_blockchain.stake_coins("Alice", 50)  # High-stake stakeholder
    my_blockchain.stake_coins("Bob", 30)    # Medium-stake stakeholder
    my_blockchain.stake_coins("Charlie", 20) # New stakeholder

    # Stakeholders vote for delegates
    my_blockchain.vote_for_delegate("Alice", "Alice")
    my_blockchain.vote_for_delegate("Bob", "Bob")
    my_blockchain.vote_for_delegate("Charlie", "Charlie")

    # Elect delegates based on votes
    my_blockchain.elect_delegates()

    print("Creating social media posts...")
    my_blockchain.create_transaction("User1: 'Decentralized networks empower freedom!'")
    my_blockchain.create_transaction("User2: 'Censorship-resistant social media is the future.'")

    print("Validating and adding posts to blockchain...")
    my_blockchain.validate_and_add_block()

    print("Creating more posts...")
    my_blockchain.create_transaction("User3: 'Blockchain ensures content integrity!'")
    my_blockchain.create_transaction("User4: 'Social media should be open-source and trustless.'")

    print("Validating and adding posts to blockchain...")
    my_blockchain.validate_and_add_block()

    print("\nBlockchain valid?", my_blockchain.is_chain_valid())
    
    print("\nSocial Media Blockchain Feed:")
    for block in my_blockchain.chain:
        print(f"Post ID: {block.index}, Content: {block.transactions}, Delegate: {block.delegate}")