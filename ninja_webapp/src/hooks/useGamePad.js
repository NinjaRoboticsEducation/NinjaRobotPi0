import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { movementSnapshot, runNativeMovement, subscribeMovement } from '../utils/nativeMovement';

export default function useGamePad(actions, onError, onStart) {
    const movement = useSyncExternalStore(subscribeMovement, movementSnapshot);
    const [pressed, setPressed] = useState(null);
    const intent = useRef(null);
    const alive = useRef(false);
    const release = useCallback(source => {
        if (source && intent.current?.source !== source) return;
        intent.current = null;
        setPressed(null);
    }, []);
    useEffect(() => {
        alive.current = true;
        const cancel = () => release();
        const visibility = () => { if (document.hidden) release(); };
        window.addEventListener('blur', cancel);
        window.addEventListener('pagehide', cancel);
        document.addEventListener('visibilitychange', visibility);
        return () => {
            alive.current = false;
            intent.current = null;
            window.removeEventListener('blur', cancel);
            window.removeEventListener('pagehide', cancel);
            document.removeEventListener('visibilitychange', visibility);
        };
    }, [release]);
    const press = (direction, source) => {
        const name = actions[direction];
        const snapshot = movementSnapshot();
        if (!name || intent.current || snapshot.busy || snapshot.uncertain || document.hidden) return false;
        const current = { source, direction };
        intent.current = current;
        onStart?.();
        setPressed(direction);
        const execute = async () => {
            try {
                do {
                    if (!await runNativeMovement(name)) break;
                } while (direction !== 'center' && alive.current && intent.current === current && !document.hidden);
            } catch (error) {
                if (alive.current) { onError(error); release(); }
            } finally {
                if (direction !== 'center' && alive.current && intent.current === current) release();
            }
        };
        execute();
        return true;
    };
    return { pressed, press, release, ...movement };
}
