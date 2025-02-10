import streamlit as st
from tinydb import TinyDB
from simple_blockchain6 import Blockchain

# ✅ Move this to the first line
st.set_page_config(page_title="Blockchain Explorer", layout="wide")

# Initialize Blockchain and TinyDB
blockchain = Blockchain()
db = TinyDB("blockchain.json")
validators_db = TinyDB("validators.json")
users_db = TinyDB("users.json")

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
    if not blockchain.pending_transactions:
        st.warning("⚠️ No transactions to add to a new block! Add transactions first.")
    else:
        # Select a validator before mining
        validator = blockchain.select_validator()
        
        if not validator:
            st.warning("⚠️ No validator available! Stake coins first.")
        else:
            # Debug: Show transactions before mining
            st.write("🛠️ Transactions to be added:", blockchain.pending_transactions)
            st.write(f"🔍 Selected Validator: {validator}")

            blockchain.add_block(validator)
            latest_block = blockchain.get_latest_block()

            # Debug: Show the block data
            st.write("🛠️ New Block Data:")
            st.json({
                "index": latest_block.index,
                "previous_hash": latest_block.previous_hash,
                "timestamp": latest_block.timestamp,
                "transactions": latest_block.transactions,
                "validator": latest_block.validator,
                "hash": latest_block.hash,
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

            # Clear pending transactions
            blockchain.pending_transactions = []
            st.success(f"✅ Block {latest_block.index} mined successfully by {validator} and saved to TinyDB!")





# Run Blockchain Validity Check
st.subheader("✅ Check Blockchain Validity")
if st.button("Validate Blockchain"):
    if blockchain.is_chain_valid():
        st.success("✅ Blockchain is valid!")
    else:
        st.error("❌ Blockchain is NOT valid!")

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
