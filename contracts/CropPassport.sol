// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract CropPassport is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

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
    
    event PassportCreated(uint256 indexed tokenId, address indexed farmer, string cropType, string season);
    event PassportVerified(uint256 indexed tokenId, address indexed verifier);
    
    constructor() ERC721("Krishi Sahayak Crop Passport", "KSCP") {}
    
    function mintPassport(
        string memory cropType,
        string memory season,
        string memory ipfsHash,
        string memory location,
        uint256 area
    ) external returns (uint256) {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        
        _mint(msg.sender, tokenId);
        
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
    
    function verifyPassport(uint256 tokenId) external onlyOwner {
        require(_exists(tokenId), "Passport does not exist");
        passports[tokenId].verified = true;
        emit PassportVerified(tokenId, msg.sender);
    }
    
    function getPassport(uint256 tokenId) external view returns (Passport memory) {
        require(_exists(tokenId), "Passport does not exist");
        return passports[tokenId];
    }
    
    function getFarmerPassports(address farmer) external view returns (uint256[] memory) {
        return farmerPassports[farmer];
    }
    
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter.current();
    }
}