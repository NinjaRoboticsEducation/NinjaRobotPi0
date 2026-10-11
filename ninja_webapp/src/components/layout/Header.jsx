import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import styles from './Header.module.css';

function Header({ status, robotType }) {
    const { t } = useTranslation();
    return (
        <header className={styles.header}>
            <div className={styles.identity}>
                <Link to="/" className={styles.logo}>NINJA ROBOT Pi0{robotType && ` - ${t(`robotType.${robotType}`)}`}</Link>
                <span role="status" className={`${styles.badge} ${status === 'connected' ? styles.active : ''}`}>
                    {t(status === 'connected' ? 'header.controllerActive' : `session.${status}`)}
                </span>
            </div>
            <Link to="/" className={styles.menuButton} aria-label={t('header.openMenu')}>
                <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                    <path d="M3 5h18M3 12h18M3 19h18" />
                </svg>
            </Link>
        </header>
    );
}

export default Header;
