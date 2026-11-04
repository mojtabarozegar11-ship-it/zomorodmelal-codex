// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {MOJ37} from "../src/MOJ37.sol";

contract TestSpender {
    function spend(MOJ37 token, address holder, address recipient, uint256 amount) external {
        require(token.transferFrom(holder, recipient, amount), "transferFrom false");
    }
}

contract MOJ37Test {
    MOJ37 internal token;
    address internal constant RECIPIENT = address(0xBEEF);
    uint256 internal constant SUPPLY = 1_000_000_000_000 * 10 ** 18;

    constructor() {
        token = new MOJ37(address(this));
    }

    function testMetadata() public view {
        require(keccak256(bytes(token.name())) == keccak256(bytes("Moj 37")), "name");
        require(keccak256(bytes(token.symbol())) == keccak256(bytes("MOJ37")), "symbol");
        require(token.decimals() == 18, "decimals");
    }

    function testInitialSupplyOnlyToHolder() public view {
        require(token.totalSupply() == SUPPLY, "supply");
        require(token.balanceOf(address(this)) == SUPPLY, "holder amount");
        require(token.balanceOf(RECIPIENT) == 0, "recipient unexpectedly funded");
    }

    function testDirectTransferPreservesSupply() public {
        uint256 amount = 7 * 10 ** 18;
        require(token.transfer(RECIPIENT, amount), "transfer");
        require(token.balanceOf(RECIPIENT) == amount, "receiver");
        require(token.balanceOf(address(this)) == SUPPLY - amount, "sender");
        require(token.totalSupply() == SUPPLY, "supply increased/decreased");
    }

    function testApproveAndTransferFrom() public {
        TestSpender spender = new TestSpender();
        uint256 approved = 10 * 10 ** 18;
        require(token.approve(address(spender), approved), "approve");
        spender.spend(token, address(this), RECIPIENT, 4 * 10 ** 18);
        require(token.balanceOf(RECIPIENT) == 4 * 10 ** 18, "recipient balance");
        require(token.allowance(address(this), address(spender)) == 6 * 10 ** 18, "allowance mismatch");
        require(token.totalSupply() == SUPPLY, "supply mismatch");
    }

    function testUnapprovedTransferFromReverts() public {
        TestSpender spender = new TestSpender();
        (bool success,) = address(spender).call(
            abi.encodeWithSelector(TestSpender.spend.selector, token, address(this), RECIPIENT, 1)
        );
        require(!success, "unapproved spending succeeded");
    }

    function testTransferMoreThanBalanceReverts() public {
        (bool success,) = address(token).call(
            abi.encodeWithSelector(token.transfer.selector, RECIPIENT, SUPPLY + 1)
        );
        require(!success, "overdraft succeeded");
    }

    function testTransferToZeroReverts() public {
        (bool success,) = address(token).call(
            abi.encodeWithSelector(token.transfer.selector, address(0), 1)
        );
        require(!success, "zero transfer succeeded");
    }

    function testZeroHolderConstructorReverts() public {
        bool deployed;
        try new MOJ37(address(0)) returns (MOJ37) { deployed = true; }
        catch { deployed = false; }
        require(!deployed, "zero initial holder accepted");
    }

    function testNoAdministrativeEntrypoints() public {
        (bool mintOK,) = address(token).call(abi.encodeWithSignature("mint(address,uint256)", address(this), 1));
        (bool pauseOK,) = address(token).call(abi.encodeWithSignature("pause()"));
        (bool blackOK,) = address(token).call(abi.encodeWithSignature("blacklist(address)", RECIPIENT));
        (bool upgradeOK,) = address(token).call(abi.encodeWithSignature("upgradeTo(address)", RECIPIENT));
        require(!mintOK && !pauseOK && !blackOK && !upgradeOK, "privileged function accessible");
        require(token.totalSupply() == SUPPLY, "supply changed");
    }

    function testFuzzTransferPreservesSupply(uint128 rawAmount) public {
        uint256 amount = uint256(rawAmount) % (SUPPLY + 1);
        require(token.transfer(RECIPIENT, amount), "transfer false");
        require(token.balanceOf(RECIPIENT) == amount, "receiver mismatch");
        require(token.balanceOf(address(this)) + token.balanceOf(RECIPIENT) == SUPPLY, "conservation failure");
        require(token.totalSupply() == SUPPLY, "supply failure");
    }

    function testFuzzAllowance(uint128 rawAmount) public {
        uint256 amount = uint256(rawAmount) % (SUPPLY + 1);
        TestSpender spender = new TestSpender();
        require(token.approve(address(spender), amount), "approve false");
        spender.spend(token, address(this), RECIPIENT, amount);
        require(token.allowance(address(this), address(spender)) == 0, "allowance not depleted");
        require(token.balanceOf(RECIPIENT) == amount, "balance mismatch");
        require(token.totalSupply() == SUPPLY, "supply changed");
    }

    function testFullSupplyCanTransfer() public {
        require(token.transfer(RECIPIENT, SUPPLY), "entire supply transfer false");
        require(token.balanceOf(address(this)) == 0, "remaining balance");
        require(token.balanceOf(RECIPIENT) == SUPPLY, "full recipient");
        require(token.totalSupply() == SUPPLY, "total changed");
    }
}
