import os
import importlib
from datetime import datetime, timedelta


def make_mock_supabase(data):
    class MockQuery:
        def __init__(self, data):
            self._data = data

        def select(self, *args, **kwargs):
            return self

        def execute(self):
            class R:
                pass

            r = R()
            r.data = self._data
            return r

    class MockSupabase:
        def __init__(self, data):
            self._data = data

        def table(self, name):
            return MockQuery(self._data)

    return MockSupabase(data)


def test_stats_page_with_data():
    # Ensure env vars exist so app import doesn't raise
    os.environ.setdefault('SUPABASE_URL', 'http://example')
    os.environ.setdefault('SUPABASE_KEY', 'dummy')

    # Import app after env vars are set
    app = importlib.import_module('app')

    # Prepare mock data: one recent visitor and one older
    now = datetime.utcnow()
    recent = {
        'name': 'Alice',
        'visit_count': 5,
        'first_visit': (now - timedelta(hours=1)).isoformat() + 'Z',
        'last_visit': now.isoformat() + 'Z'
    }
    older = {
        'name': 'Bob',
        'visit_count': 2,
        'first_visit': (now - timedelta(days=10)).isoformat() + 'Z',
        'last_visit': (now - timedelta(days=5)).isoformat() + 'Z'
    }

    app.supabase = make_mock_supabase([recent, older])

    client = app.app.test_client()
    resp = client.get('/stats')
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    # Should contain both names in the rendered template
    assert 'Alice' in body
    assert 'Bob' in body
