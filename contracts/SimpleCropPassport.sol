// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleCropPassport {
    struct Passport {
        string cropType;
        string season;
        string ipfsHash;
        address farmer;
        uint256 timestamp;
    }
    
    mapping(uint256 => Passport) public passports;
    uint256 public nextTokenId = 1;
    
    event PassportCreated(uint256 tokenId, address farmer, string cropType, string ipfsHash);
    
    function createPassport(string memory cropType, string memory season, string memory ipfsHash) external returns (uint256) {
        uint256 tokenId = nextTokenId++;
        
        passports[tokenId] = Passport({
            cropType: cropType,
            season: season,
            ipfsHash: ipfsHash,
            farmer: msg.sender,
            timestamp: block.timestamp
        });
        
        emit PassportCreated(tokenId, msg.sender, cropType, ipfsHash);
        return tokenId;
    }
    
    function getPassport(uint256 tokenId) external view returns (string memory, string memory, string memory, address, uint256) {
        Passport memory p = passports[tokenId];
        return (p.cropType, p.season, p.ipfsHash, p.farmer, p.timestamp);
    }
}