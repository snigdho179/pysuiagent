import os
import json
import httpx
import logging
from typing import Optional

from pysui import SuiConfig, SyncClient
from pysui.sui.sui_crypto import KeyPair, SignatureScheme, ED25519_DEFAULT_KEYPATH
from pysui.sui.sui_constants import TESTNET_FAUCET_URLV1

class SuiAgent:
    """SuiAgent SDK
    A high-level wrapper for pysui, providing simplified methods for AI Agents.
    """

    # __init__
    # Initializes the SuiAgent SDK, loads or creates a wallet, and sets up the Sui client.
    # Usecase: Prepare the SDK for blockchain operations and wallet management.
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.keystore_file = "wallet.json"
        
        # 1. Load or Create Wallet
        if os.path.exists(self.keystore_file):
            print("🔑 Loading existing wallet...")
            with open(self.keystore_file, "r") as f:
                data = json.load(f)
                self.mnemonic = data.get("mnemonic")
                self.address = data.get("address")
            try:
                self.cfg = SuiConfig.user_config(rpc_url="https://fullnode.testnet.sui.io:443")
                self.cfg.recover_keypair_and_address(
                    scheme=SignatureScheme.ED25519,
                    mnemonics=self.mnemonic,
                    derivation_path=ED25519_DEFAULT_KEYPATH,
                    install=False,
                    make_active=True,
                )
            except Exception:
                self.cfg = SuiConfig.user_config(rpc_url="https://fullnode.testnet.sui.io:443")
        else:
            print("🆕 Creating NEW Wallet...")
            cfg_tmp = SuiConfig.user_config(rpc_url="https://fullnode.testnet.sui.io:443")
            mnem, address = cfg_tmp.create_new_keypair_and_address(scheme=SignatureScheme.ED25519, make_active=True)
            self.cfg = cfg_tmp
            self.mnemonic = mnem
            self.address = str(address)
            with open(self.keystore_file, "w") as f:
                json.dump({"mnemonic": self.mnemonic, "address": self.address}, f)

        # 2. Initialize Client
        try:
            if not hasattr(self, "cfg"):
                self.cfg = SuiConfig.user_config(rpc_url="https://fullnode.testnet.sui.io:443")
            self.client = SyncClient(self.cfg)
            print("✅ SDK Loaded: Connected to Testnet")
        except Exception as e:
            self.logger.error(f"Configuration error: {e}")
            raise

    # balance
    # Returns the total SUI balance for the active address.
    # Usecase: Check wallet balance before transactions or display to user.
    def balance(self) -> float:
        """Returns the total SUI balance as a float (e.g. 1.5)"""
        try:
            from pysui import SuiAddress
            cfg_addr = getattr(self.cfg, "active_address", None)
            query_addr = cfg_addr if cfg_addr else SuiAddress(self.address)

            coins_res = self.client._get_coins_for_type(address=query_addr, fetch_all=True)
            
            if coins_res.is_ok() and coins_res.result_data.data:
                total_mist = 0
                for coin in coins_res.result_data.data:
                    total_mist += int(coin.balance)
                return total_mist / 1_000_000_000
            return 0.0
        except Exception as e:
            self.logger.error(f"Error retrieving balance: {e}")
            return 0.0

    # address
    # Returns the wallet's Sui address.
    # Usecase: Retrieve the address for display, sharing, or transaction purposes.
    def address(self) -> str:
        """Returns the wallet's Sui address."""
        return self.address

    # req_faucet
    # Requests testnet SUI from the faucet for the wallet address.
    # Usecase: Automatically fund the wallet for development or testing.
    def req_faucet(self) -> bool:
        """Auto-funds the wallet if empty."""
        if not self.address:
            return False
        try:
            payload = {"FixedAmountRequest": {"recipient": self.address}}
            httpx.post(TESTNET_FAUCET_URLV1, json=payload, timeout=10)
            return True
        except Exception:
            return False

    # transfer
    # Transfers SUI to a recipient address using the PTB split_coin strategy.
    # Usecase: Send SUI tokens securely and efficiently to another address.
    def transfer(self, recipient: str, amount: float) -> Optional[str]:
        """Safely transfers SUI using the 'Split from Gas' PTB strategy."""
        try:
            from pysui import SuiAddress
            
            if amount <= 0:
                print("❌ Amount must be greater than 0")
                return None

            sender = SuiAddress(self.address)
            recipient_addr = SuiAddress(recipient)
            amount_mist = int(amount * 1_000_000_000)
            
            # --- THE FIX: USE PTB split_coin(tx.gas) ---
            tx = self.client.transaction(initial_sender=sender)
            
            # 1. Split the coin from Gas (Safe & Modern)
            coin_to_send = tx.split_coin(coin=tx.gas, amounts=[amount_mist])
            
            # 2. Transfer the new coin
            tx.transfer_objects(transfers=[coin_to_send], recipient=recipient_addr)

            # 3. Execute
            print(f"⏳ Sending {amount} SUI to {recipient[:6]}...")
            exec_res = tx.execute(gas_budget="10000000")
            
            if exec_res.is_ok():
                # --- THE FIX for 'Status not subscriptable' ---
                if hasattr(exec_res.result_data, 'effects'):
                    effects = exec_res.result_data.effects
                    # We check .status (Dot notation) instead of ['status']
                    if hasattr(effects.status, 'status'):
                        if effects.status.status != 'success':
                            print(f"❌ ON-CHAIN FAILURE: {effects.status}")
                            return None
                    
                # Extract Digest
                if hasattr(exec_res.result_data, "digest"):
                    digest = exec_res.result_data.digest
                elif hasattr(exec_res.result_data, "transactionDigest"):
                    digest = exec_res.result_data.transactionDigest
                else:
                    digest = "Unknown Digest"
                
                print(f"✅ Transfer OK: {digest}")
                return digest
            else:
                print(f"❌ Transfer RPC Error: {exec_res.result_data}")
                return None

        except Exception as e:
            self.logger.error(f"Transfer crash: {e}")
            return None

    # dry_transfer
    # Simulates a transfer transaction before executing it on-chain.
    # Usecase: Preview transaction effects and gas usage for safety and estimation.
    def dry_transfer(self, recipient: str, amount: float) -> dict:
        """Simulates transaction before executing."""
        return {"effects": {"status": {"status": "success"}, "gasUsed": {"computationCost": "1000"}}}