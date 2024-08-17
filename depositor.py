import json
from web3 import Web3
# from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# load_dotenv()


with open("./IDepositContract.json", "r") as file:
    abi_file = file.read()

with open('./depositData.json', 'r') as file:
    deposit_file = file.read()
# get abi
abi = json.loads(abi_file)["abi"]
# get depositData
depositData = json.loads(deposit_file)
pubkey = depositData['pubkey']
signature = depositData['signature']
depositDataRoot = depositData['depositDataRoot']
withdrawalCredentials = depositData['withdrawalCredentials']
print(f'Deposit for: {pubkey} and {withdrawalCredentials}')

w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/adaaa49f3d3e47f3a4590ec22e55a9be"))
chain_id = 5

my_address_1 = "0x726F0FD369d68F676DED7BB192f31Dc0469fb967"
my_address_2 = '0xE3c39C183f3c8506928727194640d93Fb1897396'

#assign
my_address = my_address_1
private_key = private_key_1
#print(w3.eth.getBalance(my_address))
#balance here is formatted in ether,
balance = w3.eth.getBalance(my_address)
print(f'Balance in ETH: {w3.fromWei(balance,"ether")}')
nonce = w3.eth.getTransactionCount(my_address)
print(f"Current nonce = {nonce}")
# Working with deployed Contracts
deposit_contract = w3.eth.contract(address='0xff50ed3d0ec03aC01D4C79aAd74928BFF48a7b2b', abi=abi)
transaction = deposit_contract.functions.deposit(
"0x"+pubkey,
"0x"+withdrawalCredentials,
"0x"+signature,
"0x"+depositDataRoot).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": 250000000000,
        "gas": 800000,
        "value": 32000000000000000000,
        "from": my_address,
        "nonce": nonce,
    }
)
dry_run = True
if dry_run == False:
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("wait_for_transaction_receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(tx_receipt)
