import pytest
from cryptography.fernet import InvalidToken

from storage import Storage


@pytest.fixture
def storage():
    return Storage()


# basic storage tests

def test_init_empty(storage):
    assert storage.messages == {}


def test_add_message(storage):
    storage.add_message(1, "hello")
    assert storage.messages[1] == "hello"


def test_get_message_existing(storage):
    storage.add_message(42, "world")
    assert storage.get_message(42) == "world"


def test_get_message_missing(storage):
    assert storage.get_message(999) is None


def test_add_message_overwrites(storage):
    storage.add_message(1, "first")
    storage.add_message(1, "second")
    assert storage.get_message(1) == "second"


# storage persistence tests


def test_save_load_round_trip(storage, tmp_path):
    path = tmp_path / "messages.enc"
    expected = {1: "Hello", 42: "This is a saved message"}

    for msg_id, text in expected.items():
        storage.add_message(msg_id, text)

    storage.save(str(path), "secret")
    restored = Storage()
    restored.load(str(path), "secret")

    assert restored.messages == expected
    assert all(isinstance(key, int) for key in restored.messages)


def test_save_load_empty_storage(storage, tmp_path):
    path = tmp_path / "empty.enc"
    storage.save(str(path), "secret")

    restored = Storage()
    restored.load(str(path), "secret")

    assert restored.messages == {}


def test_load_replaces_existing_messages(storage, tmp_path):
    path = tmp_path / "messages.enc"
    storage.add_message(1, "Saved message")
    storage.save(str(path), "secret")

    storage.add_message(1, "Changed message")
    storage.add_message(2, "Unsaved message")
    storage.load(str(path), "secret")

    assert storage.messages == {1: "Saved message"}


def test_load_wrong_passphrase_preserves_messages(storage, tmp_path):
    path = tmp_path / "messages.enc"
    storage.add_message(1, "Saved message")
    storage.save(str(path), "correctpassword")
    storage.add_message(2, "Unsaved message")
    expected = storage.messages.copy()

    with pytest.raises(InvalidToken):
        storage.load(str(path), "wrongpassword")

    assert storage.messages == expected


def test_save_overwrites_existing_file(storage, tmp_path):
    path = tmp_path / "messages.enc"
    storage.add_message(1, "Original message")
    storage.save(str(path), "secret")

    storage.add_message(1, "Updated message")
    storage.add_message(2, "New message")
    storage.save(str(path), "secret")

    restored = Storage()
    restored.load(str(path), "secret")

