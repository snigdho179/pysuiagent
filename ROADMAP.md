# 🗺️ Sui-Py-Agent Roadmap (2026)

This roadmap outlines the development trajectory for **pysuiagent**, moving from a foundational SDK to a comprehensive **Autonomous Agent Framework** for the Sui Ecosystem.

---

## ✅ Phase 1: Core Agent Infrastructure (Completed)
*Goal: Build the "Hands" of the Agent—enabling basic connectivity and financial transactions.*

- [x] **Semantic SDK:** High-level Python class `SuiAgent` for wallet management.
- [x] **Smart Coin Manager:** Logic to automatically merge "dust" coins (`split_coin` from gas) to prevent `ObjectInUse` errors.
- [x] **AI-Native Data:** Automatic conversion of raw MIST (integer) to SUI (float) for LLM context.
- [x] **Safety Layer:** `dry_run()` transaction simulation for AI pre-validation.
- [x] **Testnet Faucet:** One-function auto-funding for rapid prototyping.

---

## 🚧 Phase 2: DeFi Protocol Packs (Grant Milestone 1)
*Goal: Enable Agents to participate in the DeFi economy (Yield, Swaps, Liquidity).*

### 1. Navi Protocol Integration (Lending/Borrowing)
* **Feature:** Semantic wrappers for Navi's lending pools.
* **Syntax:** `agent.protocols.navi.supply("SUI", 10)`
* **Use Case:** Agents can autonomously manage yield farming strategies or collateralize assets.

### 2. Cetus DEX Integration (Swapping)
* **Feature:** Integration with Cetus CLMM (Concentrated Liquidity Market Maker) for efficient swaps.
* **Syntax:** `agent.protocols.cetus.swap(from_token="SUI", to_token="USDC", amount=5)`
* **Use Case:** Arbitrage bots and automated portfolio rebalancing agents.

### 3. Token Standard Support
* **Feature:** Unified interface for managing non-SUI assets (USDC, SEND, FUD).
* **Syntax:** `agent.balance(token="0x...::usdc::USDC")`

---

## 🔐 Phase 3: Mainnet Hardening (Security Audit)
*Goal: Transition from a Testnet PoC to a Production-Grade Mainnet SDK.*

### 1. Secure Key Management
* **Upgrade:** Remove reliance on local `wallet.json`.
* **Implementation:** Integrate with **AWS Secrets Manager** and system Environment Variables (`OS_ENV`) to handle private keys without writing them to disk.

### 2. Mainnet RPC Configuration
* **Upgrade:** Allow dynamic switching between Testnet and Mainnet.
* **Implementation:** Add `network="mainnet"` parameter to `SuiAgent()` init, with support for custom RPC endpoints (Shinami, Mysten) to handle high traffic.

### 3. Error Resilience (Retry Logic)
* **Upgrade:** Add automatic retry mechanisms for network timeouts or congestion.
* **Implementation:** `Exponential Backoff` strategy for failed RPC calls to ensure agents don't crash during market volatility.

---

## 🔮 Phase 4: The Agentic Web (Future Innovation)
*Goal: Align with Sui's 2025 roadmap for AI, Storage, and Mass Adoption.*

### 1. Model Context Protocol (MCP) Support
* **Concept:** Implement an [MCP](https://modelcontextprotocol.io/) Server interface.
* **Impact:** Allows `pysuiagent` to be installed as a native "Tool" in **Claude Desktop**, **ChatGPT**, and other MCP-compliant LLM interfaces.

### 2. Sponsored Transactions (Gasless Agents)
* **Concept:** Integrate Sui's [Sponsored Transaction](https://docs.sui.io/concepts/transactions/sponsored-transactions) primitive.
* **Impact:** Enables "Ephemeral Agents" that do not need to hold SUI for gas. The developer's main wallet pays the fees.

---

## 🛡️ Long-Term Vision
To become the standard **Python Interface** for the Agentic Web on Sui, empowering millions of Python-native AI developers to build on-chain without learning Rust or TypeScript.
