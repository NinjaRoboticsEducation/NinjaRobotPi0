import { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import useRobotActivity from '../../hooks/useRobotActivity';
import useRobotStream from '../../hooks/useRobotStream';
import SystemActivity from '../../components/common/SystemActivity';
import styles from './Movement.module.css';

const controls = [
    { key: 'movements', listPath: '/api/servos/movements', field: 'movements', title: 'agent.movements', description: 'movement.movementsDescription', run: 'agent.runMovements', actionPath: name => `/api/servos/movements/${encodeURIComponent(name)}/execute` },
    { key: 'expressions', listPath: '/api/display/expressions', field: 'expressions', title: 'agent.expressions', description: 'movement.expressionsDescription', run: 'agent.runExpressions', actionPath: name => `/api/display/expressions/${encodeURIComponent(name)}` },
    { key: 'sounds', listPath: '/api/sound/emotions', field: 'emotions', title: 'agent.sounds', description: 'movement.soundsDescription', run: 'agent.runSounds', actionPath: name => `/api/sound/emotions/${encodeURIComponent(name)}` },
];

export default function Movement() {
    const { t } = useTranslation();
    const { logs, appendLog, clearLogs } = useRobotActivity();
    const [distance, setDistance] = useState(null);
    const [lists, setLists] = useState({});
    const [selected, setSelected] = useState({});
    const receiveDistance = useCallback(raw => {
        try {
            const data = JSON.parse(raw);
            const value = data.distance_mm ?? data.distance;
            setDistance(typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null);
        } catch { setDistance(null); }
    }, []);
    const clearDistance = useCallback(() => setDistance(null), []);
    useRobotStream('/ws/distance', receiveDistance, clearDistance);

    useEffect(() => {
        const abort = new AbortController();
        for (const control of controls) {
            const load = async () => {
                try {
                    const response = await fetch(control.listPath, { signal: abort.signal });
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    const data = await response.json();
                    const names = Array.isArray(data[control.field]) ? data[control.field].filter(name => typeof name === 'string') : [];
                    if (abort.signal.aborted) return;
                    setLists(previous => ({ ...previous, [control.key]: names }));
                    setSelected(previous => ({ ...previous, [control.key]: names[0] || '' }));
                } catch (error) {
                    if (!abort.signal.aborted) appendLog(`${control.key}: ${error.message}`);
                }
            };
            load();
        }
        return () => abort.abort();
    }, [appendLog]);

    const triggerAction = async control => {
        const name = selected[control.key];
        if (!name) return;
        try {
            const response = await fetch(control.actionPath(name), { method: 'POST' });
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP ${response.status}`);
            }
            appendLog(`${control.key}: ${name}`);
        } catch (error) { appendLog(`${control.key}: ${name}: ${error.message}`); }
    };

    return (
        <div className={styles.movementPage}>
            <section className={styles.card} aria-labelledby="distance-title">
                <h1 id="distance-title">{t('agent.distance')}</h1>
                <div className={styles.distance} role="status" aria-label={`${t('agent.distance')}: ${distance ?? t('movement.distanceUnavailable')} ${distance === null ? '' : t('agent.distanceUnit')}`}>
                    <span>{distance ?? '—'}</span><small>{distance === null ? t('movement.distanceUnavailable') : t('agent.distanceUnit')}</small>
                </div>
            </section>
            {controls.map(control => (
                <section className={styles.card} key={control.key} aria-labelledby={`${control.key}-title`}>
                    <h2 id={`${control.key}-title`}>{t(control.title)}</h2>
                    <p>{t(control.description)}</p>
                    <div className={styles.controlRow}>
                        <select aria-label={t(control.title)} value={selected[control.key] || ''} disabled={!lists[control.key]?.length} onChange={event => setSelected(previous => ({ ...previous, [control.key]: event.target.value }))}>
                            {!lists[control.key]?.length && <option value="">{t('movement.noActions')}</option>}
                            {(lists[control.key] || []).map(name => <option key={name} value={name}>{name}</option>)}
                        </select>
                        <button aria-label={t(control.run)} disabled={!selected[control.key]} onClick={() => triggerAction(control)}><span aria-hidden="true">▶</span></button>
                    </div>
                </section>
            ))}
            <SystemActivity logs={logs} onClear={clearLogs} />
        </div>
    );
}
