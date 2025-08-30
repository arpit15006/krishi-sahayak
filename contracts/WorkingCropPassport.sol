// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract WorkingCropPassport {
    struct Passport {
        string cropType;
        string season;
        string ipfsHash;
        address farmer;
        uint256 timestamp;
        bool verified;
        string location;
        uint256 area;
    }
    
    mapping(uint256 => Passport) public passports;
    mapping(address => uint256[]) public farmerPassports;
    
    uint256 private _tokenIdCounter;
    address public owner;
    
    event PassportCreated(uint256 indexed tokenId, address indexed farmer, string cropType, string season);
    
    constructor() {
        owner = msg.sender;
    }
    
    function mintPassport(
        string memory cropType,
        string memory season,
        string memory ipfsHash,
        string memory location,
        uint256 area
    ) external returns (uint256) {
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        passports[tokenId] = Passport({
            cropType: cropType,
            season: season,
            ipfsHash: ipfsHash,
            farmer: msg.sender,
            timestamp: block.timestamp,
            verified: false,
            location: location,
            area: area
        });
        
        farmerPassports[msg.sender].push(tokenId);
        
        emit PassportCreated(tokenId, msg.sender, cropType, season);
        return tokenId;
    }
    
    function getPassport(uint256 tokenId) external view returns (
        string memory cropType,
        string memory season,
        string memory ipfsHash,
        address farmer,
        uint256 timestamp,
        bool verified,
        string memory location,
        uint256 area
    ) {
        Passport memory p = passports[tokenId];
        return (p.cropType, p.season, p.ipfsHash, p.farmer, p.timestamp, p.verified, p.location, p.area);
    }
    
    function getFarmerPassports(address farmer) external view returns (uint256[] memory) {
        return farmerPassports[farmer];
    }
    
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter;
    }
}