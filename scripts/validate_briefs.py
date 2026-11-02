#!/usr/bin/env python3
"""Validate brief/index consistency; source accuracy still requires editorial checks."""
import argparse
import json
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def validate(day):
    date.fromisoformat(day)
    data = json.loads((ROOT / 'briefs' / f'{day}.json').read_text())
    index = json.loads((ROOT / 'briefs/index.json').read_text())
    assert data['date'] == day, 'date differs from filename'
    stamp = datetime.fromisoformat(data['generatedAt'])
    assert stamp.utcoffset() and stamp.utcoffset().total_seconds() == 28800, 'generatedAt must use +08:00'
    assert stamp.date().isoformat() == day, 'generatedAt date mismatch'
    for key in ('headline', 'stats', 'question'):
        assert isinstance(data.get(key), str) and data[key].strip(), f'missing {key}'
    assert isinstance(data['themes'], list) and all(isinstance(t, str) and t.strip() for t in data['themes']), 'invalid themes'
    assert [s['id'] for s in data['sections']] == ['x', 'pod', 'industry'], 'invalid sections'
    items = [i for s in data['sections'] for i in s['items']]
    assert items, 'empty brief'
    assert len({i['id'] for i in items}) == len(items), 'duplicate item id'
    assert len({i['url'] for i in items}) == len(items), 'duplicate URL'
    assert sum(i['weight'] == 3 for i in items) <= 2, 'too many top stories'
    for item in items:
        for key in ('id', 'who', 'tag', 'url', 'sourceLabel', 'title', 'summary', 'ctx'):
            assert isinstance(item.get(key), str) and item[key].strip(), f"{item.get('id')}: missing {key}"
        url = urlparse(item['url'])
        assert url.scheme in ('https', 'http') and url.netloc, 'invalid source URL'
        assert type(item['weight']) is int and item['weight'] in (1, 2, 3), 'invalid weight'
        if item.get('quote'):
            assert item.get('quoteZh') and item.get('gist'), 'quote needs translation and gist'
        if item['weight'] == 1:
            assert not item.get('soWhat'), 'weight 1 must not have soWhat'
    dates = [r['date'] for r in index]
    assert dates == sorted(set(dates), reverse=True), 'index must be unique and descending'
    entries = [r for r in index if r['date'] == day]
    assert len(entries) == 1, 'missing index entry'
    assert entries[0]['headline'] == data['headline'], 'headline mismatch'
    assert entries[0]['count'] == len(items), 'count mismatch'
    for filename in ('pulse.json', 'revenue.json'):
        json.loads((ROOT / filename).read_text())
    print(f'OK {day}: {len(items)} items; index consistent (source facts not checked)')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)
    args = parser.parse_args()
    try:
        validate(args.date)
    except (AssertionError, ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f'Validation failed: {exc}\n')
