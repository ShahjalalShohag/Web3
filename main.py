from web3 import Web3
import json
import os

# connecting to a hosted ethereum node (infura)
infura_url = os.environ.get("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())
# looking up blocks
print(web3.eth.get_block(32415))


# checking wallet balance
metamask_addr = os.environ.get("METAMASK_ADDRESS")  # my metamask address
wei_balance = web3.eth.get_balance(metamask_addr)
balance = web3.fromWei(wei_balance, "ether")
print(balance)

# connecting to an ERC-20 token -- Tether USD (USDT) which is powered by smart contract
# abi is a json array of what the smart contract looks like
# abi link: https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7#code
f = open("tether_abi.json", "r")
abi = json.loads(f.read())
# contract address
address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

contract = web3.eth.contract(address=address, abi=abi)

# playing with the contract specs
total_supply = contract.functions.totalSupply().call()
print(total_supply)

# getting balance of some random dude
checksum_address = web3.toChecksumAddress("0x7d812b62dc15e6f4073eba8a2ba8db19c4e40704")
balance = contract.functions.balanceOf(checksum_address).call()
print(balance)

# connecting to ganache - a local ethereum test net
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
print(web3.isConnected())

account_1 = "0x7e51C02e7D74f76e8105d6D1424CFf085fea92c7"
account_2 = "0x5A083aa628166BB9074f006DdB93Fa62A41C392A"
private_key = "456aec4d9269158799d97190395a4d5a85ba07240fc5c5ed2d71d5046192984a"

# nonce means "number only used once", basically it is the number that blockchain miners are solving for
nonce = web3.eth.getTransactionCount(account_1)

# building the transaction
txn = {
    "nonce": nonce,
    "to": account_2,
    "value": web3.toWei(5, "ether"),  # sending 5 ether
    "gas": 1000000,  # gas units
    "gasPrice": web3.toWei(20, "gwei"),
}

# signing the txn
signed_txn = web3.eth.account.sign_transaction(txn, private_key)

# sending the txn
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(web3.toHex(txn_hash))

# getting the txn details
txn_details = web3.eth.get_transaction(txn_hash)
print(txn_details)
