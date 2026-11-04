// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title MOJ37 — fixed-supply ERC20 token for BNB Smart Chain
/// @notice All tokens are minted once to the constructor-provided holder.
/// @dev No privileged owner, mint, pause, blacklist, upgrade or transfer tax.
contract MOJ37 is ERC20 {
    uint256 public constant INITIAL_SUPPLY = 1_000_000_000_000 * 10 ** 18;

    constructor(address initialHolder) ERC20("Moj 37", "MOJ37") {
        _mint(initialHolder, INITIAL_SUPPLY);
    }
}
