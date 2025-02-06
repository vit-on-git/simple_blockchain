import streamlit as st
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

# Initialize blockchain
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("Decentralized Social Media Blockchain")

# Sidebar for staking coins
st.sidebar.header("Stake Coins")
validator_name = st.sidebar.text_input("Validator Name")
stake_amount = st.sidebar.number_input("Stake Amount", min_value=1, value=10)
if st.sidebar.button("Stake"):
    st.session_state.blockchain.stake_coins(validator_name, stake_amount)
    st.sidebar.success(f"{stake_amount} coins staked by {validator_name}")

# Main area for creating posts and viewing blockchain
st.header("Create a New Post")
post_content = st.text_area("Post Content")
if st.button("Submit Post"):
    st.session_state.blockchain.create_transaction(post_content)
    st.success("Post added to pending transactions!")

if st.button("Validate and Add Block"):
    st.session_state.blockchain.validate_and_add_block()
    st.success("Block validated and added to the blockchain!")

st.header("Blockchain Feed")
for block in st.session_state.blockchain.chain:
    st.subheader(f"Post ID: {block.index}")
    st.write(f"Content: {block.transactions}")
    st.write(f"Validator: {block.validator}")
    st.write(f"Timestamp: {time.ctime(block.timestamp)}")
    st.write(f"Block Hash: {block.hash}")
    st.write("---")

st.header("Blockchain Validity")
if st.button("Check Blockchain Validity"):
    if st.session_state.blockchain.is_chain_valid():
        st.success("The blockchain is valid!")
    else:
        st.error("The blockchain is invalid!")