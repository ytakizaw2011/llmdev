import pytest
from authenticator import Authenticator

@pytest.fixture
def authenticator():
    auth = Authenticator()
    yield auth

@pytest.mark.parametrize("username, password, expected", [
    ("Tanaka", "abc123", "abc123"),
    ("鈴木", "def456", "def456"),
    ("Sato", "abc123", "abc123"),
])

def test_register(authenticator, username, password, expected):
    authenticator.register(username, password)
    assert authenticator.users[username] == expected

def test_register_by_duplication(authenticator):
    authenticator.register("Yamada", "abc123")
    with pytest.raises(ValueError, match="エラー: ユーザーは既に存在します。"):
        authenticator.register("Yamada", "abc123")

@pytest.mark.parametrize("username, password, expected", [
    ("Tanaka", "abc123", "ログイン成功"),
    ("鈴木", "def456", "ログイン成功"),
    ("Sato", "abc123", "ログイン成功"),
])

def test_login(authenticator, username, password, expected):
    authenticator.register(username, password)
    result = authenticator.login(username, password)
    assert expected == result

def test_login_by_missmatch(authenticator):
    with pytest.raises(ValueError, match="エラー: ユーザー名またはパスワードが正しくありません。"):
        authenticator.login("Watanabe", "ghi789")
