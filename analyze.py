"""Run: python analyze.py web.log worker.log"""
import sys
from collections import Counter

web = {}
with open(sys.argv[1]) as lines:
    for line in lines:
        match = re.search(r'method=(\S+) path=(\S+) status=(\d+).*user_id=(\d+) request_id=(\w+)', line)
        if match:
            method, path, status, user, request = match.groups()
            web[request] = (method, path, status, int(user), line[:23])

results = Counter()
affected = set()
first = None
with open(sys.argv[2]) as lines:
    for line in lines:
        if '[worker]' not in line:
     
        match = re.search(r'request_id=(\w+)', line)
        if not match or match.group(1) not in web:
          
        method, path, status, user, timestamp = web[match.group(1)]
        if method != 'POST' or path != '/checkout':
           
        period = 'after' if timestamp >= '2026-07-02 14:32:40' else 'before'
        parity = 'odd' if user % 2 else 'even'
        outcome = 'failed' if 'ERROR [worker]' in line else 'completed'
        results[(period, parity, outcome)] += 1
        if outcome == 'failed':
            affected.add(user)
            candidate = (line[:23], timestamp, match.group(1))
            if first is None or candidate < first:
                first = candidate

print('First failure (worker timestamp, web timestamp, request_id):', first)
for key, count in sorted(results.items()):
    print(*key, count)
print('Distinct affected users:', len(affected))
