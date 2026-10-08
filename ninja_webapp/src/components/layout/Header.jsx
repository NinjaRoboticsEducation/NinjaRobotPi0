import { useState, useEffect, useRef } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import LanguageSelector from '../common/LanguageSelector';
import styles from './Header.module.css';

function Header() {
    const { t } = useTranslation();
    const location = useLocation();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isBleAdvertising, setIsBleAdvertising] = useState(false);
    const buttonRef = useRef(null);
    const menuRef = useRef(null);

    // This reports advertising only, not a connected or authenticated controller.
    useEffect(() => {
        const checkBleStatus = async () => {
            try {
                const res = await fetch('/api/ble/status');
                if (res.ok) {
                    const data = await res.json();
                    setIsBleAdvertising(data.advertising || false);
                } else { setIsBleAdvertising(false); }
            } catch { setIsBleAdvertising(false); }
        };
        checkBleStatus();
        const interval = setInterval(checkBleStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (!isMenuOpen) return;
        const trigger = buttonRef.current;
        const focusables = () => [...menuRef.current.querySelectorAll('button, a, select')];
        focusables()[0]?.focus();
        const onKeyDown = (event) => {
            if (event.key === 'Escape') setIsMenuOpen(false);
            if (event.key !== 'Tab') return;
            const items = focusables();
            const first = items[0];
            const last = items[items.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault(); last?.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault(); first?.focus();
            }
        };
        document.addEventListener('keydown', onKeyDown);
        return () => { document.removeEventListener('keydown', onKeyDown); trigger?.focus(); };
    }, [isMenuOpen]);

    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <NavLink to="/" className={styles.logo}>
                    <img src="/logo.png" alt="" className={styles.logoImage} />
                    <span>NINJA ROBOT PI0</span>
                </NavLink>
                <span className={`${styles.badge} ${isBleAdvertising ? styles.advertising : ''}`}>
                    {t(isBleAdvertising ? 'header.advertising' : 'header.bleOff')}
                </span>
                <button ref={buttonRef} className={styles.menuButton}
                    onClick={() => setIsMenuOpen(true)} aria-label={t('header.openMenu')}
                    aria-expanded={isMenuOpen} aria-controls="robot-menu">☰</button>
            </div>
            {isMenuOpen && (
                <div className={styles.backdrop} onClick={() => setIsMenuOpen(false)}>
                    <div id="robot-menu" ref={menuRef} className={styles.menuSheet} role="dialog"
                        aria-modal="true" aria-labelledby="robot-menu-title" onClick={(event) => event.stopPropagation()}>
                        <div className={styles.menuHeading}>
                            <h2 id="robot-menu-title">{t('header.menuTitle')}</h2>
                            <button onClick={() => setIsMenuOpen(false)} aria-label={t('header.closeMenu')}>×</button>
                        </div>
                        <nav className={styles.nav} aria-label={t('header.navigation')}>
                            {[['/', 'home'], ['/agent', 'agent'], ['/help', 'help']].map(([path, label]) => (
                                <NavLink key={path} to={path} className={location.pathname === path ? styles.active : ''}
                                    onClick={() => setIsMenuOpen(false)}>{t(`nav.${label}`)}</NavLink>
                            ))}
                        </nav>
                        <LanguageSelector />
                    </div>
                </div>
            )}
        </header>
    );
}

export default Header;
