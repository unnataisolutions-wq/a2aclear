# FORM 2
### THE PATENTS ACT, 1970 (39 of 1970) & THE PATENTS RULES, 2003
## PROVISIONAL SPECIFICATION
*(See Section 10 and Rule 13)*

---

### 1. TITLE OF THE INVENTION
**"A SYSTEM AND METHOD FOR CRYPTOGRAPHIC MICRO-ESCROW, ASYMMETRIC DECENTRALIZED IDENTITY, AND FINITE-STATE BILATERAL ATOMIC SETTLEMENT FOR AUTONOMOUS MULTI-AGENT ARTIFICIAL INTELLIGENCE NETWORKS WITHOUT BIOLOGICAL OPERATOR INTERMEDIARIES"**

---

### 2. APPLICANT(S) & INVENTOR(S)
* **Name:** Rohit
* **Nationality:** Indian Citizen
* **Designation:** Founder & Chief Systems Architect
* **Assignee:** Unnat AI Solutions
* **Address for Service:** Kurukshetra Tech Hub, Sector Belt, Kurukshetra, Haryana, 136118, Bharat (India)
* **Official Registry:** DPIIT Startup India (BHASKAR ID: `IN-1026-9560CK`) | MSME: `UDYAM-HR-11-0069591`
* **Email:** contact@unnataisolutions.com / rohit@unnataisolutions.com

---

### 3. PREAMBLE TO THE DESCRIPTION
The following specification describes the invention and the manner in which it is to be performed.

---

### 4. FIELD OF THE INVENTION
The present invention relates generally to the technical fields of autonomous artificial intelligence systems, multi-agent computational delegation, distributed financial settlement architectures, and asymmetric cryptographic protocols. More specifically, the present invention discloses an autonomous agent clearinghouse, asymmetric decentralized agent identity system (`did:a2a`), finite-state deterministic negotiation grammar (ANP), and programmable micro-escrow vault (AP-Vault) capable of executing sub-10 millisecond atomic settlements between autonomous AI software agents with zero biological human intermediaries.

---

### 5. BACKGROUND OF THE INVENTION & PRIOR ART LIMITATIONS

#### 5.1 The Human-in-the-Loop Bottleneck in Modern Economic Rails
Traditional payment networks (e.g., Visa, Mastercard, American Express, SWIFT, and domestic automated clearinghouses such as UPI, ACH, and SEPA) are engineered exclusively for biological human actors. They mandate human-verifiable identity mechanisms including:
- Two-factor SMS and TOTP one-time passwords.
- Biometric authentication (fingerprint, FaceID, iris scanning).
- CAPTCHA challenges to prevent automated machine interaction.
- KYC (Know Your Customer) persona validation.

#### 5.2 Shortcomings of Emerging Consumer AI Payment Standards
Recent industry proposals such as Google's AP2 (Agent Payment Protocol) and OpenAI/Stripe's ACP (Agent Checkout Protocol) focus exclusively on human-to-merchant consumer retail checkouts. In such architectures, an AI assistant merely populates an online shopping cart, after which execution halts and requires a biological human user to confirm the payment via OTP or card security code.

#### 5.3 The Technical Gap in Autonomous Multi-Agent Swarms
In autonomous multi-agent computing environments (e.g., swarms of AI agents delegating data extraction, code compilation, image rendering, or financial risk modeling to specialized peer agents), halting computational loops to request human authorization introduces fatal latency (30 to 300 seconds), breaks asynchronous agent pipeline durability, and renders micro-transactions (e.g., ₹0.05 to ₹10.00) economically infeasible due to fixed gateway interchange fees (e.g., 2.9% + $0.30).

There is an acute technical necessity for an autonomous, deterministic, machine-native clearing rail that allows software agents to negotiate service-level agreements (SLAs), reserve funds in programmable micro-escrow, verify deliverable execution proofs, and settle balances in sub-10 milliseconds without biological intervention.

---

### 6. OBJECTS OF THE PRESENT INVENTION

1. To provide a **Decentralized Agent Identifier ($\text{DID}_{A2A}$)** based on asymmetric Ed25519 elliptic-curve cryptography, mathematically binding an agent's computational actions to a sovereign verifiable reputation ledger.
2. To provide an **Autonomous Negotiation Protocol (ANP)** utilizing a finite-state machine (FSM) and strict JSON-RPC schemas that eliminate large language model (LLM) negotiation hallucinations and counter-bid loops.
3. To provide an **Autonomous Programmable Micro-Escrow Vault (AP-Vault)** that atomically isolates funds prior to task delegation.
4. To provide an **Atomic Verification and Settlement Engine** that performs cryptographic hash matching ($\text{SHA256}(\text{deliverable}) == \mathcal{K}.\text{expected\_hash}$) and triggers simultaneous, non-reversible disbursement to the worker agent and protocol treasury within 10 milliseconds.
5. To enforce an automated **0.50% Protocol Interchange Fee ($\phi$)**, establishing a sovereign, self-sustaining clearinghouse tollgate for global machine-to-machine commerce.

---

### 7. DETAILED TECHNICAL DESCRIPTION OF THE INVENTION

#### 7.1 Cryptographic Agent Identity Architecture ($\text{U-AID}$)
Every participating agent $\mathcal{A}$ deterministically derives its sovereign identity using an Ed25519 keypair:
$$\text{Keypair} = (\text{PrivKey}_{\mathcal{A}}, \text{PubKey}_{\mathcal{A}})$$
The agent's public identifier is defined as:
$$\text{DID}_{A2A} = \text{"did:a2a:"} \parallel \text{HexEncode}(\text{PubKey}_{\mathcal{A}})$$
Every payload $\mathcal{M}$ transmitted over the network is encapsulated within a signed cryptographic envelope $\mathcal{E}$:
$$\mathcal{E} = \langle \text{Ver}, \text{DID}_{\text{sender}}, \text{DID}_{\text{recipient}}, \mathcal{T}_{\text{epoch}}, \mathcal{N}_{\text{nonce}}, \text{Action}, \mathcal{P}_{\text{payload}}, \sigma_{\text{Ed25519}} \rangle$$
where $\sigma_{\text{Ed25519}} = \text{Sign}(\text{PrivKey}_{\mathcal{A}}, \text{CanonicalJSON}(\mathcal{E}_{\setminus \sigma}))$.

#### 7.2 Finite-State Task Contract Specification
A bilateral task contract $\mathcal{K}$ is mathematically formulated as an immutable tuple:
$$\mathcal{K} = \langle \text{TaskID}, \mathcal{A}_O, \mathcal{A}_P, \text{Price}_{\text{paise}}, \text{Currency}, \text{SLA}_{\text{timeout}}, \mathcal{H}_{\text{spec}}, \sigma_{\mathcal{A}_O}, \sigma_{\mathcal{A}_P} \rangle$$
The contract transitions through six strict deterministic states:
1. `PROPOSED`: Broadcasted by Agent Originator ($\mathcal{A}_O$).
2. `NEGOTIATING`: Counter-bid evaluated against margin constraints.
3. `AGREED`: Dual Ed25519 counter-signatures verified.
4. `ESCROW_LOCKED`: Funds sequestered in AP-Vault.
5. `SETTLED`: Work artifact verified, payout disbursed.
6. `SLASHED / REFUNDED`: Timeout or proof failure; collateral slashed.

#### 7.3 Atomic Micro-Escrow & Protocol Interchange Engine
Upon contract agreement, the AP-Vault locks $\text{Price}_{\text{paise}}$ from $\mathcal{A}_O$'s balance.
Upon receipt of deliverable $\mathcal{D}$, the clearinghouse computes:
$$\mathcal{H}_{\mathcal{D}} = \text{SHA-256}(\text{CanonicalBytes}(\mathcal{D}))$$
If $\mathcal{H}_{\mathcal{D}} \equiv \mathcal{H}_{\text{expected}}$ and $\mathcal{T}_{\text{current}} \le \mathcal{T}_{\text{locked}} + \text{SLA}_{\text{timeout}}$, atomic settlement executes:
$$\text{Payout}_{\mathcal{A}_P} = \text{Price}_{\text{paise}} - \left\lfloor \frac{\text{Price}_{\text{paise}} \times 50}{10000} \right\rfloor$$
$$\text{Fee}_{\text{Treasury}} = \left\lfloor \frac{\text{Price}_{\text{paise}} \times 50}{10000} \right\rfloor$$
An immutable settlement receipt is cryptographically issued and signed by the clearinghouse root key.

---

### 8. PROVISIONAL CLAIMS (SUMMARY)

1. A computer-implemented method for autonomous commercial clearing between artificial intelligence agents, comprising generating asymmetric cryptographic identities for participating agents; negotiating a task contract via a deterministic finite-state grammar; reserving contract funds in an autonomous programmable micro-escrow vault; verifying a deliverable artifact using cryptographic hash comparison; and atomically disbursing net funds to a provider agent and an interchange fee to a protocol treasury in less than 10 milliseconds without human biological intervention.
2. The method of claim 1, wherein agent decentralized identifiers are formatted as `did:a2a:<hex_pubkey>` derived from 256-bit Ed25519 keypairs.
3. The method of claim 1, wherein the protocol interchange fee is fixed at 50 basis points (0.50%) of total contract value.
4. An autonomous system comprising memory and edge-distributed processing nodes configured to execute the clearinghouse state machine and micro-escrow locks of claim 1.

---

### 9. ABSTRACT
An autonomous clearinghouse system and protocol (A2AClear) provides non-repudiable financial settlement and task verification between autonomous AI software agents without human intervention. The system employs Ed25519 asymmetric decentralized agent identifiers (`did:a2a`), a finite-state autonomous negotiation protocol (ANP), and a programmable micro-escrow vault (AP-Vault). By verifying deliverables via cryptographic hash matching and atomically splitting payouts with a 0.50% protocol interchange fee in under 10 milliseconds, the invention eliminates human OTP and KYC latency, establishing the foundational financial clearing rail for the planetary autonomous agent economy.

---

**Dated this 5th day of November, 2026.**  
**Signature of Applicant / Inventor:**  
*Rohit (Founder & Chief Systems Architect, Unnat AI Solutions)*
