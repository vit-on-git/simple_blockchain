import streamlit as st
from tinydb import TinyDB
from simple_blockchain5 import Blockchain

# ✅ Move this to the first line
st.set_page_config(page_title="Blockchain Explorer", layout="wide")

# Initialize Blockchain and TinyDB
blockchain = Blockchain()
db = TinyDB("blockchain.json")

# Streamlit UI
st.title("🛠️ Simple Blockchain Explorer")

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
    else:
        st.warning("Enter valid transaction data.")

# Mine Block
st.subheader("⛏️ Mine Block")
if st.button("Mine New Block"):
    blockchain.validate_and_add_block()
    latest_block = blockchain.get_latest_block()

    db.insert({
        "index": latest_block.index,
        "previous_hash": latest_block.previous_hash,
        "timestamp": latest_block.timestamp,
        "transactions": latest_block.transactions,
        "validator": latest_block.validator,
        "hash": latest_block.hash,
    })
    st.success(f"Block {latest_block.index} mined successfully!")

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

# Run Blockchain Validity Check
st.subheader("✅ Check Blockchain Validity")
if st.button("Validate Blockchain"):
    if blockchain.is_chain_valid():
        st.success("✅ Blockchain is valid!")
    else:
        st.error("❌ Blockchain is NOT valid!")
