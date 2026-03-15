import pytest
import hashlib

from scripts.extract_load import hash_ip_address

def test_hash_ip_address_valid():
    """Test that a valid IP address is correctly hashed and anonymized"""
    raw_ip = "192.168.1.10"
    salt = "darktrace_secure_salt_2026"

    # Manually create what the expected hash should be
    expected_hash = hashlib.sha256((raw_ip + salt).encode('utf-8')).hexdigest()

    # Run pipline function
    actual_hash = hash_ip_address(raw_ip, salt)

    # Assert they match
    assert actual_hash == expected_hash

def test_hash_ip_address_null():
    """Test that the function handles empty or null IPs gracefully."""
    assert hash_ip_address(None, "salt") is None
    assert hash_ip_address("", "salt") is None