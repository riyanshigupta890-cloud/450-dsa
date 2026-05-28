from unittest.mock import MagicMock, patch
from app.platforms.fetchers import clear_platform_http_session, fetch_codechef


def setup_function():
    clear_platform_http_session()


def test_fetch_codechef_returns_data_on_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
        fully solved 150 problems
        "currentRating": 1845
        "highestRating": 1920
        "contestsAttended": 30
    '''
    fake_session = MagicMock()
    fake_session.get.return_value = mock_response

    with patch('app.platforms.fetchers._get_http_session', return_value=fake_session):
        result = fetch_codechef('tourist')

    assert result['total'] == 150
    assert result['rating'] == 1845
    assert result['highest_rating'] == 1920
    assert result['contests'] == 30


def test_fetch_codechef_returns_empty_on_non_200():
    mock_response = MagicMock()
    mock_response.status_code = 404
    fake_session = MagicMock()
    fake_session.get.return_value = mock_response

    with patch('app.platforms.fetchers._get_http_session', return_value=fake_session):
        result = fetch_codechef('unknown_user')

    assert result == {}


def test_fetch_codechef_returns_empty_on_exception():
    fake_session = MagicMock()
    fake_session.get.side_effect = Exception('timeout')

    with patch('app.platforms.fetchers._get_http_session', return_value=fake_session):
        result = fetch_codechef('tourist')

    assert result == {}


def test_fetch_codechef_handles_missing_fields_gracefully():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html>some page with no structured data</html>'
    fake_session = MagicMock()
    fake_session.get.return_value = mock_response

    with patch('app.platforms.fetchers._get_http_session', return_value=fake_session):
        result = fetch_codechef('tourist')

    assert result['total'] == 0
    assert result['rating'] is None
    assert result['highest_rating'] is None
    assert result['contests'] == 0
