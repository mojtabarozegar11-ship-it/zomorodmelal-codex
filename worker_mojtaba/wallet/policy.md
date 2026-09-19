# Revenue Wallet Policy

This is the owner-defined revenue routing policy for Worker Mojtaba.

- Wallet 1 receives **10% of total revenue** and may use that allocation only within its granted operational permissions.
- Wallet 2 receives **90% of total revenue**.
- Wallet 2 is **deposit-only**.
- Wallet 2 has **no withdrawal permission**.
- Wallet 2 has **no outbound transfer permission**.
- The worker may initiate deposits to Wallet 2, but must never create or execute a withdrawal/outbound-transfer path for Wallet 2.
- Private keys, seed phrases, passwords, and signing secrets must not be stored in source code or ordinary memory.

Example: 100 revenue units -> 10 units to Wallet 1 and 90 units to Wallet 2.
