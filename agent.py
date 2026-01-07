import time
import re
import sys
from pysuiagent import SuiAgent

# Initialize the Agent
print("--- 🤖 INITIALIZING SUI AI AGENT ---")
try:
    agent = SuiAgent()
    print("✅ Agent Online. Connected to Testnet.")
except Exception as e:
    print(f"❌ Failed to start Agent: {e}")
    sys.exit(1)

my_addr = agent.address

def print_slow(text):
    """Makes the text look like it's being typed by an AI"""
    print(text)
    time.sleep(0.5)

def parse_and_execute(user_input):
    user_input = user_input.lower().strip()
    # --- 1. GET ADDRESS ---
    if "address" in user_input or "who am i" in user_input:
        print_slow(f"🤖 AGENT: Your wallet address is: {my_addr}")
        print(f"   (View on Explorer: https://suiscan.xyz/testnet/account/{my_addr})")
        return

    # --- 2. GET BALANCE ---
    if "balance" in user_input or "how much" in user_input:
        print_slow("🤖 AGENT: Checking the blockchain...")
        bal = agent.balance()
        print_slow(f"💰 AGENT: You currently have {bal:.4f} SUI.")
        return

    # --- 3. FAUCET (FUND WALLET) ---
    if "faucet" in user_input or "give me money" in user_input or "fund" in user_input:
        print_slow("🤖 AGENT: Contacting Sui Testnet Faucet...")
        success = agent.req_faucet()
        if success:
            print_slow("✅ AGENT: Faucet request sent! Wait 10s for coins to arrive.")
        else:
            print_slow("❌ AGENT: Faucet failed. You might be rate-limited.")
        return

    # --- 4. TRANSFER & DRY RUN ---
    # Regex to find "send/simulate X to Y"
    # Matches: "send 0.1 to 0x123" or "pay 0.1 to 0x123"
    match = re.search(r"(send|pay|transfer|simulate|test)\s+([\d\.]+)\s+(?:sui\s+)?(?:to\s+)?(0x[a-fA-F0-9]+)", user_input)

    if match:
        action = match.group(1)
        amount = float(match.group(2))
        recipient = match.group(3)

        # A. DRY RUN / SIMULATION
        if action in ["simulate", "test"]:
            print_slow(f"🤖 AGENT: Simulating transaction (Safety Check)...")
            result = agent.dry_transfer(recipient=recipient, amount=amount)

            if result:
                status = result.get('effects', {}).get('status', {})
                if status.get('status') == 'success':
                    print_slow("✅ AGENT: Simulation SUCCESS. This transaction is safe to execute.")
                    print(f"   (Gas Cost Estimate: {result.get('effects', {}).get('gasUsed', {}).get('computationCost', 'Unknown')} MIST)")
                else:
                    print_slow("⚠️ AGENT: Simulation predicted a FAILURE.")
            else:
                print_slow("❌ AGENT: Simulation crashed.")
            return

        # B. REAL TRANSFER
        else:
            print_slow(f"🤖 AGENT: Preparing to send {amount} SUI to {recipient[:6]}...")
            confirm = input(f"   ⚠️ Are you sure? (type 'yes'): ")
            if confirm.lower() != "yes":
                print("🚫 Cancelled.")
                return

            tx_digest = agent.transfer(recipient=recipient, amount=amount)
            if tx_digest:
                print_slow(f"✅ AGENT: Transaction Sent! ID: {tx_digest}")
                print(f"   🔗 https://suiscan.xyz/testnet/tx/{tx_digest}")
            else:
                print_slow("❌ AGENT: Transaction failed.")
            return

    # --- HELP / UNKNOWN ---
    print("🤖 AGENT: I didn't understand. Try these commands:")
    print("   - 'What is my address?'")
    print("   - 'Check balance'")
    print("   - 'Give me money' (Faucet)")
    print("   - 'Simulate 0.01 to 0x...'" )
    print("   - 'Send 0.01 to 0x...'")

# --- MAIN LOOP ---
print("\n💬 SYSTEM READY. Type 'exit' to quit.\n")
while True:
    try:
        user_text = input("👤 COMMAND: ")
        if user_text.lower() in ["exit", "quit"]:
            print("👋 Shutting down.")
            break
        parse_and_execute(user_text)
        print("-" * 40)
    except KeyboardInterrupt:
        break