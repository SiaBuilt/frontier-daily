#!/usr/bin/env python3
"""Collect public RSS/Atom evidence; no brief edits or automatic editorial claims.

Usage: python3 scripts/collect_sources.py --output /tmp/frontier-sources
Results include HTTP errors, original dates, full feed-provided text and transcript
links. Feed text may be an excerpt; length is never proof of completeness.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS_ATOM = '{http://www.w3.org/2005/Atom}'

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.hidden += 1
        if tag in ('p', 'br', 'div', 'li', 'h1', 'h2', 'h3'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.hidden = max(0, self.hidden - 1)
    def handle_data(self, text):
        if not self.hidden: self.parts.append(text)

def plain(value):
    parser = PlainText()
    parser.feed(value)
    return '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())

def date_value(raw):
    if not raw: return None
    try:
        value = datetime.fromisoformat(raw.replace('Z', '+00:00'))
    except ValueError:
        try:
            value = parsedate_to_datetime(raw)
            # RFC 5322 -0000 is UTC with unknown originating local zone.
            if value.tzinfo is None and raw.strip().endswith('-0000'):
                value = value.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError, OverflowError): return None
    # Never invent a timezone for ambiguous dates.
    return value.astimezone(timezone.utc) if value.tzinfo else None

def parse_feed(body, source, now):
    root = ET.fromstring(body)
    if root.tag == NS_ATOM + 'feed':
        nodes = root.findall(NS_ATOM + 'entry')
    elif root.tag == 'rss':
        nodes = root.findall('./channel/item')
    else:
        raise ValueError('Response is not an RSS/Atom feed')
    entries = []
    for node in nodes:
        fields = {}
        for child in node:
            fields.setdefault(child.tag.split('}')[-1], child.text or '')
        links = [c.attrib.get('href') for c in node if c.tag == NS_ATOM+'link' and c.attrib.get('rel','alternate') == 'alternate']
        url = next((u for u in links if u), '') or fields.get('link','')
        raw = fields.get('pubDate') or fields.get('published') or ''
        stamp = date_value(raw)
        text_raw = fields.get('encoded') or fields.get('content') or fields.get('description') or fields.get('summary') or ''
        age = now - stamp if stamp else None
        # Include older entries too, so an empty time window has visible evidence.
        entries.append({
            'title':fields.get('title',''), 'url':url,
            'publishedRaw':raw, 'publishedAt':stamp.isoformat() if stamp else None,
            'updatedRaw':fields.get('updated',''),
            'within36Hours':age is not None and timedelta(0) <= age <= timedelta(hours=36),
            'within7Days':age is not None and timedelta(0) <= age <= timedelta(days=7),
            'dateStatus':'verified_feed_date' if stamp else 'missing_or_ambiguous_publication_date',
            'contentStatus':'feed_text_requires_completeness_review' if text_raw else 'metadata_only',
            'text':plain(text_raw), 'contentHtml':text_raw,
            'transcripts':[dict(c.attrib) for c in node if c.tag.split('}')[-1]=='transcript'],
            'enclosures':[dict(c.attrib) for c in node if c.tag.split('}')[-1]=='enclosure'],
        })
    return entries

def collect(source, now):
    result = dict(source, fetchedAt=datetime.now(timezone.utc).isoformat(), attempts=[])
    for attempt in range(2):
        try:
            req = urllib.request.Request(source['url'], headers={'User-Agent':'FrontierDaily/1.0 (public RSS reader)', 'Accept':'application/rss+xml, application/atom+xml, application/xml, text/xml'})
            with urllib.request.urlopen(req, timeout=20) as response:
                body = response.read(12_000_001)
                result['attempts'].append({'status':response.status,'url':response.url})
            if len(body)>12_000_000: raise ValueError('Feed exceeds 12 MB limit')
            entries = parse_feed(body, source, now)
            result.update(status='ok', entries=entries, entryCount=len(entries),
                          recent36Hours=sum(e['within36Hours'] for e in entries),
                          recent7Days=sum(e['within7Days'] for e in entries),
                          unknownDates=sum(e['publishedAt'] is None for e in entries),
                          latestPublishedAt=max((e['publishedAt'] for e in entries if e['publishedAt']), default=None))
            return result
        except urllib.error.HTTPError as exc:
            result['attempts'].append({'httpStatus':exc.code,'error':str(exc)})
            status = {401:'authentication_required',403:'http_forbidden',404:'not_found',429:'rate_limited'}.get(exc.code,'http_error')
            retry = exc.code in (429,500,502,503,504)
        except (ET.ParseError, ValueError) as exc:
            result['attempts'].append({'error':str(exc)})
            status, retry = 'invalid_feed', False
        except (OSError, TimeoutError) as exc:
            result['attempts'].append({'error':str(exc)})
            status, retry = 'transport_error', True
        if attempt == 0 and retry: time.sleep(2)
        else: break
    result.update(status=status, entries=[])
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source', action='append', help='Optional source ID, repeatable')
    args = parser.parse_args()
    sources = json.loads((ROOT/'sources/feeds.json').read_text())
    if args.source:
        unknown = set(args.source)-{s['id'] for s in sources}
        if unknown: parser.error('Unknown source: '+', '.join(sorted(unknown)))
        sources = [s for s in sources if s['id'] in args.source]
    now = datetime.now(timezone.utc)
    args.output.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda s: collect(s, now), sources))
    for result in results:
        (args.output/(result['id']+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(result['id'], result['status'], '36h:',result.get('recent36Hours','?'), '7d:',result.get('recent7Days','?'))
    report = {'checkedAt':now.isoformat(),'sources':[{k:v for k,v in r.items() if k!='entries'} for r in results]}
    (args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    # Partial failures remain visible in report; other sources are still useful.
    return 0 if all(r['status']=='ok' for r in results) else 1

if __name__ == '__main__':
    raise SystemExit(main())
