// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title MOJ37 - fixed supply token for BNB Smart Chain
/// @notice All tokens are created once and assigned to initialHolder at deployment.
/// @dev No owner, privileged roles, minting, tax, blacklist, pause, or upgrade hooks.
contract MOJ37 is ERC20 {
    uint256 public constant INITIAL_SUPPLY = 1_000_000_000_000 * 10 ** 18;

    constructor(address initialHolder) ERC20("Moj 37", "MOJ37") {
        _mint(initialHolder, INITIAL_SUPPLY);
    }
}
