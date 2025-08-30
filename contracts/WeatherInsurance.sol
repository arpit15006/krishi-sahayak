// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WeatherInsurance {
    struct Policy {
        bool active;
        uint256 premium;
        uint256 payout;
        uint256 pincode;
        uint256 startTime;
    }
    
    mapping(address => Policy) public policies;
    address public owner;
    
    event PolicyPurchased(address farmer, uint256 pincode, uint256 premium);
    event PayoutTriggered(address farmer, uint256 amount, string reason);
    
    constructor() {
        owner = msg.sender;
    }
    
    function buyPolicy(uint256 _pincode) external payable {
        require(msg.value >= 0.001 ether, "Minimum premium required");
        
        policies[msg.sender] = Policy({
            active: true,
            premium: msg.value,
            payout: msg.value * 10, // 10x payout
            pincode: _pincode,
            startTime: block.timestamp
        });
        
        emit PolicyPurchased(msg.sender, _pincode, msg.value);
    }
    
    function triggerPayout(address farmer, string memory reason) external {
        require(msg.sender == owner, "Only owner can trigger");
        Policy storage policy = policies[farmer];
        require(policy.active, "No active policy");
        
        uint256 amount = policy.payout;
        policy.active = false;
        
        payable(farmer).transfer(amount);
        emit PayoutTriggered(farmer, amount, reason);
    }
    
    function simulateExtremeWeather(string memory eventType) external {
        Policy storage policy = policies[msg.sender];
        require(policy.active, "No active policy");
        
        uint256 amount = policy.payout;
        policy.active = false;
        
        payable(msg.sender).transfer(amount);
        emit PayoutTriggered(msg.sender, amount, eventType);
    }
}