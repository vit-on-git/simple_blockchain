from flask import Flask, request, jsonify
from simple_blockchain5 import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{
        'index': block.index,
        'previous_hash': block.previous_hash,
        'timestamp': block.timestamp,
        'transactions': block.transactions,
        'validator': block.validator,
        'hash': block.hash
    } for block in blockchain.chain]
    return jsonify({'length': len(blockchain.chain), 'chain': chain_data}), 200

@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data or 'transaction' not in data:
        return jsonify({'message': 'Invalid transaction data'}), 400
    
    blockchain.create_transaction(data['transaction'])
    return jsonify({'message': 'Transaction added'}), 201

@app.route('/mine', methods=['POST'])
def mine_block():
    blockchain.validate_and_add_block()
    return jsonify({'message': 'Block added'}), 201

@app.route('/latest', methods=['GET'])
def get_latest_block():
    latest_block = blockchain.get_latest_block()
    return jsonify({
        'index': latest_block.index,
        'previous_hash': latest_block.previous_hash,
        'timestamp': latest_block.timestamp,
        'transactions': latest_block.transactions,
        'validator': latest_block.validator,
        'hash': latest_block.hash
    }), 200

@app.route('/stake', methods=['POST'])
def stake_coins():
    data = request.get_json()
    if not data or 'validator' not in data or 'amount' not in data:
        return jsonify({'message': 'Invalid stake data'}), 400
    
    blockchain.stake_coins(data['validator'], data['amount'])
    return jsonify({'message': f'{data["amount"]} coins staked by {data["validator"]}'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
