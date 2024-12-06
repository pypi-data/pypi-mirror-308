import pytest
import requests_mock
from opmentis import register_miners, userdata, endchat

# Base URL for the API
BASE_URL = "https://labfoodbot.opmentis.xyz/api/v1"

def test_register_miners_success():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dy"
    endpoint = f"{BASE_URL}/authenticate_or_register"
    
    # Mock response for a successful registration with access_token
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"access_token": "mocked_token"}, status_code=200)
        response = register_miners(wallet_address)
        
        assert response == "mocked_token", f"Expected access token, but got '{response}'"

def test_register_miners_duplicate():
    wallet_address = "0x0EDA10bE51C5458E00Af47d16751250ce188aC37"
    endpoint = f"{BASE_URL}/authenticate_or_register"
    expected_response = "User already exists. No need to register again."

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"message": "User already exists"}, status_code=200)
        response = register_miners(wallet_address)
        
        # Assert that the response matches the expected error message
        assert response == expected_response, f"Expected response was '{expected_response}', but got '{response}'"

def test_register_miners_invalid():
    wallet_address = "0x42C58401622D09827EF8dD33d93Dc"  # Invalid wallet address
    endpoint = f"{BASE_URL}/authenticate_or_register"
    expected_response = "Registration failed: Invalid wallet address format"

    # Setup mock for an invalid wallet address attempt
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"message": "Invalid wallet address format"}, status_code=400)
        response = register_miners(wallet_address)
        
        # Assert that the response matches the expected error message
        assert response == expected_response, f"Expected response was '{expected_response}', but got '{response}'"

def test_register_miners_missing_stake():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/authenticate_or_register"
    
    # Mock response for missing stake in new user registration
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"message": "Stake is required for new user registration."}, status_code=400)
        response = register_miners(wallet_address)
        
        assert response == "Registration failed: Stake is required for new user registration."

def test_register_miners_server_error():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/authenticate_or_register"
    
    # Mock response for a server error
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"message": "Database query error."}, status_code=500)
        response = register_miners(wallet_address)
        
        assert response == "Server error: Database query error."

def test_userdata_success():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/user_data/table"
    expected_response = "Mocked table data"

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"user_table": expected_response}, status_code=200)
        response = userdata(wallet_address)
        
        # Assert response
        assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"
        
        # Assert last request payload
        assert m.last_request.json() == {"wallet_address": wallet_address}

def test_userdata_failure():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/user_data/table"
    expected_response = {"error": "Failed to fetch user data.", "status_code": 500}

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"error": "Failed to fetch user data."}, status_code=500)
        response = userdata(wallet_address)
        
        # Assert response
        assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"
        
        # Assert last request payload
        assert m.last_request.json() == {"wallet_address": wallet_address}
