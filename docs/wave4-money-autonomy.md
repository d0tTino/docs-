---
title: "Real-World Cyberpunk Manifesto — Wave 4: Money & Autonomy"
tags: [cyberpunk, finance]
project: docs-hub
updated: 2025-07-29
---

--8<-- "_snippets/disclaimer.md"

# Real-World Cyberpunk Manifesto — Wave 4: Money & Autonomy

Introduction: From OPSEC to FINSEC — The Financial Counter-Attack
This manual marks the fourth wave of the strategic doctrine initiated in this series. It transitions from the defensive postures of operational security (OPSEC), detailed in Wave 3, to the proactive measures of financial security (FINSEC). The core argument of this text is that financial autonomy is not a tangential objective but a critical, non-negotiable enabler of the "Radical Autonomy" mindset articulated in Wave 1[^1] The capacity for authentic thought, dissent, and action is fundamentally compromised when one's ability to acquire, store, and transact value is contingent upon permission from the very corporate-state sovereigns whose architectures of control were mapped in Wave 2[^1] A kill switch on your bank account is a kill switch on your dissent.
This wave, therefore, serves as the direct tactical response to the financial control vectors identified in the Threat Matrix[^1] The looming threats of Programmable Central Bank Digital Currencies (CBDCs) and the legislative co-option of digital assets via frameworks like the U.S. GENIUS Act and the EU's MiCA regulation are not future hypotheticals; they are the legal and technical foundations of a new, more efficient financial panopticon being constructed in the present[^1] The techniques detailed herein are not theoretical financial advice; they are concrete countermeasures designed to build a resilient, parallel financial existence, immune to these emerging systems of surveillance and control.
The analysis re-engages the "DIY imperative" from Wave 1: when the masters' financial systems are designed for legibility, traceability, and programmable control—as evidenced by the extensive monitoring capabilities built into systems like FedNow and the technical mandates for asset seizure in new stablecoin legislation—the only rational and strategic response is to build, operate, and secure one's own[^1] This is the process of seizing the masters' technology—in this case, the cryptographic primitives and decentralized protocols of the digital asset ecosystem—and turning it against their ambition of total financial visibility. This is the financial counter-attack.

## Part I: The Unseen Ledger — Acquiring and Moving Value Anonymously

The foundational layer of financial sovereignty is the ability to transact without leaving a permanent, legible, and identity-linked record on a public ledger. This section provides a technical deep-dive into the next generation of privacy-preserving cryptocurrencies and analyzes the evolving regulatory landscape designed to contain them. The objective is to equip the operator with the knowledge to select the appropriate tools for untraceable value transfer and to navigate the legal chokepoints where these systems intersect with the traditional world.

### Chapter 1: The State of the Art in Untraceable Value

The first generation of cryptocurrencies, exemplified by Bitcoin, offered pseudonymity, where transactions are linked to addresses rather than legal names. This model has proven catastrophically fragile against modern blockchain analysis. True financial privacy requires protocols designed from the ground up to break the links between sender, receiver, and transaction history. As of 2025, two protocols stand at the forefront of this technological arms race: Monero, with its upcoming Seraphis/Jamtis upgrade, and Firo, with its Lelantus Spark protocol.

#### Monero's Next Generation: Seraphis & Jamtis

Monero's planned upgrade to the Seraphis transaction protocol, accompanied by the Jamtis addressing scheme, represents the most significant evolution in its history.2 It is a direct response to the known theoretical weaknesses of its current RingCT protocol, which relies on small, fixed-size ring signatures (currently 16 members) that can be vulnerable to statistical analysis and chain-reaction deanonymization attacks.5

##### Technical Breakdown: From Rings to Full-Chain Membership

Seraphis fundamentally re-architects Monero's transaction structure by separating the cryptographic proofs of "membership" (proving a spent output exists on the blockchain) from the proofs of "ownership" and "spend authorization" (proving you have the right to spend it).6 This modular design allows for much more efficient and powerful membership proofs. The ultimate goal of this architecture is the implementation of Full-Chain Membership Proofs (FCMPs).5 Instead of a transaction input being hidden within a small ring of 15 decoys, an FCMP would allow a user to prove they are spending one valid output from among the entire set of outputs on the blockchain—potentially hundreds of millions of them.2 This exponentially increases the anonymity set to a global scale, rendering traditional statistical tracing and decoy selection analysis effectively obsolete.

The new key image construction in Seraphis, which enables these advanced proofs, is not compatible with Monero's original CryptoNote addresses, necessitating a network-wide migration to a new format.8 This is where the Jamtis addressing scheme comes in.

#### Jamtis Address Scheme: Enhanced Privacy and Usability

Jamtis is designed to solve numerous long-standing privacy and usability issues with Monero's current address system.8 Its key features include:

- **Multi-Tiered View Keys:** Jamtis introduces a more granular permission system for wallets. A "Master" key has full spend authority, but it can derive lesser keys with limited capabilities.8 For example, a `FindReceived` key can be used by a light wallet or a third-party service to scan the blockchain for incoming transactions using "view tags" without being able to see the transaction amounts or generate new addresses. This allows for highly efficient and privacy-preserving wallet synchronization, as the scanning service can discard approximately 99.6% of all blockchain outputs without needing to perform expensive cryptographic operations on them.8
- **Unified Address Structure:** Jamtis eliminates the distinction between "main addresses" and "subaddresses." All addresses are structurally equivalent, which mitigates the "Janus attack," a heuristic that can be used to link subaddresses belonging to the same wallet.9
- **View Tags:** This is a critical efficiency improvement. A view tag is a short, encrypted tag attached to each transaction output. The sender calculates it using a shared secret derived from the recipient's address. The recipient's wallet can quickly scan these tags and use its private view key to determine if a transaction is potentially for them before attempting the much more computationally expensive full transaction decryption. This is what enables the massive speed-up in wallet scanning, reducing the data a light wallet needs to download by a factor of at least 256.8

#### Firo's Alternative Paradigm: Lelantus Spark

Firo's Lelantus Spark protocol represents a different architectural philosophy for achieving on-chain privacy.10 It is an evolution of the "burn-and-redeem" model pioneered by the Zerocoin protocol, where users effectively destroy coins on the public ledger and mint new, anonymous coins with no transaction history into a private, shielded pool.11

##### Technical Breakdown: The Shielded Pool Model

Lelantus Spark's privacy is built upon a combination of well-understood cryptographic primitives that do not require a trusted setup ceremony—a significant security advantage over protocols like Zcash's original Sprout and Sapling implementations.14 The core components include:

- **Pedersen Commitments:** These are used to hide transaction amounts. A commitment scheme allows a user to commit to a value (the amount) while keeping it hidden, but they can later prove that the commitment corresponds to that specific value. The homomorphic property of Pedersen commitments is crucial, as it allows the network to verify that the sum of the hidden input amounts equals the sum of the hidden output amounts in a transaction, ensuring no new currency is created out of thin air.12
- **One-Out-Of-Many Proofs:** This is a form of zero-knowledge proof that allows a user to prove they own one specific coin (commitment) within a large set of all minted private coins (the anonymity set, which can exceed 65,000) without revealing which one it is.11 This is what breaks the link between the "redeem" transaction and the original "burn" transaction.

##### Key Features and Spark Addresses

Lelantus Spark introduces several features designed to enhance both privacy and usability:

- **Spark Addresses:** This is a non-interactive addressing system that provides strong recipient privacy.10 A user can publicly post their Spark address without risk. When someone wants to send them funds, the sender's wallet uses the public Spark address to automatically generate a unique, one-time address on the recipient's behalf. This one-time address is what appears on the blockchain, but it is not searchable and cannot be linked back to the recipient's public Spark address by a third-party observer.10 This prevents an adversary from simply looking up a known public address to see a user's entire transaction history.
- **Full View Key Support:** Unlike Monero's original RingCT, which only supported incoming view keys, Spark provides both incoming and full (incoming and outgoing) view keys, allowing for more flexible and complete auditing capabilities for users who require them.10
- **Efficient Multisignature:** The protocol integrates a modified Chaum-Pedersen proof to enable efficient multisignature operations, a feature that is often complex to implement in other privacy protocols.14

The divergence between Monero's and Firo's next-generation protocols is not merely technical but philosophical. Monero's evolution toward FCMPs aims to create a single, massive, and uniform anonymity set where every transaction is private by default and indistinguishable from every other transaction on the network.5 This approach is designed to protect against metadata analysis that could reveal when a user chooses to seek privacy, because privacy is the mandatory, universal state. Firo's shielded pool model, by contrast, creates an explicit boundary between the transparent and private domains.11 While this may leak timing information when a user moves funds from a transparent address into a Spark address (an act known as "shielding"), once inside the private pool, the anonymity set is very large and static, making it less susceptible to the kind of heuristic attacks that target the decoy selection algorithms of ring-signature-based systems.15

For the cyberpunk operator, this presents a strategic choice based on the threat model. Monero is superior for a continuous stream of private transactions where the goal is to blend into a constant flow of anonymous activity. Firo may be the superior choice for a specific, high-value operation, such as receiving a payment from a transparent source (like an exchange withdrawal) and then definitively breaking all links to that source before the funds are used in the future.

The following table provides a strategic comparison of these two leading protocols.

| Feature                | Monero (Seraphis/FCMP++)                                                                | Firo (Lelantus Spark)                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Core Privacy Model** | Full-Chain Membership Proof (FCMP)                                                      | Shielded Pool (Burn-and-Redeem)                                                                        |
| **Anonymity Set**      | The entire blockchain history (potentially 100,000,000+ outputs) 5                      | The entire set of shielded coins (e.g., >65,000) 11                                                    |
| **Trusted Setup**      | No                                                                                      | No 14                                                                                                  |
| **Recipient Privacy**  | Jamtis addresses with view tags 8                                                       | Spark addresses (non-interactive, one-time) 10                                                         |
| **View Key Support**   | Multi-tiered (e.g., scanning-only, full view) 8                                         | Full incoming and outgoing view keys 10                                                                |
| **Multisig Support**   | Simple implementation, comparable to previous versions 6                                | Efficient, based on modified Chaum-Pedersen proofs 14                                                  |
| **Primary Advantage**  | Universal, mandatory privacy; massive anonymity set protects against metadata analysis. | Very large, static anonymity set; strong recipient privacy; no reliance on decoy selection heuristics. |
| **Primary Trade-off**  | Requires a complex, network-wide address migration.                                     | The act of "shielding" funds from a transparent address to a private one is a visible event.           |

### Chapter 2: Navigating the Regulatory Dragnet

The increasing sophistication of privacy-enhancing cryptocurrencies has triggered a direct and predictable response from state actors: a global regulatory campaign aimed at containing their use. This campaign, led by intergovernmental bodies like the Financial Action Task Force (FATF) and implemented through national and regional legislation like the European Union's Anti-Money Laundering Regulation (AMLR), is not designed to ban the technology outright. Instead, it follows a clear strategic doctrine: regulate the intermediaries. The goal is to build a compliant wall around the decentralized ecosystem, controlling the on-ramps and off-ramps where crypto intersects with the traditional fiat financial system.

#### The EU's AMLR Pincer Movement

The European Union's latest AML package, specifically Regulation (EU) 2024/1624, represents one of the most direct legislative assaults on privacy coins to date.17 Effective from July 10, 2027, the regulation explicitly prohibits Crypto-Asset Service Providers (CASPs)—a broad category that includes exchanges, custodial wallet providers, and other financial intermediaries—from offering any services related to coins with built-in anonymity or obfuscation features.17 The text of the regulation is unambiguous, stating that "it is necessary to prohibit the provision and custodial holding of anonymous crypto-asset accounts as well as accounts that allow the anonymization or enhanced obfuscation of transactions".17 This effectively mandates the delisting of assets like Monero and Firo from all regulated European exchanges and platforms.

However, the legislation contains a critical, strategic loophole. The prohibitions apply only to licensed intermediaries (the CASPs). The regulation explicitly clarifies that the rules do not apply to individual users, to the developers of hardware or software wallets, or to providers of self-hosted (non-custodial) wallets, on the grounds that these entities "have no control over these wallets".17 This distinction is the central pivot point for any effective counter-strategy. The state is not criminalizing the ownership or use of privacy coins; it is criminalizing the servicing of them by regulated businesses.

#### FATF Travel Rule & Its Limits

This "regulate the intermediary" doctrine is a direct implementation of the global standards set by the FATF. The FATF's Recommendation 16, commonly known as the "Travel Rule," requires VASPs (the FATF's term for CASPs) to obtain, hold, and transmit originator and beneficiary information for virtual asset transfers above a certain threshold (typically $1,000).22 The explicit goal is to make crypto transactions as transparent to law enforcement as traditional bank wire transfers.24

While straightforward to implement for transparent assets like Bitcoin moving between two compliant exchanges, the Travel Rule presents immense technical and conceptual challenges when applied to privacy coins and transactions involving self-custodial wallets.23 The FATF's own guidance acknowledges these difficulties. A transaction originating from a privacy coin wallet by definition obscures the originator's information. A transaction sent to a new, self-custodial address has no pre-existing "beneficiary" information for a VASP to collect. This creates a fundamental conflict between the architecture of privacy-preserving systems and the architecture of total financial surveillance demanded by the regulations.

#### Mitigation Strategy: The Sovereignty of Self-Custody

The convergence of these regulatory frameworks reveals a clear and consistent strategy by state actors. They are not attempting to shut down decentralized protocols, which is technically infeasible. Instead, they are building a highly regulated and surveilled perimeter around them. Inside this perimeter, on centralized exchanges and with licensed issuers, all activity must be transparent, identity-linked, and compliant. Outside the perimeter, in the world of peer-to-peer transactions and self-custodial wallets, the rules are largely unenforceable.

The primary countermeasure, therefore, is a disciplined and unwavering adherence to self-custody. By acquiring value through non-regulated or "gray-market" channels (detailed in Part IV) and securing that value in a self-sovereign cold storage setup (detailed in Part III), the operator can remain largely outside the direct jurisdiction of these control frameworks. The legal and operational risk is not in the holding or using of private assets, but is concentrated at the point of interface with the regulated financial system. Any attempt to convert a privacy coin into fiat currency via a regulated exchange will be blocked. This means that the cyberpunk's operational theater is necessarily outside the regulatory wall, and any crossing of that wall must be planned and executed with extreme caution to avoid direct contact with the chokepoints of control.

## Part II: The Programmable Panopticon — Countering Centralized Control

While privacy coins face containment through the regulation of intermediaries, another class of digital assets—stablecoins—is being actively co-opted and integrated into the state's financial surveillance apparatus. This section dissects the new regulatory frameworks designed to domesticate stablecoins and analyzes the existential threat posed by Central Bank Digital Currencies (CBDCs). The goal is to understand the architecture of this new programmable panopticon and to identify the tools and strategies necessary to resist it.

### Chapter 3: Deconstructing the Stablecoin Compliance Stack

Stablecoins, digital assets pegged to fiat currencies, have emerged as a critical piece of infrastructure for the crypto ecosystem. Recognizing their potential to bridge the gap between the traditional and decentralized financial worlds, state actors have moved decisively to bring them under control. The landmark legislation in this area is the U.S. Guiding and Establishing National Innovation for U.S. Stablecoins (GENIUS) Act, signed into law in July 2025.1

#### The GENIUS Act Deep Dive

The GENIUS Act's core function is to transform stablecoin issuers from unregulated tech companies into fully regulated financial institutions, subject to the same oversight and control as traditional banks.26 For the individual user seeking autonomy, several key provisions are of critical concern:

- **Issuer as "Financial Institution":** The Act designates all "permitted payment stablecoin issuers" as financial institutions for the purposes of the Bank Secrecy Act (BSA).26 This is not a minor technicality; it is a mandate for total surveillance. It legally obligates issuers to implement comprehensive Anti-Money Laundering (AML) and Know Your Customer (KYC) programs, effectively eliminating the possibility of anonymous or pseudonymous use of regulated stablecoins.
- **Technical Control Mandate:** The most direct threat to user autonomy is a provision that requires issuers to possess the technical capability to "seize, freeze, or burn" payment stablecoins in order to comply with lawful orders from government agencies.31 This codifies a universal backdoor at the protocol or issuer level, granting the state the power to censor transactions and confiscate assets without needing to compromise a user's private keys. It transforms a bearer asset into a permissioned liability.
- **Globalized Compliance:** The Act extends its reach globally by stipulating that foreign-issued stablecoins can only be offered to U.S. persons if the issuer registers with the Office of the Comptroller of the Currency (OCC) and is subject to a "comparable" regulatory regime in its home jurisdiction.30 This creates a strong incentive for other nations to adopt a similar surveillance-and-control framework, effectively exporting the U.S. model.

#### Countermeasures

Resisting the control grid established by the GENIUS Act requires a strategic shift away from centrally issued, fiat-backed stablecoins. The primary countermeasures involve leveraging more decentralized and censorship-resistant alternatives:

- **Decentralized Stablecoins:** The most robust alternative is the use of crypto-collateralized, decentralized stablecoins, with MakerDAO's DAI being the prime example. In this model, there is no central issuer that can be served with a court order. The "stablecoin" is minted by users who lock up other crypto assets (like ETH) as collateral in an autonomous smart contract. The stability of the system is maintained by algorithmic mechanisms and a decentralized governance process. While this model introduces a higher degree of smart contract risk, it eliminates the single point of failure and control inherent in the centralized issuer model.
- **Privacy Mixers and Shielded Pools:** For users who must interact with regulated stablecoins like USDC or USDT, the only way to break the on-chain link between their legal identity and their transaction activity is through the use of privacy-enhancing technologies. This can involve using decentralized mixing services to obfuscate the transaction graph. This is a high-risk tactic, as demonstrated by the U.S. Treasury's OFAC sanctioning of the Tornado Cash protocol, which effectively criminalized interaction with its smart contracts for U.S. persons. A more sustainable long-term solution lies in the use of Layer-2 protocols with built-in privacy, which allow users to transact with stablecoins inside a shielded pool, providing confidentiality from the public view of the base-layer blockchain.

### Chapter 4: The CBDC Gambit and the Sovereignty Defense

The logical endpoint of the state's desire for total financial visibility and control is the issuance of a retail Central Bank Digital Currency (CBDC). A CBDC is a direct liability of the central bank, a digital form of cash issued and controlled by the state.1 While proponents highlight potential benefits like payment efficiency, the architecture of a retail CBDC represents an unprecedented tool for surveillance and social engineering.

#### The Surveillance Architecture

Unlike physical cash, which is anonymous, a retail CBDC would, by design, create a permanent "digital trail" of every transaction.33 International Monetary Fund (IMF) reports on CBDC design openly acknowledge that the technology allows for the collection and storage of vast amounts of personal data, including transaction histories and behavioral patterns.33 This centralized ledger creates a single point of failure for privacy, making the entire financial history of a nation's citizens vulnerable to data leakage, abuse by the state for non-financial purposes, and cyberattacks.1 A CBDC that provides true cash-like anonymity is seen as fundamentally incompatible with modern AML/CFT regulations, meaning any implementation will necessarily involve a trade-off where privacy is sacrificed for state control.35

#### Programmable Money as Social Control

The most profound threat of a CBDC is its potential for programmability. As identified in the Wave 2 Threat Matrix, this feature would allow the state to embed policy rules directly into the currency itself.1 This could be used for overt social control, such as restricting the purchase of certain goods or services, or for more subtle forms of economic engineering, like setting expiration dates on stimulus funds to compel spending or automatically applying negative interest rates to encourage consumption.1 Money would cease to be a neutral medium of exchange and would become an active instrument of state policy enforcement, wielded directly against the individual citizen.

The regulatory framework being built for stablecoins under the GENIUS Act serves as a crucial stepping stone toward this future. The technical mandates for issuers to be able to seize, freeze, and burn assets are functionally identical to the control a central bank would have over a retail CBDC.31 Both systems create a financial environment where a central authority can permission, censor, and reverse transactions at will. The GENIUS Act is not merely a regulation; it is a pilot program for a CBDC-like control grid, implemented through private-sector proxies. It normalizes the concept of centrally-controlled digital dollars and builds the technical and legal precedent for a seamless transition to a full state-run CBDC. From the perspective of user autonomy, a GENIUS-compliant stablecoin and a retail CBDC represent the same fundamental threat, differing only in the name of the entity holding the kill switch.

#### The Sovereignty Defense

The only effective and durable defense against this programmable panopticon is to operate with assets that are architecturally immune to such control. Truly decentralized, base-layer cryptocurrencies like Bitcoin and Monero are the ultimate expression of this sovereignty. They are digital bearer assets. Their rules are not set by a board of directors or a central bank committee but are governed by immutable code and a globally distributed consensus mechanism. Their core value proposition is precisely their lack of programmability by any central authority. Holding and transacting in these assets is a practical rejection of the permissioned, surveilled financial system that CBDCs and regulated stablecoins are designed to create. It is the foundational act of financial self-defense.

## Part III: The Sovereign Vault — A Cookbook for Cold Storage

Theoretical understanding of decentralized assets is insufficient. True financial sovereignty requires the technical and procedural discipline to securely self-custody private keys. Entrusting keys to a third-party custodian (such as an exchange) negates the entire principle of decentralization and reintroduces the very counterparty risk that these systems were designed to eliminate. This section provides a practical, step-by-step guide to architecting a resilient, multi-layered cold storage system, moving from single-device security to robust multisignature configurations and fully air-gapped transaction workflows.

### Chapter 5: Hardware Wallet Threat Modeling

A hardware wallet is a specialized device designed to store private keys in an offline environment, allowing the user to sign transactions without exposing the keys to a potentially compromised online computer.36 However, not all hardware wallets are created equal. Selecting the right device requires a careful assessment of its security model against the operator's specific threat profile.

#### Comparative Analysis of Security Models (2025)

As of 2025, the market is dominated by a few key players, each with a distinct security philosophy 37:

- **Secure Element (SE):** This is a dedicated, tamper-resistant microcontroller (often with an EAL5+ or EAL6+ certification) designed to securely store cryptographic secrets and resist physical extraction attacks.37 Devices like the Ledger series, the Coldcard Mk4, and the Trezor Safe 3 use a Secure Element as the core of their physical security model. This provides strong protection against an adversary with physical access to the device.
- **Firmware Transparency:** The firmware is the software that runs on the hardware wallet itself. A critical distinction exists between closed-source and open-source firmware.
  - **Closed-Source (e.g., Ledger):** The firmware code is proprietary and not publicly available for inspection. This requires the user to place absolute trust in the manufacturer not to have included backdoors or vulnerabilities.39
  - **Open-Source (e.g., Trezor, Coldcard, BitBox02):** The firmware code is publicly available for anyone to audit and verify.36 This "trust but verify" model is strongly preferred from a security-first perspective, as it allows the community to discover and disclose vulnerabilities independently.
- **Air-Gap Functionality:** A true air-gap means the hardware wallet never makes a direct electronic connection (e.g., via USB) to an online computer.41 Instead, transaction data is transferred via an intermediary medium, typically a microSD card (for Partially Signed Bitcoin Transactions, or PSBTs) or QR codes. This eliminates a wide range of potential attack vectors that rely on a compromised USB connection. The Coldcard Mk4 is the gold standard for this type of operation.41

The choice of device involves a trade-off. An operator whose primary threat is a sophisticated remote software attack may prioritize open-source firmware and a fully air-gapped workflow above all else. An operator whose primary threat is physical seizure by a state adversary may prioritize a device with a robust Secure Element and advanced duress features (such as a PIN that opens a decoy wallet or a PIN that bricks the device).

The following table provides a comparative overview of the leading hardware wallets in 2025.

| Device        | Secure Element                              | Firmware Source  | Air-Gap Method      | Bitcoin-Only Option | Key Feature                               |
| ------------- | ------------------------------------------- | ---------------- | ------------------- | ------------------- | ----------------------------------------- |
| Coldcard Mk4  | Dual SE (from different vendors) 39         | Open-Source 41   | PSBT via microSD 44 | Yes (Default) 41    | Advanced duress PINs (decoy, brick) 39    |
| Trezor Safe 3 | EAL6+ Certified SE 37                       | Open-Source 42   | N/A (USB)           | No                  | Shamir Backup support 37                  |
| Ledger Flex   | EAL6+ Certified SE 38                       | Closed-Source 40 | N/A (USB/Bluetooth) | No                  | Large touchscreen, wireless capability 38 |
| BitBox02      | Dual-chip (Secure Element + general MCU) 36 | Open-Source 36   | N/A (USB)           | Yes                 | Instant microSD card backup 36            |

### Chapter 6: Architecting a Multisignature Bastion

While a single hardware wallet provides excellent security, it still represents a single point of failure. If the device is lost, stolen, or destroyed, and the backup seed phrase is compromised or inaccessible, the funds are gone forever. A multisignature (multisig) wallet is the solution. It requires M-of-N keys to authorize a transaction, providing robust protection against theft, loss, and even duress.45 For an individual operator, a 2-of-3 or 3-of-5 configuration is the gold standard for resilient self-custody.

#### The Multisig Protocol with Sparrow Wallet

Sparrow Wallet is a powerful, desktop-based Bitcoin wallet that provides advanced features, including robust support for multisignature and hardware wallet integration.47 The following protocol outlines the creation of a secure 2-of-3 multisig vault.

**Hardware Selection and Initialization:** Acquire three hardware wallets, ideally from three different vendors (e.g., one Coldcard, one Trezor, one BitBox02). This mitigates the risk of a single-vendor supply-chain attack or a systemic vulnerability in one manufacturer's firmware. Initialize each device separately according to its instructions, securely generating and backing up its unique 12- or 24-word seed phrase.

**Wallet Creation in Sparrow:**

1. Install and verify Sparrow Wallet on a secure, preferably dedicated, computer.47 For maximum security, connect Sparrow to your own Bitcoin node rather than a public server.
2. In Sparrow, select File > New Wallet. Give the wallet a name.
3. In the settings tab, change the Policy Type from Single Signature to Multi Signature. Set the quorum to 2-of-3.48

**Keystore Import:** You will now import the public key information (the xPub) from each of the three hardware wallets. This is done without ever exposing the private keys to the computer.

For each of the three keystore slots in Sparrow, select the appropriate import method. For air-gapped devices like a Coldcard, this will involve exporting the xPub file to a microSD card and importing that file into Sparrow. For USB-connected devices, Sparrow will communicate with the device to retrieve the xPub.48

**Finalize and Backup:** Once all three keystores have been imported, click Apply. Sparrow will generate the multisignature wallet. At this point, it is critically important to perform a wallet backup. Go to File > Export Wallet and save the wallet output descriptor file. This file contains the xPubs, derivation paths, and other metadata needed to reconstruct the entire multisignature setup on another machine or with different wallet software. It does not contain private keys but is essential for recovery.

**Secure Storage of Backups:** The operator now has four critical pieces of information to secure: the three seed phrases for the hardware wallets and the Sparrow wallet descriptor file. These must be stored with extreme care, following best practices 45:

- **Material:** Transcribe seed phrases onto durable, non-digital materials like steel plates to protect against fire and water damage.
- **Separation:** Store each backup component in a separate, secure, and geographically distinct location. For a 2-of-3 setup, one could store one seed at home, one in a bank safe deposit box, and one with a trusted family member or lawyer. The wallet descriptor file should be backed up in multiple locations as well.
- **Security:** Use tamper-evident bags to ensure backups have not been accessed. Never store any of these backups digitally (e.g., in cloud storage, email, or a password manager).

### Chapter 7: The Air-Gap Workflow — A PSBT Walkthrough

The most secure method for signing a transaction from a cold storage vault is a fully air-gapped workflow. This process leverages the Partially Signed Bitcoin Transaction (PSBT) standard (BIP 174) to move transaction data between an online "watch-only" wallet and an offline signing device without any direct electronic connection.43

#### Conceptual Framework: The Roles of PSBT

The PSBT standard defines a collaborative process with distinct roles 51:

- **Creator:** Proposes the transaction (inputs, outputs, amounts).
- **Updater:** Adds necessary information to the PSBT, such as the full details of the UTXOs being spent.
- **Signer:** Adds a valid cryptographic signature for one of the inputs.
- **Combiner:** Merges multiple partially signed PSBTs into one.
- **Finalizer:** Checks that all necessary signatures are present and adds the final script data to the transaction inputs.
- **Extractor:** Converts the finalized PSBT into a fully valid, network-ready raw transaction.

In a typical air-gapped workflow, the online watch-only wallet acts as the Creator, Updater, Finalizer, and Extractor, while the offline hardware wallet acts as the Signer.

#### The Protocol in Practice (Sparrow + Coldcard)

This walkthrough demonstrates signing a transaction from a single-signature air-gapped wallet. The process for a multisig wallet is similar but requires repeating the signing step with multiple offline devices.

**Transaction Creation (Online Watch-Only Wallet):**

1. On your online computer running Sparrow in watch-only mode (no private keys loaded), navigate to the Send tab.
2. Construct the transaction by entering the recipient's address, the amount, and the desired fee rate. Sparrow, acting as the Creator and Updater, assembles the transaction and fetches the necessary UTXO data from its connection to the blockchain node.
3. Instead of clicking Sign, click Finalize Transaction for Signing and then Save PSBT. Save the unsigned `.psbt` file to a microSD card.48

**Transaction Signing (Offline Hardware Wallet):**

1. Eject the microSD card from the online computer and insert it into the powered-on, air-gapped Coldcard wallet.
2. The Coldcard will automatically detect the PSBT file and display a "Ready to Sign" prompt. Select it.
3. The Coldcard, acting as the Signer, will now display the full transaction details—recipient address, amount, and fee—on its trusted screen. This is the most critical verification step. The PSBT format includes all the necessary UTXO information, allowing the offline device to independently verify the entire transaction without trusting the online computer.43
4. After carefully verifying the details, confirm the transaction on the device. The Coldcard will sign the transaction and save a new, partially-signed `.psbt` file to the microSD card (e.g., `...-part.psbt`).44

**Finalizing and Broadcasting (Online Watch-Only Wallet):**

1. Move the microSD card back to the online computer.
2. In Sparrow, go to File > Open Transaction and select the signed `.psbt` file from the microSD card.
3. Sparrow, now acting as the Finalizer and Extractor, will verify the signature and show that the transaction is fully signed.
4. Click the Broadcast Transaction button to send the finalized, valid transaction to the Bitcoin network.48

This workflow provides the highest level of security because the private keys never leave the offline device, and the device itself never connects to a potentially compromised machine. It moves the root of trust for transaction verification entirely to the physically secured hardware wallet, making "what you see is what you sign" a verifiable reality.

## Part IV: The Autonomous Engine — Generating and Automating Stability

Financial sovereignty requires not only the secure storage of value but also the means to acquire it and make it productive outside of traditional employment and banking structures. This section details strategies for generating income directly in crypto assets, navigating the corresponding tax compliance obligations, and deploying capital into decentralized finance (DeFi) protocols to create automated, passive income streams. The final chapter provides the code necessary to interact with these protocols directly, embodying the cyberpunk principle of "Technical Fluency" to achieve true autonomy.

### Chapter 8: Gray-Market Operations and Tax Compliance

The first step in building a parallel financial existence is to establish income streams that terminate directly in self-custodied crypto assets, bypassing the regulated fiat on-ramps that serve as the primary chokepoints for state surveillance. A growing ecosystem of platforms facilitates this direct value exchange.

#### Acquiring Value Beyond the Fiat Gateway

For a technically proficient operator, numerous opportunities exist to earn crypto directly for valuable skills:

- **Decentralized Freelancing:** Platforms like CryptoTask and LaborX connect freelancers directly with clients for peer-to-peer payment in crypto.54 These marketplaces often feature roles in high-demand niche areas like blockchain development, cybersecurity, and AI, and use smart contract-based escrow to ensure payment upon completion of work.
- **Bug and Development Bounties:** This is a direct path for programmers to earn significant crypto rewards.
  - **Security Bounties:** Platforms like Immunefi host bug bounty programs for major DeFi protocols, offering substantial rewards (often in the millions of dollars) for the responsible disclosure of critical vulnerabilities.57
  - **Open-Source Bounties:** Gitcoin is a platform that allows open-source projects to place bounties on specific GitHub issues, from simple bug fixes to complex feature development. It provides a direct way to contribute to and get paid by the open-source ecosystem.58
- **Skill Bartering:** Emerging decentralized platforms aim to facilitate direct peer-to-peer skill exchanges, often using reputation systems and token rewards to build a community of mutual learning and service exchange.60

#### A Pragmatic Guide to U.S. Tax Compliance

Operating outside traditional financial rails does not mean operating outside the law. Maintaining autonomy requires a disciplined approach to tax compliance to mitigate legal risk. In the United States, the Internal Revenue Service (IRS) treats digital assets as "property," not currency, which establishes a clear framework for taxation.62

- **The Income Event:** When you receive cryptocurrency as payment for services—whether from freelancing, completing a bounty, or staking rewards—it is considered ordinary income.62
- **Reporting:** This income must be reported. For an independent contractor, this is done on Schedule C (Form 1040), Profit or Loss from Business. For other income like staking rewards, it is reported on Schedule 1 (Form 1040), Additional Income.62
- **Valuation:** The amount of income to report is the Fair Market Value (FMV) of the cryptocurrency in U.S. dollars at the exact time of receipt.62 Meticulous record-keeping of the date, time, and USD value of every payment is non-negotiable.
- **Establishing Cost Basis:** This is the most critical step for future tax calculations. The FMV of the crypto at the time you received it as income becomes your cost basis for that asset.62 For example, if you complete a bounty and receive 1 ETH when the price of ETH is $3,000, you have $3,000 of ordinary income to report, and your cost basis for that 1 ETH is now $3,000.

#### The Capital Gains Event

A second, separate taxable event occurs when you later sell, trade, or spend that cryptocurrency.63

- **Calculation:** The capital gain or loss is calculated as: `(Proceeds from sale in USD) - (Cost Basis)`. Using the previous example, if you later sell that 1 ETH for $3,500, you have a capital gain of $3,500 - $3,000 = $500.
- **Reporting:** All capital gains and losses are reported on Form 8949, Sales and Other Dispositions of Capital Assets, and the totals are summarized on Schedule D (Form 1040).69
- **Holding Period:** The tax rate applied to the capital gain depends on how long you held the asset. If held for one year or less, it is a short-term capital gain and is taxed at your higher ordinary income tax rate. If held for more than one year, it is a long-term capital gain and is taxed at lower preferential rates (0%, 15%, or 20%).68

### Chapter 9: The DeFi Passive Income Stack

Once value has been acquired, it can be deployed into decentralized finance (DeFi) protocols to generate passive income streams. This is the process of putting capital to work within an autonomous, code-driven financial system. However, this potential for high yield comes with a unique set of risks that must be understood and managed.

#### Core Strategies for Yield Generation

Three primary strategies form the foundation of most DeFi yield generation:

- **Staking:** In Proof-of-Stake (PoS) networks like Ethereum, staking involves locking up the network's native token (ETH) to help secure the network and validate transactions. In return, stakers receive a share of network issuance and transaction fees as a reward. To avoid the complexity and capital requirements of running a full validator node, most users engage in liquid staking through protocols like Lido. Users deposit their ETH into the Lido smart contract and receive stETH in return. stETH is a liquid, tradable token that represents their staked ETH and automatically accrues staking rewards, while the underlying ETH is staked with a distributed set of professional node operators.71
- **Lending:** Decentralized lending protocols like Aave function as autonomous money markets. Users can supply assets (e.g., stablecoins like USDC, or volatile assets like ETH) to a lending pool and earn interest. This interest is paid by borrowers who take loans from the pool, posting other crypto assets as over-collateralized collateral. The interest rates are variable and are determined algorithmically based on the supply and demand (utilization rate) of each asset in the pool.71
- **Liquidity Provision (LP):** Decentralized exchanges (DEXs) like Uniswap use an Automated Market Maker (AMM) model instead of a traditional order book. To facilitate trading, they rely on "liquidity pools" containing pairs of assets (e.g., WETH and USDC). Users, known as Liquidity Providers (LPs), can deposit an equal value of both assets into a pool. In return, they earn a percentage of the trading fees generated every time another user swaps between those two assets.73 Uniswap v3 introduced "concentrated liquidity," allowing LPs to provide liquidity within a specific price range, potentially earning much higher fees but also increasing their risk exposure.

#### Risk Analysis: Code, Markets, and Systems

The promise of DeFi yield is predicated on a complex and often fragile technological stack. A pragmatic operator must be acutely aware of the inherent risks:

- **Smart Contract Risk:** This is the risk of a bug or vulnerability in a protocol's code that could be exploited by an attacker to drain funds. The history of DeFi is littered with catastrophic hacks resulting from common vulnerabilities like reentrancy attacks, access control failures, integer overflows, and business logic errors.75 Due diligence requires reviewing a protocol's security audits, but even audited contracts can be exploited.
- **Impermanent Loss (IL):** This risk is specific to liquidity providers in AMMs. IL is the opportunity cost that arises when the price of the assets in a liquidity pool diverges. If an LP withdraws their liquidity after a significant price change, the total value of their withdrawn assets can be less than if they had simply held the original assets in their wallet. It is the "impermanent" loss an LP suffers relative to just holding.79
- **Systemic and Oracle Risk:** The DeFi ecosystem is highly interconnected. The failure of one protocol can have cascading effects on others. The largest and most damaging hacks have often targeted the weakest points in this interconnected system: cross-chain bridges (which allow assets to move between blockchains) and price oracles (which provide external price data to smart contracts). The manipulation of a price oracle can trick a lending protocol into believing collateral is worth more than it is, allowing an attacker to drain the protocol by taking out under-collateralized loans.78

### Chapter 10: Code is Law — Automating Your Autonomy

The final step in achieving financial sovereignty is to move beyond reliance on third-party web interfaces and interact with DeFi protocols directly through code. A web front-end is a potential point of failure; it can be censored, compromised to serve malicious code, or used to log user IP addresses and transaction data. Direct interaction via a library like Python's web3.py provides superior security, control, and the potential for automation. This is the ultimate expression of the "Technical Fluency" mindset: understanding and wielding the protocol at its most fundamental level.1

#### Environment Setup

To begin, the operator must set up a Python environment and install the web3.py library. Connection to the Ethereum blockchain requires access to a node. While running a local node provides maximum privacy, a simpler starting point is to use a node service provider like Infura.

```bash
# Create and activate a Python virtual environment
python3 -m venv web3-env
source web3-env/bin/activate

# Install the web3.py library
pip install web3
```

The following code snippets demonstrate foundational interactions with key DeFi protocols. They require the user to provide their Ethereum account address, private key, and an Infura Project ID. Note: In a real-world application, private keys should never be hard-coded. They should be stored securely using environment variables or a dedicated secrets management tool.

#### Code Snippet 1: Staking ETH with Lido using web3.py

```python
import json
from web3 import Web3

# --- Configuration ---
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
my_address = "YOUR_ETHEREUM_ADDRESS"
private_key = "YOUR_PRIVATE_KEY"  # WARNING: For demonstration only. Use secure key management.

# Lido stETH Contract Address and a minimal ABI
LIDO_CONTRACT_ADDRESS = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
LIDO_ABI = json.loads('[{"constant":false,"inputs":,"name":"submit","outputs":[{"name":"","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"}]')

# Amount of ETH to stake (in Ether)
eth_to_stake = 0.1

# --- Connection and Contract Setup ---
w3 = Web3(Web3.HTTPProvider(infura_url))
if not w3.is_connected():
    print("Error: Could not connect to Ethereum node.")
    exit()

lido_contract = w3.eth.contract(address=LIDO_CONTRACT_ADDRESS, abi=LIDO_ABI)

# --- Transaction Creation ---
print(f"Preparing to stake {eth_to_stake} ETH with Lido...")

# Convert ETH amount to Wei
amount_in_wei = w3.to_wei(eth_to_stake, 'ether')

# Build the transaction
transaction = lido_contract.functions.submit().build_transaction({
    'from': my_address,
    'value': amount_in_wei,
    'gas': 250000,  # Gas limit can be estimated more accurately
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(my_address),
    'chainId': 1 # Mainnet
})

# --- Signing and Sending ---
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(f"Transaction sent with hash: {w3.to_hex(tx_hash)}")
print("Waiting for transaction receipt...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction successful!")
print(f"View on Etherscan: https://etherscan.io/tx/{w3.to_hex(tx_hash)}")
```

#### Code Snippet 2: Supplying USDC to Aave v3 using web3.py

```python
import json
from web3 import Web3

# --- Configuration ---
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
my_address = "YOUR_ETHEREUM_ADDRESS"
private_key = "YOUR_PRIVATE_KEY" # WARNING: For demonstration only.

# Contract Addresses (Ethereum Mainnet)
AAVE_POOL_ADDRESS = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

# Minimal ABIs
AAVE_POOL_ABI = json.loads(',"name":"supply","outputs":,"stateMutability":"nonpayable","type":"function"}]')
ERC20_ABI = json.loads('[{"constant":true,"inputs":,"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":,"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')

# Amount of USDC to supply (note: USDC has 6 decimal places)
usdc_to_supply = 100
amount_in_smallest_unit = usdc_to_supply * (10**6)

# --- Connection and Contract Setup ---
w3 = Web3(Web3.HTTPProvider(infura_url))
aave_pool_contract = w3.eth.contract(address=AAVE_POOL_ADDRESS, abi=AAVE_POOL_ABI)
usdc_contract = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)

# --- Step 1: Approve Aave to spend USDC ---
print("Step 1: Approving Aave Pool to spend USDC...")
approve_txn = usdc_contract.functions.approve(AAVE_POOL_ADDRESS, amount_in_smallest_unit).build_transaction({
    'from': my_address,
    'gas': 100000,
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(my_address),
    'chainId': 1
})

signed_approve_txn = w3.eth.account.sign_transaction(approve_txn, private_key=private_key)
approve_tx_hash = w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
print(f"Approval transaction sent: {w3.to_hex(approve_tx_hash)}")
w3.eth.wait_for_transaction_receipt(approve_tx_hash)
print("Approval successful!")

# --- Step 2: Supply USDC to Aave Pool ---
print(f"\nStep 2: Supplying {usdc_to_supply} USDC to Aave...")
supply_txn = aave_pool_contract.functions.supply(USDC_ADDRESS, amount_in_smallest_unit, my_address, 0).build_transaction({
    'from': my_address,
    'gas': 300000,
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(my_address), # Nonce must be incremented from the approval tx
    'chainId': 1
})

signed_supply_txn = w3.eth.account.sign_transaction(supply_txn, private_key=private_key)
supply_tx_hash = w3.eth.send_raw_transaction(signed_supply_txn.rawTransaction)
print(f"Supply transaction sent: {w3.to_hex(supply_tx_hash)}")
w3.eth.wait_for_transaction_receipt(supply_tx_hash)
print("Supply successful!")
print(f"View on Etherscan: https://etherscan.io/tx/{w3.to_hex(supply_tx_hash)}")
```

#### Code Snippet 3: Querying a Uniswap v3 Pool with web3.py

```python
import json
from web3 import Web3

# --- Configuration ---
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"

# Contract Addresses (Ethereum Mainnet)
UNISWAP_V3_FACTORY_ADDRESS = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

# Minimal ABIs
FACTORY_ABI = json.loads(',"name":"getPool","outputs":,"stateMutability":"view","type":"function"}]')
POOL_ABI = json.loads('[{"inputs":,"name":"slot0","outputs":,"stateMutability":"view","type":"function"}]')

# Pool fee tier (e.g., 0.05% = 500)
FEE_TIER = 500

# --- Connection and Contract Setup ---
w3 = Web3(Web3.HTTPProvider(infura_url))
factory_contract = w3.eth.contract(address=UNISWAP_V3_FACTORY_ADDRESS, abi=FACTORY_ABI)

# --- Querying the Pool ---
print("Finding WETH/USDC 0.05% pool address...")
pool_address = factory_contract.functions.getPool(WETH_ADDRESS, USDC_ADDRESS, FEE_TIER).call()

if pool_address == "0x0000000000000000000000000000000000000000":
    print("Pool not found.")
else:
    print(f"Pool Address: {pool_address}")
    pool_contract = w3.eth.contract(address=pool_address, abi=POOL_ABI)

    # Read the 'slot0' storage slot of the pool
    slot0 = pool_contract.functions.slot0().call()
    current_tick = slot0

    # The price of token0 in terms of token1 is 1.0001^tick
    # For WETH/USDC, price of WETH in USDC is 1.0001^tick / 10^(18-6)
    price = (1.0001 ** current_tick) / (10**12)

    print(f"Current Tick: {current_tick}")
    print(f"Approximate Price of WETH in USDC: ${price:.2f}")
```

### Works cited — Wave 4

Cyberpunk Threat and Power Analysis
MONERO [XMR] REPORT - Scaling New Heights in Blockchain Performance: 2025 Portfolio / Part Two, accessed July 25, 2025, https://www.thestandard.io/blog/monero-xmr-report---scaling-new-heights-in-blockchain-performance-2025-portfolio-part-two-6
Developer Opportunities at the Monero Project, accessed July 25, 2025, https://www.getmonero.org/it/2023/02/02/seraphis-jamtis-developer-opportunities.html
Developer Opportunities at the Monero Project, accessed July 25, 2025, https://www.getmonero.org/tr/2023/02/02/seraphis-jamtis-developer-opportunities.html
Full-Chain Membership Proofs Development | Monero - secure, private, untraceable, accessed July 25, 2025, https://www.getmonero.org/2024/04/27/fcmps.html
What is Seraphis, and Why Should You Care? | Monero - secure, private, untraceable, accessed July 25, 2025, https://www.getmonero.org/2021/12/22/what-is-seraphis.html
Seraphis: A Privacy-Preserving Transaction Protocol Abstraction (WIP) - GitHub, accessed July 25, 2025, https://raw.githubusercontent.com/UkoeHB/Seraphis/master/seraphis/Seraphis-0-0-18.pdf
jamtis.md - GitHub Gist, accessed July 25, 2025, https://gist.github.com/tevador/50160d160d24cfc6c52ae02eb3d17024
Seraphis/Jamtis - GitHub, accessed July 25, 2025, https://raw.githubusercontent.com/MoneroKon/meta/main/slides/2022/j-berman.pdf
Firo Announces New Privacy Protocol Lelantus Spark | The Fintech Times, accessed July 25, 2025, https://thefintechtimes.com/firo-announces-new-privacy-protocol-lelantus-spark/
What is Firo? All You Need to Know About FIRO - Gate.io, accessed July 25, 2025, https://www.gate.com/learn/articles/-what-is-motorverse-all-you-need-to-know-about-revv/2906
Cryptocurrency Privacy Technologies: Lelantus Protocol - Ventral Digital, accessed July 25, 2025, https://ventral.digital/posts/2024/3/25/cryptocurrency-privacy-technologies-lelantus/
Firo: Pioneering Privacy in Blockchain Technology | NOWNodes Blog, accessed July 25, 2025, https://nownodes.io/blog/firo-blockchain-privacy-lelantus-spark/
Firo Reveals Lelantus Spark: Its New Flexible Privacy Protocol - Bitcoin.com News, accessed July 25, 2025, https://news.bitcoin.com/firo-reveals-lelantus-spark-its-new-flexible-privacy-protocol/
FIRO Coin and Its Lelantus Spark Privacy Protocol - CryptoPotato, accessed July 25, 2025, https://cryptopotato.com/firo-coin-and-its-lelantus-spark-privacy-protocol/
Lelantus Spark is live on Firo | Firo - Privacy-preserving cryptocurrency - FIRO.org, accessed July 25, 2025, https://firo.org/2024/01/18/spark-is-live.html
EU: EU to Ban Trading of Privacy Coins from 2027 | I... - IFC Review, accessed July 25, 2025, https://www.ifcreview.com/news/2025/may/eu-eu-to-ban-trading-of-privacy-coins-from-2027/
L_202401624EN.000101.fmx.xml - EUR-Lex, accessed July 25, 2025, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1624
New EU regulation to track crypto transfers and ban privacy coins, accessed July 25, 2025, https://dig.watch/updates/new-eu-regulation-to-track-crypto-transfers-and-ban-privacy-coins
New EU regulation to track crypto transfers and ban privacy coins, accessed July 25, 2025, https://v45.diplomacy.edu/updates/new-eu-regulation-to-track-crypto-transfers-and-ban-privacy-coins
The Death of Privacy in Crypto: EU's 2027 Ban Raises Existential Questions - Shyft Network, accessed July 25, 2025, https://shyftnetwork.medium.com/the-death-of-privacy-in-crypto-eus-2027-ban-raises-existential-questions-9e85b5f1123f
Updated Guidance for a Risk-Based Approach to Virtual Assets and Virtual Asset Service Providers - FATF, accessed July 25, 2025, https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html
Financial Action Task Force (FATF) Travel Rule - Sanction Scanner, accessed July 25, 2025, https://www.sanctionscanner.com/blog/financial-action-task-force-fatf-travel-rule-140
EU passes landmark crypto regulation, MiCA, in lock step after cementing decried, dreaded virtual value AML 'travel rule', accessed July 25, 2025, https://www.acfcs.org/eu-passes-landmark-crypto-regulation
Virtual Assets - FATF, accessed July 25, 2025, https://www.fatf-gafi.org/en/topics/virtual-assets.html
The GENIUS Act of 2025 Stablecoin Legislation Adopted in the US - Latham & Watkins LLP, accessed July 25, 2025, https://www.lw.com/en/insights/the-genius-act-of-2025-stablecoin-legislation-adopted-in-the-us
Donald Trump's Genius Act: Major crypto bill for stablecoins passed in US; here is what to know, accessed July 25, 2025, https://timesofindia.indiatimes.com/business/international-business/donald-trumps-genius-act-major-crypto-bill-for-stablecoins-passed-in-us-here-is-what-to-know/articleshow/122776414.cms
Real GENIUS: Landmark U.S. Federal Payment Stablecoin Legislation | Winston & Strawn, accessed July 25, 2025, https://www.winston.com/en/blogs-and-podcasts/non-fungible-insights-blockchain-decrypted/real-genius-landmark-us-federal-payment-stablecoin-legislation
Building a Digital Asset Regulatory Framework: The GENIUS Act and Next Steps, accessed July 25, 2025, https://www.wiley.law/alert-Building-a-Digital-Asset-Regulatory-Framework-The-GENIUS-Act-and-Next-Steps
The GENIUS Act: A New Era of Stablecoin Regulation - Gibson Dunn, accessed July 25, 2025, https://www.gibsondunn.com/the-genius-act-a-new-era-of-stablecoin-regulation/
Fact Sheet: President Donald J. Trump Signs GENIUS Act into Law - The White House, accessed July 25, 2025, https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-president-donald-j-trump-signs-genius-act-into-law/
US Establishes First Federal Regulatory Framework for Stablecoins: The GENIUS Act Passes Congress and Awaits President Trump's Signature | Skadden, Arps, Slate, Meagher & Flom LLP, accessed July 25, 2025, https://www.skadden.com/insights/publications/2025/07/us-establishes-first-federal-regulatory-framework
Central Bank Digital Currency Data Use and Privacy Protection in - IMF eLibrary, accessed July 25, 2025, https://www.elibrary.imf.org/view/journals/063/2024/004/article-A001-en.xml
Central Bank Digital Currency Tracker - Atlantic Council, accessed July 25, 2025, https://www.atlanticcouncil.org/cbdctracker/
Central Bank Digital Currencies - Congress.gov, accessed July 25, 2025, https://www.congress.gov/crs_external_products/IF/PDF/IF11471/IF11471.4.pdf
Hardware wallet comparison 2025: Ledger, Trezor, BitBox, accessed July 25, 2025, https://bitbox.swiss/bitbox02/compare-hardware-wallets/
Best Crypto Hardware Wallets for 2025: Reviews & Top Picks, accessed July 25, 2025, https://cointelegraph.com/learn/articles/best-crypto-hardware-wallets
The 5 Best Hardware Wallets [2025] - Ledger, Trezor, Tangem and, accessed July 25, 2025, https://www.hardwarewalletonline.com/top-5-hardware-wallets-2025/

- COLDCARD Mk4 review | Is it safe? | Finder.com, accessed July 25, 2025, https://www.finder.com/cryptocurrency/wallets/coldcard-mk4-review
- Top 9 Cryptocurrency Hardware Wallets for 2025 | Security Researcher Review, accessed July 25, 2025, https://patrickalphac.medium.com/top-9-cryptocurrency-hardware-wallets-for-2025-security-researcher-review-9fcb16d771e0
- Coldcard Mk4 Review: 3 Things to Know [2024] - Buy Bitcoin Worldwide, accessed July 25, 2025, https://buybitcoinworldwide.com/wallets/coldcard/
- Trezor Model T Review - Best Hardware Wallets - Cryptotesters.com, accessed July 25, 2025, https://cryptotesters.com/best-hardware-wallets/trezor-model-t-review
- Bitcoin Air-Gapped Wallets: What Are They and How Do They Work - Lightspark, accessed July 25, 2025, https://www.lightspark.com/glossary/air-gapped-wallet
- ColdCard Wallet Review 2025 - CryptoVantage, accessed July 25, 2025, https://www.cryptovantage.com/best-crypto-wallets/coldcard/
- Using Multisig Wallets to Secure Your Crypto Assets | BitPay, accessed July 25, 2025, https://www.bitpay.com/blog/multisig-wallet-security
- Mastering the Multisig Wallet: Your Guide to Enhanced Security - OneSafe Blog, accessed July 25, 2025, https://www.onesafe.io/blog/multisig-wallets-guide-benefits-challenges-best-practices
- Quick Start Guide - Sparrow Wallet, accessed July 25, 2025, https://sparrowwallet.com/docs/quick-start.html
- Sparrow Wallet - Bitcoiner.Guide, accessed July 25, 2025, https://bitcoiner.guide/sparrow/
- Sparrow Wallet - Multisig.Guide, accessed July 25, 2025, https://bitcoiner.guide/multisig/recover/
- 10 Steps to Set Up a Multi-Signature Wallet - Krayon, accessed July 25, 2025, https://www.krayondigital.com/blog/10-steps-to-set-up-a-multi-signature-wallet
- 7.1: Creating a Partially Signed Bitcoin Transaction - GitHub, accessed July 25, 2025, https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line/blob/master/07_1_Creating_a_Partially_Signed_Bitcoin_Transaction.md
- BIP 0174 - Bitcoin Wiki, accessed July 25, 2025, https://en.bitcoin.it/wiki/BIP_0174
- Electrum 2/2 PSBT Multi-sig - Keystone Support, accessed July 25, 2025, https://support.keyst.one/3rd-party-wallets/bitcoin-wallets/electrum/electrum-2-2-psbt-multi-signature
- Decentralized freelancing marketplace - CryptoTask, accessed July 25, 2025, https://www.cryptotask.org/
- 8 Freelance Websites that Pay in Crypto - Fuspay, accessed July 25, 2025, https://fuspay.us/freelance-websites-that-pay-in-crypto/
- Freelance Crypto Platforms: Pay & Get Paid in Cryptocurrency - Tangem, accessed July 25, 2025, https://tangem.com/en/blog/post/cryptocurrency-platforms-for-freelance-work/
- Crypto Bug Bounties: How to Get Started - Coinmetro, accessed July 25, 2025, https://www.coinmetro.com/learning-lab/crypto-bug-bounties-how-to-get-started
- Everything You Need to Know About Gitcoin, accessed July 25, 2025, https://www.gitcoin.co/blog/everything-you-need-to-know-about-gitcoin
- Integrating Standard Bounties | Gitcoin Blog, accessed July 25, 2025, https://www.gitcoin.co/blog/integrating-standard-bounties
- SkillSwap – App to exchange knowledge, accessed July 25, 2025, http://skill-swap.com/
- SkillSwap - HackQuest, accessed July 25, 2025, https://www.hackquest.io/projects/skillswap-5a48f85c
- Digital assets | Internal Revenue Service, accessed July 25, 2025, https://www.irs.gov/filing/digital-assets
- How Is Crypto Taxed? (2025) IRS Rules and How to File | Gordon Law Group, accessed July 25, 2025, https://gordonlaw.com/learn/crypto-taxes-how-to-report/
- Taxpayers need to report crypto, other digital asset transactions on their tax return - IRS, accessed July 25, 2025, https://www.irs.gov/newsroom/taxpayers-need-to-report-crypto-other-digital-asset-transactions-on-their-tax-return
- Your Crypto Tax Guide - TurboTax - Intuit, accessed July 25, 2025, https://turbotax.intuit.com/tax-tips/investments-and-taxes/your-cryptocurrency-tax-guide/L4k3xiFjB
- Crypto Taxes USA: Expert Guide for 2025 [IRS Rules] - CoinTracking, accessed July 25, 2025, https://cointracking.info/crypto-taxes-us
- Crypto Cost Basis: Easy Guide to Methods and Calculations 2025 | Gordon Law Group, accessed July 25, 2025, https://gordonlaw.com/learn/crypto-cost-basis/
- How to Calculate Crypto Capital Gains Tax in 2025 (from a CPA) | Gordon Law Group, accessed July 25, 2025, https://gordonlaw.com/crypto-capital-gains-tax/
- Crypto tax guide - Fidelity Investments, accessed July 25, 2025, https://www.fidelity.com/learning-center/trading-investing/crypto/crypto-tax-guide
- Ultimate 2025 US Crypto Tax Guide [IRS Rules] - Blockpit, accessed July 25, 2025, https://www.blockpit.io/tax-guides/crypto-tax-usa
- Passive Income in Crypto: A Guide to Staking, Lending, and Yield ..., accessed July 25, 2025, https://www.coinmetro.com/learning-lab/passive-income-in-crypto
- Stake with Lido | Lido, accessed July 25, 2025, https://stake.lido.fi/
- How to get started in DeFi - Coinbase, accessed July 25, 2025, https://www.coinbase.com/learn/wallet/how-to-get-started-in-defi
- Understanding DeFi Yield Farming: Comprehensive Guide for Beginners - Antier Solutions, accessed July 25, 2025, https://www.antiersolutions.com/blogs/understanding-defi-yield-farming-a-comprehensive-beginners-guide-to-earning-passive-income/
- OWASP Smart Contract Top 10, accessed July 25, 2025, https://owasp.org/www-project-smart-contract-top-10/

### References

[^1]: See the previous waves for context on Radical Autonomy and the Threat Matrix.
