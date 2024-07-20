import sys
import time
import asyncio
from solders.keypair import Keypair
from solana.rpc.api import Client
from buy_swap import buy
from sell_swap import sell_normal
from dotenv import dotenv_values
from create_wallet import create_wallet
from transfer import transfer_fund
import json
config = dotenv_values(".env")


if len(sys.argv) < 3:
    print("Usage: python main.py <CONTRACT_ADDRESS> <PRIVATE_KEY_1> ")
    sys.exit(1)

# Get contract address and wallet keys from console arguments
arg_contract_address=sys.argv[1]
funding_wallet=sys.argv[2]

# print(arg_contract_address,arg_wallet_keys)
# Connect to Solana cluster
solana_client = Client(config["RPC_HTTPS_URL"])

# Define buy amounts and cycles
# Example usage
start = 0.0000001
stop = 0.0000009
num_elements = 3
buy_times=1
number_of_wallets=10
amount_in_sol = 0.001  # 1 SOL

# Convert the amount to lamports
amount_in_lamports = int(amount_in_sol * 1_000_000_000)
def float_range(start, stop, num_elements):
    step = (stop - start) / (num_elements - 1)
    return [start + step * i for i in range(num_elements)]
amounts = float_range(start, stop, num_elements)
async def main():
    payer = Keypair.from_base58_string(funding_wallet)
    print("Creating Wallets ")
    await create_wallet(number_of_wallets)

    print("Opemning Wallets ")
    with open('wallets.json', 'r') as file:
        wallets = json.load(file)
    for wallet in wallets:
        print("transfering funds in Wallet ",wallet['public_key'])
        receiver = Keypair.from_base58_string(wallet['private_key'])
        await transfer_fund(solana_client,payer,receiver,amount_in_lamports)
        wallet['transfer']=True
        time.sleep(5)
    token_toBuy=arg_contract_address #Enter token you wish to buy here
    for i in range(buy_times):
        print("Buy time",i+1)
        for wallet in wallets:
            payer_wallet = Keypair.from_base58_string(wallet['private_key'])
            for amount in amounts:

                buy_transaction=await buy(solana_client, token_toBuy, payer_wallet, amount) #Enter amount of sol you wish to spend
                print(buy_transaction,"Buy TX with Amount",amount)
                time.sleep(5)
            
            sell_transaction=await sell_normal(solana_client, token_toBuy, payer_wallet)
            print(sell_transaction,"Sell TX",)
            time.sleep(5)
            wallet['traded']=True
        

while True:
    
    asyncio.run(main())