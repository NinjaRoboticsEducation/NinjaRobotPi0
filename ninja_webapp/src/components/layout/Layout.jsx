/**
 * @file Layout.jsx
 * @description Persistent controller session and page layout.
 */

import { Outlet, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Header from './Header';
import styles from './Layout.module.css';
import { useTranslation } from 'react-i18next';
import useRobotSession from '../../hooks/useRobotSession';
import useAppViewport from '../../hooks/useAppViewport';
import requestAppFullscreen from '../../utils/fullscreen';

function Layout() {
    const status = useRobotSession();
    const { t } = useTranslation();
    const { pathname } = useLocation();
    useAppViewport();
    const [selectedInterface, setSelectedInterface] = useState(
        () => ['/movement', '/agent'].includes(pathname) ? pathname : null
    );
    const [robotType, setRobotType] = useState(null);
    useEffect(() => {
        if (status !== 'connected') return;
        const abort = new AbortController();
        const load = async () => {
            try {
                const response = await fetch('/api/robot/status', { signal: abort.signal });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                if (!abort.signal.aborted) {
                    setRobotType(['tire', 'humanoid', 'spider'].includes(data.robot_type) ? data.robot_type : null);
                }
            } catch { if (!abort.signal.aborted) setRobotType(null); }
        };
        load();
        return () => abort.abort();
    }, [status]);
    const selectInterface = path => {
        setSelectedInterface(path);
        requestAppFullscreen();
    };
    return (
        <div className={styles.layout}>
            {pathname !== '/' && <Header status={status} robotType={robotType} />}
            <main className={styles.main}>
                {status === 'connected' ? <Outlet context={{ selectedInterface, selectInterface, robotType }} /> : (
                    <p role="status" aria-live="polite">{t(`session.${status}`)}</p>
                )}
            </main>
        </div>
    );
}

export default Layout;
