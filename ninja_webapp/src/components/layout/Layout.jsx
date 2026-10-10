/**
 * @file Layout.jsx
 * @description Layout wrapper with Header, main content, and Footer.
 */

import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import styles from './Layout.module.css';
import { useTranslation } from 'react-i18next';
import useRobotSession from '../../hooks/useRobotSession';

function Layout() {
    const status = useRobotSession();
    const { t } = useTranslation();
    return (
        <div className={styles.layout}>
            <Header />
            <main className={styles.main}>
                {status === 'connected' ? <Outlet /> : (
                    <p role="status" aria-live="polite">{t(`session.${status}`)}</p>
                )}
            </main>
            <Footer />
        </div>
    );
}

export default Layout;
