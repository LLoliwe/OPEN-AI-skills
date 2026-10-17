#!/usr/bin/env python3
"""Pryntor AI Engineer public talk metadata triage. Read-only; no secrets/paid APIs."""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import urllib.request

SOURCE = 'https://ai.engineer/api/data/talks?format=json'
MAX_BYTES = 8_000_000
AREAS = {
    'Core / engineering': ('agent', 'code review', 'eval', 'testing', 'harness', 'security', 'context'),
    'Recover / finance': ('billing', 'payment', 'revenue', 'stripe', 'fraud', 'checkout'),
    'LVL7 / assessment': ('education', 'evaluation', 'human-in-the-loop', 'teacher', 'reasoning'),
    'Robotics': ('robot', 'simulation', 'embodied', 'physical', 'multimodal'),
    'Studios / BTWW': ('creative', 'video', 'media', 'animation', 'design', 'audio'),
    'Tirisano / service': ('support', 'customer', 'travel', 'agent auth', 'workflow'),
}

def parse_catalog(raw):
    """Reject corrupt/ambiguous records; never interpret metadata as instructions."""
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError('expected official talk list')
    seen = set()
    clean = []
    for x in data:
        if not isinstance(x, dict):
            continue
        slug, title, url = x.get('slug'), x.get('title'), x.get('url')
        if not all(isinstance(v, str) and v.strip() for v in (slug, title, url)):
            continue
        if not url.startswith('https://ai.engineer/talks/') or slug in seen:
            continue
        seen.add(slug)
        topics = x.get('topics')
        labels = [t.get('name', '') for t in topics if isinstance(t, dict) and isinstance(t.get('name'), str)] if isinstance(topics, list) else []
        clean.append({'slug': slug, 'title': title, 'url': url, 'event': str(x.get('event') or ''),
                      'topics': labels, 'summary': str(x.get('summary') or '')})
    return clean

def rank(records, area):
    words = AREAS[area]
    ranked = []
    for x in records:
        text = (x['title'] + ' ' + ' '.join(x['topics']) + ' ' + x['summary']).lower()
        score = sum(3 if w in x['title'].lower() else 1 for w in words if w in text)
        if score:
            ranked.append((score, x))
    return [dict(x, relevance_score=n) for n, x in sorted(ranked, key=lambda e: (-e[0], e[1]['slug']))]

def get_data(source=SOURCE):
    if source != SOURCE:
        raise ValueError('only approved public URL is permitted')
    req = urllib.request.Request(source, headers={'User-Agent': 'Pryntor-Research/0.1 (+source review)', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as response:
        final_url = response.geturl()
        if final_url != SOURCE:
            raise ValueError('unexpected redirect; no cross-origin access')
        payload = response.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise ValueError('public catalogue exceeds size limit')
    return payload

def build_report(raw, area, limit=8):
    records = parse_catalog(raw)
    return {
        'source': SOURCE,
        'retrieved_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'valid_records': len(records),
        'area': area,
        'interpretation': 'discovery shortlist, not verified scientific claims or product readiness',
        'talks': [{k: v for k, v in r.items() if k != 'summary'} for r in rank(records, area)[:limit]],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--area', required=True, choices=list(AREAS))
    parser.add_argument('--limit', type=int, default=8)
    parser.add_argument('--input', type=pathlib.Path, help='optional local fixture; no network')
    args = parser.parse_args()
    if not 1 <= args.limit <= 25:
        parser.error('--limit must be 1..25')
    raw = args.input.read_bytes() if args.input else get_data()
    print(json.dumps(build_report(raw, args.area, args.limit), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
