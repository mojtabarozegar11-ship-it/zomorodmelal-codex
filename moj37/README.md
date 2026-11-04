# MOJ37 — BNB Smart Chain fixed-supply token

- Name: Moj 37; Symbol: MOJ37; Decimals: 18
- Supply: **1,000,000,000,000** MOJ37 fixed, minted once at construction.
- Intended initial recipient: `0x89149b01f59115B86553561F12438D2ADF517E75`
- Solidity: `0.8.26`, OpenZeppelin Contracts: `v5.4.0`, optimizer 200, Paris EVM.
- This repository contains **source and tests only**. It does not include signing keys or deployed contracts.
- **No mainnet transaction, BNB payment, or blockchain deployment is authorized by this CI.**

To run locally (no keys or blockchain needed):
```bash
cd moj37
git clone --depth 1 --branch v5.4.0 https://github.com/OpenZeppelin/openzeppelin-contracts.git lib/openzeppelin-contracts
forge test -vvv
forge build --sizes
```

The same commands run automatically on the isolated audit branch under GitHub Actions.
Deployment must be separately confirmed by the wallet owner; the public address alone cannot sign transactions.
