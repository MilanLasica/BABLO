"""
Tests for BlockchainManager class.
"""

from bablo.blockchain import BlockchainManager


def test_blockchain_manager_initialization():
    """Test BlockchainManager initialization."""
    manager = BlockchainManager(network="ethereum")
    assert manager is not None
    assert manager.network == "ethereum"


def test_connect():
    """Test blockchain connection."""
    manager = BlockchainManager()
    result = manager.connect()
    assert result is True


def test_register_content():
    """Test content registration."""
    manager = BlockchainManager()

    tx_hash = manager.register_content(
        content_hash="test_hash_123", metadata={"title": "Test Video"}, content_type="video"
    )

    assert tx_hash is not None
    assert tx_hash.startswith("0x")
    assert len(tx_hash) == 66


def test_verify_content():
    """Test content verification."""
    manager = BlockchainManager()

    verification = manager.verify_content("test_hash")

    assert verification is not None
    assert "verified" in verification
    assert "content_hash" in verification
    assert verification["content_hash"] == "test_hash"


def test_get_owner():
    """Test getting content owner."""
    manager = BlockchainManager()

    owner = manager.get_owner("test_hash")

    assert owner is not None
    assert isinstance(owner, str)


def test_transfer_ownership():
    """Test ownership transfer."""
    manager = BlockchainManager()

    tx_hash = manager.transfer_ownership(
        content_hash="test_hash", new_owner="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    )

    assert tx_hash is not None
    assert tx_hash.startswith("0x")
