import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skewer.app import create_app


@pytest.fixture
def app():
    # Mock load_config to return empty or dummy config
    with pytest.MonkeyPatch.context() as m:
        m.setattr("skewer.app.load_config", lambda: {"host": "test-host"})

        # Mock Teradata connection
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("Info", "Data")]
        mock_db.cursor.return_value = mock_cursor

        app = create_app()
        app.config.update({"TESTING": True})

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_route(client):
    # We need to mock the db module usage
    # Since 'db' is imported inside create_app, we patch where it is defined: skewer.db
    with patch("skewer.db.get_db") as mock_get_db:
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_cur.__enter__.return_value = mock_cur
        mock_cur.fetchall.return_value = [("DBC Version", "17.20")]

        mock_get_db.return_value = mock_conn

        response = client.get("/")
        assert response.status_code == 200
        assert b"Skewer" in response.data
        assert b"DBC Version" in response.data
