from solcx import compile_standard
import json
from web3 import Web3

with open("./SimpleStorage.sol","r") as file:
    simple_storage=file.read()


compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("./compilation.json", "w") as file:
    json.dump(compiled_sol, file)


abi=compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
bytecode=compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# testnet== goerli
chainId=5
my_address= "0xF9018fdF8CbeFb82b9977815eB9619883d8ac5c7"
PRIVATE_KEY= "39a02a566b29ab167d78ac397adfd9615f2695be24bca55c89e9919c5966906d"
provider= Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/1b5903345a4049dda5930ce3dcaadd7c"))


simple_storage_contract= provider.eth.contract(abi=abi,bytecode=bytecode)
nonce = provider.eth.getTransactionCount(my_address)
transaction=simple_storage_contract.constructor().buildTransaction({
    "chainId":chainId,
    "from":my_address,
    "gas":600000,
    "gasPrice": provider.eth.gas_price,
    "nonce":nonce,
    

})

signed_tx=provider.eth.account.sign_transaction(transaction,PRIVATE_KEY)

#hash
hash= provider.eth.send_raw_transaction(signed_tx.rawTransaction)
print('the transaction hash is :  ' ,  hash)
receipt= provider.eth.wait_for_transaction_receipt(hash)
#receipt
print('the transaction receipt is : ',receipt)
print('the contract address is : ', receipt.contractAddress)

the_instance= provider.eth.contract(address=receipt.contractAddress,abi=abi)

print(the_instance.functions.retrieve().call()) 

tx1= the_instance.functions.store(11).buildTransaction(
    {
        "chainId":chainId,
        "nonce":nonce+1,
        "from": my_address,
        "gasPrice":provider.eth.gasPrice,
        "gas":500000
    }
)

signed_tx1= provider.eth.account.signTransaction(tx1,PRIVATE_KEY)
hash1= provider.eth.send_raw_transaction(signed_tx1.rawTransaction)
receipt1= provider.eth.wait_for_transaction_receipt(hash1)

print(the_instance.functions.retrieve().call())

