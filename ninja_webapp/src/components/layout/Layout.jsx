/**
 * @file Layout.jsx
 * @description Persistent controller session and page layout.
 */

import { Outlet, useLocation } from 'react-router-dom';
import Header from './Header';
import styles from './Layout.module.css';
import { useTranslation } from 'react-i18next';
import useRobotSession from '../../hooks/useRobotSession';

function Layout() {
    const status = useRobotSession();
    const { t } = useTranslation();
    const { pathname } = useLocation();
    return (
        <div className={styles.layout}>
            {pathname !== '/' && <Header status={status} />}
            <main className={styles.main}>
                {status === 'connected' ? <Outlet /> : (
                    <p role="status" aria-live="polite">{t(`session.${status}`)}</p>
                )}
            </main>
        </div>
    );
}

export default Layout;
