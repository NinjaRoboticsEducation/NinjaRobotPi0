// Shared across Movement page mounts: navigation cannot queue another physical command.
let state = { busy: false, uncertain: false };
const listeners = new Set();
const publish = next => { state = next; for (const listener of listeners) listener(); };
export const movementSnapshot = () => state;
export const subscribeMovement = listener => { listeners.add(listener); return () => listeners.delete(listener); };

export async function runNativeMovement(name) {
    if (state.busy || state.uncertain) return false;
    publish({ busy: true, uncertain: false });
    let uncertain = false;
    try {
        // Do not abort this request on release: aborting fetch would not cancel motion.
        const response = await fetch(`/api/servos/movements/${encodeURIComponent(name)}/execute`, { method: 'POST' });
        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            const error = new Error(data.detail || `HTTP ${response.status}`);
            error.knownResponse = response.status < 500;
            throw error;
        }
        const data = await response.json();
        if (data.status !== 'executed') throw new Error('Movement completion was not confirmed');
        return true;
    } catch (error) {
        // A lost response can leave the robot moving. Keep controls locked until reload.
        uncertain = !error.knownResponse;
        throw error;
    } finally {
        publish({ busy: false, uncertain });
    }
}
