import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import styles from './SystemActivity.module.css';

export default function SystemActivity({ logs, onClear, onOpen }) {
    const { t, i18n } = useTranslation();
    const [open, setOpen] = useState(false);
    const contentRef = useRef(null);
    useEffect(() => {
        if (open && contentRef.current) contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }, [logs, open]);
    useEffect(() => {
        if (!open) return;
        const collapse = event => { if (event.key === 'Escape') setOpen(false); };
        document.addEventListener('keydown', collapse);
        return () => document.removeEventListener('keydown', collapse);
    }, [open]);
    return (
        <aside className={`${styles.panel} ${open ? styles.open : ''}`} aria-label={t('agent.systemLog')}>
            <button className={styles.tab} aria-expanded={open} aria-controls="robot-activity-log" onClick={() => { if (!open) onOpen?.(); setOpen(previous => !previous); }}>
                <span className={styles.handle} aria-hidden="true" />
                {t('agent.systemLog')} <span className={styles.count}>({logs.length})</span>
            </button>
            <div id="robot-activity-log" hidden={!open} className={styles.body}>
                <div className={styles.heading}>
                    <h2>{t('agent.systemLog')}</h2>
                    <button onClick={onClear}>{t('activity.clear')}</button>
                </div>
                <div className={styles.entries} ref={contentRef} role="log" aria-live="polite" aria-relevant="additions">
                    {logs.length === 0 ? <p>{t('agent.logEmpty')}</p> : logs.map((log, index) => (
                        <div className={styles.entry} key={`${log.time}-${index}`}>
                            <time dateTime={new Date(log.time).toISOString()}>{new Date(log.time).toLocaleTimeString(i18n.language)}</time>
                            <span>{log.message}</span>
                        </div>
                    ))}
                </div>
            </div>
        </aside>
    );
}
