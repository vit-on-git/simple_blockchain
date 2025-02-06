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
        self.stakes = {}  # Stores stake amounts for each validator
        self.slash_records = {}  # Records validators who misbehave

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

    def stake_coins(self, validator, amount):
        if validator in self.stakes:
            self.stakes[validator] += amount
        else:
            self.stakes[validator] = amount

    def select_validator(self):
        total_stake = sum(self.stakes.values())
        if total_stake == 0:
            print("No stakes available for validation!")
            return None
        
        selection = random.choices(list(self.stakes.keys()), weights=self.stakes.values())[0]
        return selection

    def slash_validator(self, validator):
        if validator in self.stakes:
            slashed_amount = self.stakes[validator] * 0.2  # Slash 20% of the stake
            self.stakes[validator] -= slashed_amount
            self.slash_records[validator] = self.slash_records.get(validator, 0) + 1
            print(f"Validator {validator} slashed by {slashed_amount} coins! Misbehavior count: {self.slash_records[validator]}")
            if self.stakes[validator] <= 0:
                del self.stakes[validator]  # Remove validator if stake reaches zero

    def validate_and_add_block(self):
        validator = self.select_validator()
        if validator:
            if random.random() < 0.1:  # Simulate a misbehavior chance
                print(f"Validator {validator} misbehaved!")
                self.slash_validator(validator)
            else:
                self.add_block(validator)
                print(f"Block added by validator: {validator}")

# Example usage for a decentralized social media platform
if __name__ == "__main__":
    my_blockchain = Blockchain()
    my_blockchain.stake_coins("Alice", 50)  # High-stake validator
    my_blockchain.stake_coins("Bob", 30)    # Medium-stake validator
    my_blockchain.stake_coins("Charlie", 20) # New validator

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
        print(f"Post ID: {block.index}, Content: {block.transactions}, Validator: {block.validator}")
