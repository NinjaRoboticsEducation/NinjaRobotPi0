import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import LanguageSelector from '../../components/common/LanguageSelector';
import PowerOffSlider from '../../components/common/PowerOffSlider';
import styles from './Home.module.css';

function Home() {
    const { t } = useTranslation();
    return (
        <div className={styles.homePage}>
            <h1>{t('home.welcome')}</h1>
            <section className={styles.block} aria-labelledby="language-title">
                <h2 id="language-title">{t('language.label')}</h2>
                <p>{t('home.languageDescription')}</p>
                <LanguageSelector />
            </section>
            <section className={styles.block} aria-labelledby="controls-title">
                <h2 id="controls-title">{t('home.controlTitle')}</h2>
                <p>{t('home.movementDescription')}</p>
                <Link to="/movement" className={styles.movementAction}>
                    <span aria-hidden="true">⚙</span> {t('home.movementButton')}
                </Link>
                <p>{t('home.chatDescription')}</p>
                <Link to="/agent" className={styles.chatAction}>
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M4 4h16v13H8l-4 4Z" /></svg>
                    {t('home.chatButton')}
                </Link>
            </section>
            <section className={styles.block} aria-labelledby="power-title">
                <h2 id="power-title">{t('home.systemTitle')}</h2>
                <p>{t('home.powerDescription')}</p>
                <PowerOffSlider />
            </section>
        </div>
    );
}

export default Home;
