import base58
from solders.keypair import Keypair
import json

async def create_wallet(WALLETS_AMOUNT):
    data=[]
    
    for x in range(WALLETS_AMOUNT):
        account = Keypair()
        public_key=account.pubkey()
        privateKey = base58.b58encode(account.secret() + base58.b58decode(str(account.pubkey()))).decode('utf-8')
        wallet={"traded":False,"transfer":False,"public_key":str(public_key),"private_key":privateKey}
        data.append(wallet)
    with open('wallets.json', 'w') as f:
        json.dump(data, f, indent=4)