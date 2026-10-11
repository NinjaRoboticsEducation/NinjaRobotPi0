import { useEffect } from 'react';

// Auxiliary streams reconnect independently; session ownership still gates their pages.
export default function useRobotStream(path, onMessage, onUnavailable) {
    useEffect(() => {
        let active = true;
        let socket;
        let retry;
        const connect = () => {
            if (!active) return;
            try {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const current = new WebSocket(`${protocol}//${window.location.host}${path}`);
                socket = current;
                current.onmessage = event => {
                    if (active && socket === current) onMessage(event.data);
                };
                current.onerror = () => { if (active) onUnavailable?.(); };
                current.onclose = () => {
                    if (!active) return;
                    onUnavailable?.();
                    retry = setTimeout(connect, 3000);
                };
            } catch {
                onUnavailable?.();
                retry = setTimeout(connect, 3000);
            }
        };
        connect();
        return () => {
            active = false;
            clearTimeout(retry);
            socket?.close();
        };
    }, [path, onMessage, onUnavailable]);
}
