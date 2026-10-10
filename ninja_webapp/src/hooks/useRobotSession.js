import { useEffect, useState } from 'react';

// Keep ownership for the whole browser visit, including Home/Agent/Help navigation.
export default function useRobotSession() {
    const [status, setStatus] = useState('connecting');
    useEffect(() => {
        let active = true;
        let leaving = false;
        let socket;
        let retry;
        let heartbeat;

        const clearTimers = () => {
            clearTimeout(retry);
            clearInterval(heartbeat);
        };
        const scheduleRetry = () => {
            if (active && !leaving) retry = setTimeout(connect, 3000);
        };
        const connect = () => {
            if (!active || leaving) return;
            clearTimers();
            try {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const current = new WebSocket(`${protocol}//${window.location.host}/ws/session`);
                socket = current;
                current.onopen = () => {
                    if (!active || socket !== current) return;
                    heartbeat = setInterval(() => {
                        if (current.readyState === WebSocket.OPEN) current.send('ping');
                    }, 10000);
                };
                current.onmessage = event => {
                    if (!active || socket !== current) return;
                    try {
                        const message = JSON.parse(event.data);
                        if (message.type === 'session' && ['connected', 'busy'].includes(message.status)) {
                            setStatus(message.status);
                        }
                    } catch {
                        // A malformed event cannot grant access to controls.
                    }
                };
                current.onclose = event => {
                    if (socket !== current) return;
                    clearInterval(heartbeat);
                    if (!active || leaving) return;
                    setStatus(event.code === 4409 ? 'busy' : 'disconnected');
                    scheduleRetry();
                };
                current.onerror = () => {
                    if (active && !leaving && socket === current) setStatus('disconnected');
                };
            } catch {
                setStatus('disconnected');
                scheduleRetry();
            }
        };
        const leave = () => {
            leaving = true;
            clearTimers();
            socket?.close();
        };
        const resume = event => {
            if (event.persisted) {
                leaving = false;
                setStatus('connecting');
                connect();
            }
        };
        connect();
        window.addEventListener('pagehide', leave);
        window.addEventListener('pageshow', resume);
        return () => {
            active = false;
            leave();
            window.removeEventListener('pagehide', leave);
            window.removeEventListener('pageshow', resume);
        };
    }, []);
    return status;
}
