#!/usr/bin/env python3
"""Call an Instatic MCP tool over HTTP.

This session's MCP client failed to connect at startup (the container was down
then). The server is healthy, so we speak JSON-RPC to it directly instead of
losing the tooling for the whole session.
"""
import json, subprocess, sys, urllib.request

def token():
    out = subprocess.run(['claude','mcp','get','instatic'], capture_output=True, text=True).stdout
    for w in out.split():
        if w.startswith('imcp_pat_'): return w
    raise SystemExit('no instatic token in config')

def call(tool, args=None):
    body = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call',
                       'params':{'name':tool,'arguments':args or {}}}).encode()
    req = urllib.request.Request('http://localhost:3022/_instatic/mcp', data=body, headers={
        'Authorization': 'Bearer ' + token(),
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'})
    raw = urllib.request.urlopen(req, timeout=180).read().decode()
    for line in raw.splitlines():
        if line.startswith('data: '):
            d = json.loads(line[6:])
            if 'error' in d: return {'_error': d['error']}
            res = d.get('result', {})
            texts = [c.get('text','') for c in res.get('content', [])]
            joined = '\n'.join(texts)
            if res.get('isError'): return {'_toolError': joined}
            try: return json.loads(joined)
            except Exception: return joined
    return None

if __name__ == '__main__':
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    out = call(sys.argv[1], args)
    print(json.dumps(out, indent=1) if isinstance(out, (dict, list)) else out)
