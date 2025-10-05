// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VideoRegistry
 * @dev Smart contract for registering and managing video content on blockchain
 */
contract VideoRegistry {
    struct Video {
        string contentHash;
        address owner;
        uint256 timestamp;
        string metadata;
        bool exists;
    }
    
    // Mapping from content hash to Video
    mapping(string => Video) public videos;
    
    // Mapping from owner to their video hashes
    mapping(address => string[]) public ownerVideos;
    
    event VideoRegistered(
        string indexed contentHash,
        address indexed owner,
        uint256 timestamp
    );
    
    event OwnershipTransferred(
        string indexed contentHash,
        address indexed previousOwner,
        address indexed newOwner
    );
    
    /**
     * @dev Register a new video on the blockchain
     * @param contentHash Hash of the video content
     * @param metadata JSON metadata string
     */
    function registerVideo(
        string memory contentHash,
        string memory metadata
    ) public {
        require(!videos[contentHash].exists, "Video already registered");
        
        videos[contentHash] = Video({
            contentHash: contentHash,
            owner: msg.sender,
            timestamp: block.timestamp,
            metadata: metadata,
            exists: true
        });
        
        ownerVideos[msg.sender].push(contentHash);
        
        emit VideoRegistered(contentHash, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Transfer ownership of a video
     * @param contentHash Hash of the video content
     * @param newOwner Address of the new owner
     */
    function transferOwnership(
        string memory contentHash,
        address newOwner
    ) public {
        require(videos[contentHash].exists, "Video does not exist");
        require(videos[contentHash].owner == msg.sender, "Not the owner");
        require(newOwner != address(0), "Invalid new owner address");
        
        address previousOwner = videos[contentHash].owner;
        videos[contentHash].owner = newOwner;
        
        ownerVideos[newOwner].push(contentHash);
        
        emit OwnershipTransferred(contentHash, previousOwner, newOwner);
    }
    
    /**
     * @dev Get video information
     * @param contentHash Hash of the video content
     * @return Video struct
     */
    function getVideo(string memory contentHash)
        public
        view
        returns (
            string memory,
            address,
            uint256,
            string memory
        )
    {
        require(videos[contentHash].exists, "Video does not exist");
        Video memory video = videos[contentHash];
        return (
            video.contentHash,
            video.owner,
            video.timestamp,
            video.metadata
        );
    }
    
    /**
     * @dev Get all videos owned by an address
     * @param owner Address of the owner
     * @return Array of content hashes
     */
    function getOwnerVideos(address owner)
        public
        view
        returns (string[] memory)
    {
        return ownerVideos[owner];
    }
}
