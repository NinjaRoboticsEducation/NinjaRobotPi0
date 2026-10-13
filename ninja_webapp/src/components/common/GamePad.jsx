import { useTranslation } from 'react-i18next';
import styles from './GamePad.module.css';

const directions = ['up', 'left', 'center', 'right', 'down'];
export default function GamePad({ actions, controller }) {
    const { t } = useTranslation();
    const { pressed, busy, uncertain, press, release } = controller;
    return (
        <div className={styles.wrapper}>
            <div className={styles.pad} role="group" aria-label={t('gamepad.title')}>
                {directions.map(direction => (
                    <button key={direction} type="button" data-direction={direction}
                        className={`${styles.button} ${styles[direction]} ${pressed === direction ? styles.pressed : ''}`}
                        aria-label={t(`gamepad.${direction}`)} aria-pressed={pressed === direction}
                        aria-describedby="gamepad-guidance"
                        title={!actions[direction] ? t('gamepad.actionUnavailable') : undefined}
                        disabled={!actions[direction] || uncertain || ((busy || Boolean(pressed)) && pressed !== direction)}
                        onPointerDown={event => {
                            if (event.button !== 0 || !event.isPrimary || event.currentTarget.disabled) return;
                            event.preventDefault();
                            // Clear the previous button's blur before creating a new hold.
                            event.currentTarget.focus();
                            const source = `pointer:${event.pointerId}`;
                            if (press(direction, source)) {
                                try { event.currentTarget.setPointerCapture(event.pointerId); }
                                catch { release(source); }
                            }
                        }}
                        onPointerUp={event => release(`pointer:${event.pointerId}`)}
                        onPointerCancel={event => release(`pointer:${event.pointerId}`)}
                        onLostPointerCapture={event => release(`pointer:${event.pointerId}`)}
                        onKeyDown={event => {
                            if (![' ', 'Enter'].includes(event.key)) return;
                            event.preventDefault();
                            if (!event.repeat) press(direction, `key:${event.key}`);
                        }}
                        onKeyUp={event => {
                            if (![' ', 'Enter'].includes(event.key)) return;
                            event.preventDefault();
                            release(`key:${event.key}`);
                        }}
                        onBlur={() => release()}
                        onClick={event => {
                            // Assistive activation has no hold duration: execute exactly once.
                            if (event.detail === 0 && press(direction, 'assistive')) release('assistive');
                        }}>
                        <svg viewBox="0 0 40 40" aria-hidden="true">
                            {direction === 'center' ? <circle cx="20" cy="20" r="12" /> : <path d="M20 8 33 31H7Z" />}
                        </svg>
                    </button>
                ))}
            </div>
            <p id="gamepad-guidance" className={styles.guidance} role="status">
                {t(uncertain ? 'gamepad.uncertain' : busy && !pressed ? 'gamepad.finishing' : !Object.values(actions).some(Boolean) ? 'gamepad.unavailable' : 'gamepad.guidance')}
            </p>
        </div>
    );
}
