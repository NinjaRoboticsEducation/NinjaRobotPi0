// Inert socket/timer lifecycle harness; no browser connection or robot request.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const states = [], sockets = [], timeouts = new Map(), intervals = new Map(), listeners = new Map();
let cleanup, timerId = 0;
class Socket {
    static OPEN = 1;
    constructor(url) { this.url = url; this.readyState = 1; this.sent = []; sockets.push(this); }
    send(value) { this.sent.push(value); }
    close() { this.readyState = 3; this.onclose?.({ code: 1000 }); }
}
const context = {
    useState: value => [value, next => states.push(next)],
    useEffect: effect => { cleanup = effect(); },
    WebSocket: Socket,
    window: {
        location: { protocol: 'https:', host: 'inert.example.test' },
        addEventListener: (name, handler) => listeners.set(name, handler),
        removeEventListener: name => listeners.delete(name),
    },
    setTimeout: fn => { const id = ++timerId; timeouts.set(id, fn); return id; },
    clearTimeout: id => timeouts.delete(id),
    setInterval: fn => { const id = ++timerId; intervals.set(id, fn); return id; },
    clearInterval: id => intervals.delete(id),
};
const source = fs.readFileSync(path.join(__dirname, '../ninja_webapp/src/hooks/useRobotSession.js'), 'utf8')
    .replace(/^import .*;\n/m, '').replace('export default function', 'function');
vm.runInNewContext(source + '\nuseRobotSession();', context);
const first = sockets[0];
assert.equal(first.url, 'wss://inert.example.test/ws/session');
first.onopen();
first.onmessage({ data: '{"type":"session","status":"connected"}' });
assert.equal(states.at(-1), 'connected');
Array.from(intervals.values())[0]();
assert.deepEqual(first.sent, ['ping']);
first.onmessage({ data: 'invalid JSON' });
assert.equal(states.at(-1), 'connected');
first.onclose({ code: 4409 });
assert.equal(states.at(-1), 'busy');
assert.equal(intervals.size, 0);
Array.from(timeouts.values())[0]();
const second = sockets[1];
second.onopen();
second.onmessage({ data: '{"type":"session","status":"connected"}' });
first.onclose({ code: 1000 }); // Stale callback must not disturb the replacement.
assert.equal(states.at(-1), 'connected');
assert.equal(intervals.size, 1);
listeners.get('pagehide')();
assert.equal(second.readyState, 3);
assert.equal(intervals.size, 0);
assert.equal(timeouts.size, 0);
listeners.get('pageshow')({ persisted: true });
assert.equal(states.at(-1), 'connecting');
assert.equal(sockets.length, 3);
cleanup();
assert.equal(listeners.size, 0);
assert.equal(sockets[2].readyState, 3);
assert.equal(timeouts.size, 0);
console.log('PASS: session heartbeat, busy/retry, stale socket, pagehide/pageshow and cleanup');
