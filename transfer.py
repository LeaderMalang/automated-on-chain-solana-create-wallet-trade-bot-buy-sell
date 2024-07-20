from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solana.rpc.api import RPCException
import asyncio
import time
MAX_RETRIES = 3
RETRY_DELAY = 3
async def transfer_fund(solana_client,sender,receiver,amount):

    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            transfer_ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver.pubkey(), lamports=amount))
            txn = Transaction().add(transfer_ix)
            res=solana_client.send_transaction(txn, sender)
            if res.value:
                print("Transfer Transaction Url ",f'https://solscan.io/tx/{res.value}')
                return res.value
        except asyncio.TimeoutError:
            print("Transaction confirmation timed out. Retrying...")
            retry_count += 1
            time.sleep(RETRY_DELAY)
        except RPCException as e:
            print(f"RPC Error: [{e.args[0].message}]... Retrying...")
            retry_count += 1
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"Unhandled exception: {e}. Retrying...")
            # retry_count= MAX_RETRIES
            retry_count += 1
            time.sleep(RETRY_DELAY)
       
    return False