# 🤖 pysuiagent (Python Sui Agent SDK)

pysuiagent is a semantic, high-level Python SDK designed to bridge the gap between AI Agents (LLMs) and the Sui Blockchain.

It abstracts away the complexities of Programmable Transaction Blocks (PTB), Gas Coin management, and BCS serialization, allowing developers to execute financial actions using simple, human-readable methods.

🚀 The Problem

Building AI Agents on Sui is currently too hard.

Complex serialization: LLMs hallucinate when trying to construct raw BCS transactions.

Gas Management: Agents often fail with CoinBalanceNotEnough or ObjectInUse errors when trying to pay for gas.

Data Formatting: RPC nodes return raw MIST integers (e.g., 1000000000), which confuse AI models expecting 1.0 SUI.

🛠️ The Solution: pysuiagent

This SDK acts as a "Translation Layer" between your AI model and the Sui Network.

✅ Smart Gas Logic: Automatically uses the split_coin(gas) PTB strategy to prevent object locking errors.

✅ AI-Native Data: Returns clean float values for balances and semantic status updates.

✅ Safety First: Includes a dry_run mode to simulate transactions before execution.

📦 Installation

1. Clone the repository
git clone [https://github.com/snigdho179/pysuiagent.git](https://github.com/snigdho179/pysuiagent.git)
cd pysuiagent

2. Install dependencies
pip install pysui httpx



⚡ Quick Start (AI Agent)

We include a pre-built AI Interface (agent.py) that accepts natural language commands.

python agent.py



🗣️ Available Voice/Text Commands

User Command

Executed Function

Description

"Check balance"

agent.balance()

Returns float SUI balance.

"What is my address?"

agent.address

Returns wallet address string.

"Give me money"

agent.req_faucet()

Auto-funds wallet via Testnet Faucet.

"Simulate sending 0.1 to..."

agent.dry_transfer()

Runs a safety check (no gas spent).

"Send 0.5 SUI to 0x..."

agent.transfer()

Executes real on-chain payment.

📚 SDK API Reference

If you are building your own bot, import the SuiAgent class from pysuiagent.py.

from pysuiagent import SuiAgent

agent = SuiAgent()



class SuiAgent()

Initializes the connection to Sui Testnet. Automatically loads wallet.json or creates a new keypair if none exists.

1. balance() -> float

Fetches all Coin Objects owned by the address, sums their MIST value, and converts to SUI.

Returns: float (e.g., 1.54)

Why it's better: Standard RPCs return a list of complex objects. This returns a single number an AI can understand.

2. transfer(recipient: str, amount: float) -> Optional[str]

The core "Agentic" function. It handles the complex "Gas Split" logic automatically.

Parameters:

recipient: 0x... address string.

amount: Amount in SUI (e.g., 0.01).

Returns: Transaction Digest ID (str) or None if failed.

Under the Hood:

Creates a Programmable Transaction Block (PTB).

Calls tx.split_coin(gas, amount) to slice the payment directly from the gas object.

Transfers the new object to the recipient.

Signs and executes.

3. req_faucet() -> bool

Connects to the official Sui Testnet Faucet to request funds.

Returns: True if request accepted, False if rate-limited.

4. dry_transfer(recipient: str, amount: float) -> dict

Runs the transaction through the node's dryRun endpoint.

Use Case: Allows an AI Agent to "Think" about a transaction and check for errors/gas costs before actually spending money.

🛡️ Security & Disclaimer

Proof of Concept: This software is a submission for the Sui Grant Program.

Key Storage: Private keys are stored locally in wallet.json. Do not share this file.

Testnet Only: Default configuration is set to fullnode.testnet.sui.io.

📜 License

MIT License. Free to use for any AI x Crypto experiment.
