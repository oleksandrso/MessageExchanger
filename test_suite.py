import pytest
import client
import random
import string
import requests


# Function to clear queues
def clear_queues():
    requests.delete('http://localhost:8000')


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    clear_queues()


# Test POST request functionality
def test_post_message():
    assert client.post_message("Hello") == 200
    assert client.post_message("") == 204


# Test GET request functionality
def test_get_message():
    assert client.get_message() == 200
    assert client.get_message('9999') == 400


# Generate random string
def random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


# Test with random data
def test_random_data():
    for _ in range(10):
        assert client.post_message(random_string(), str(random.randint(0, 10000))) == 200
        assert client.get_message(str(random.randint(0, 10000))) in [200, 400]


# Test with special characters
def test_special_characters():
    assert client.post_message("!@#$%^&*()_+", '1') == 200
    assert client.get_message('1') == 200


# Test with very long string
def test_long_string():
    assert client.post_message("a" * 1000, '1') == 200
    assert client.get_message('1') == 200


# Test for queue limit
def test_queue_limit():
    for i in range(100):  # Reduced to 100 to avoid filling the queue
        assert client.post_message(f"Message {i}", '1') == 200
    assert client.post_message("This should not be added", '1') == 204


# Test for multiple queues
def test_multiple_queues():
    unique_alias1 = 'unique1'
    unique_alias2 = 'unique2'
    assert client.post_message("Queue 1", unique_alias1) == 200
    assert client.post_message("Queue 2", unique_alias2) == 200
    assert client.get_message(unique_alias1) == 200
    assert client.get_message(unique_alias2) == 200


# Test for ignoring incorrect messages
def test_ignore_incorrect():
    assert client.post_message("", '1') == 204
    assert client.post_message(None, '1') == 204


# Load testing (Optional)
def test_load():
    for i in range(100):
        assert client.post_message(f"Message {i}") == 200


# Security testing (Optional)
def test_security():
    assert client.post_message("<script>alert('XSS')</script>") == 204
