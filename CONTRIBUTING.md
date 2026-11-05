# Contributing to A2AClear Protocol

Thank you for your interest in contributing to the **A2AClear Sovereign Protocol** (RFC-0001)!

## 🏛️ Code of Conduct & Sovereign Standard
A2AClear is governed as a high-integrity, high-performance financial clearing standard for autonomous AI agents. All contributions must adhere to:
1. **Mathematical Determinism:** No non-deterministic LLM loops inside core escrow or negotiation state transitions.
2. **Cryptographic Rigor:** All messages must preserve Ed25519 asymmetric signature validity.
3. **Sub-10ms Latency:** Zero external blocking I/O on critical settlement paths.

## 🛠️ Development Workflow
1. Fork the repository: `https://github.com/unnataisolutions-wq/a2aclear`
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Install dependencies in editable mode: `cd python && pip install -e .`
4. Run the test suite:
   ```bash
   python python/examples/demo_bilateral_settlement.py
   python python/examples/demo_fortress_defense.py
   python python/examples/demo_security_and_antihack.py
   ```
5. Submit a Pull Request.

## 📜 Licensing
By contributing, you agree that your contributions will be licensed under the [Business Source License 1.1 (BSL 1.1)](LICENSE.md).

*(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.*
