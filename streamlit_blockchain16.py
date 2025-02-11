import streamlit as st
from tinydb import TinyDB, Query
from simple_blockchain8 import Blockchain, Block  # ✅ Import Block explicitly

# Initialize TinyDB databases
db = TinyDB("blockchain.json")
validators_db = TinyDB("validators.json")
users_db = TinyDB("users.json")

# Load blockchain state from TinyDB
def load_blockchain():
    blockchain = Blockchain()
    blocks = db.all()

    if blocks:
        blockchain.chain = []  # ✅ Clear default genesis block before loading from TinyDB
        for block in blocks:
            blockchain.chain.append(Block(
                index=block['index'],
                previous_hash=block['previous_hash'],
                timestamp=block['timestamp'],
                transactions=block['transactions'],
                validator=block['validator']
            ))

    return blockchain


# Save blockchain state to TinyDB
def save_blockchain(blockchain):
    db.truncate()  # Clear existing blocks
    for block in blockchain.chain:
        db.insert({
            "index": block.index,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "validator": block.validator,
            "hash": block.hash
        })

# Ensure blockchain persists across interactions
if "blockchain" not in st.session_state:
    st.session_state.blockchain = load_blockchain()

blockchain = st.session_state.blockchain  # Use stored instance

st.set_page_config(page_title="Blockchain Explorer", layout="wide")

st.title("🛠️ Simple Blockchain Explorer v.16-8")

# Display Blockchain Data
st.subheader("📜 Blockchain Ledger")
if db.all():
    for block in db.all():
        st.write(f"🔗 **Block {block['index']}**")
        st.json(block)
else:
    st.info("No blocks added yet!")

# Add Transaction
st.subheader("✉️ Add Transaction")
transaction_input = st.text_area("Enter transaction data:")
if st.button("Add Transaction"):
    if transaction_input:
        blockchain.create_transaction(transaction_input)
        st.success("Transaction added!")
        st.write("✅ Pending Transactions:", blockchain.pending_transactions)
    else:
        st.warning("Enter valid transaction data.")

# Stake Coins
st.subheader("💰 Stake Coins")
validator = st.text_input("Enter Validator Name:")
amount = st.number_input("Enter Amount to Stake:", min_value=1, step=1)
if st.button("Stake Coins"):
    if validator and amount > 0:
        blockchain.stake_coins(validator, amount)
        st.success(f"{amount} coins staked by {validator}!")
    else:
        st.warning("Enter valid stake details.")

# Mine Block
st.subheader("⛏️ Mine Block")
if st.button("Mine New Block"):
    st.write("🛠️ Transactions Before Mining:", blockchain.pending_transactions)  # Debug print

    if not blockchain.pending_transactions:
        st.warning("⚠️ No transactions to add to a new block! Add transactions first.")
    else:
        validator = blockchain.select_validator()

        if not validator:
            st.warning("⚠️ No validator available! Stake coins first.")
        else:
            # Ensure the block index is correct by checking the latest block in the database
            latest_block_in_db = db.all()[-1] if db.all() else None
            if latest_block_in_db and blockchain.get_latest_block().index != latest_block_in_db['index']:
                st.error("⚠️ Blockchain state is out of sync! Please refresh the page.")
            else:
                blockchain.add_block(validator)
                latest_block = blockchain.get_latest_block()

                st.write("✅ New Block Mined:", {
                    "index": latest_block.index,
                    "transactions": latest_block.transactions
                })

                # Save block to TinyDB
                db.insert({
                    "index": latest_block.index,
                    "previous_hash": latest_block.previous_hash,
                    "timestamp": latest_block.timestamp,
                    "transactions": latest_block.transactions,
                    "validator": latest_block.validator,
                    "hash": latest_block.hash,
                })

                blockchain.pending_transactions = []  # Clear transactions
                st.success(f"✅ Block {latest_block.index} mined successfully by {validator}!")

# Run Blockchain Validity Check
st.subheader("✅ Check Blockchain Validity")
if st.button("Validate Blockchain"):
    # Debugging: Print block hashes
    for i in range(1, len(blockchain.chain)):
        current_block = blockchain.chain[i]
        previous_block = blockchain.chain[i - 1]
        print(f"Checking Block {current_block.index}")
        print(f"Stored Hash: {current_block.hash}")
        print(f"Recalculated Hash: {current_block.calculate_hash()}")
        print(f"Previous Hash: {current_block.previous_hash}")
        print(f"Expected Previous Hash: {previous_block.hash}")

    if blockchain.is_chain_valid():
        st.success("✅ Blockchain is valid!")
    else:
        st.error("❌ Blockchain is NOT valid! Check logs for details.")

# Add Validator
st.subheader("👤 Add Validator")
new_validator = st.text_input("Enter New Validator Name:")
if st.button("Register Validator"):
    if new_validator:
        validators_db.insert({"name": new_validator})
        st.success(f"Validator {new_validator} registered successfully!")
    else:
        st.warning("Enter a valid validator name.")

# Add User
st.subheader("👥 Add User")
new_user = st.text_input("Enter New User Name:")
if st.button("Register User"):
    if new_user:
        users_db.insert({"name": new_user})
        st.success(f"User {new_user} registered successfully!")
    else:
        st.warning("Enter a valid user name.")
