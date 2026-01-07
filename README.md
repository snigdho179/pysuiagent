### pysuiagent
SuiAgent SDK 🌊

SuiAgent is a professional, high-level Python SDK designed to empower AI Agents and developers to interact seamlessly with the Sui Blockchain.

Built on top of the powerful pysui library, it abstracts away the complexities of cryptographic signatures, Programmable Transaction Blocks (PTB), and gas management, offering a clean, human-readable API.

##🚀 Key Features

#🔑 Automated Wallet Management

Automatically generates a secure ED25519 keypair on first run.

Persists credentials locally in wallet.json for stateful agent sessions.

Auto-loads existing wallets for continuous operation.

#💸 Smart Transfers (PTB)

Implements the modern "Split from Gas" strategy using Programmable Transaction Blocks.

Eliminates "insufficient gas" errors by dynamically splitting coins from the gas object.

Includes built-in safety checks and error handling for on-chain execution.

#🚰 Integrated Faucet Access

Programmatic access to the Sui Testnet Faucet.

Allows agents to self-fund their wallets when balances are low.

#⚡ Simplified State Access

One-line methods to retrieve real-time balances (automatically converted from MIST to SUI).

Instant access to wallet addresses and digest verification.

#🛠️ Installation

Ensure you have Python 3.10+ installed.

Install Dependencies:

pip install pysui httpx


Add the SDK:
Simply drop pysuiagent.py into your project directory.

##📖 Usage Guide

#1. Initialization

The SDK handles connection to the Sui Testnet and wallet setup automatically.

from pysuiagent import SuiAgent

 This will:
 1. Look for 'wallet.json'
 2. If missing, create a NEW wallet and save it
 3. Connect to Sui Testnet
agent = SuiAgent()

print(f"🤖 Agent Active at: {agent.address}")


#2. Checking Balance

Get the clean float value of your SUI balance (no need to calculate decimals).

balance = agent.balance()
print(f"💰 Current Balance: {balance} SUI")


3. Self-Funding (Faucet)

If your agent is running low on gas, it can request funds autonomously.

if agent.balance() < 1.0:
    print("🚰 Requesting funds from faucet...")
    success = agent.req_faucet()
    if success:
        print("✅ Faucet request sent!")


#4. Sending Tokens

Transfer SUI to another address securely.

recipient = "0x..." # Replace with valid Sui address
amount = 0.5        # Amount in SUI

tx_digest = agent.transfer(recipient, amount)

if tx_digest:
    print(f"🚀 Transaction confirmed! Digest: {tx_digest}")
else:
    print("❌ Transaction failed.")


#5. Dry Run (Simulation)

Preview transaction effects before spending real gas.

simulation = agent.dry_transfer(recipient, 0.5)
print("Simulation result:", simulation)


##🏗️ Architecture

Wallet Persistence

The SDK uses a wallet.json file to store the mnemonic phrase and address.

⚠️ Security Note: This file contains your private key (mnemonic). Ensure it is added to your .gitignore and never shared publicly.

Transaction Strategy

SuiAgent uses a Programmable Transaction Block (PTB) approach for transfers. Instead of selecting a specific coin object, it splits the transfer amount directly from the gas coin used for the transaction. This ensures higher success rates and simpler coin management.

##📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

Built for the Sui Ecosystem 💧
