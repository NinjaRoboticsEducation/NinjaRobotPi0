import { useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';
import useRobotStream from './useRobotStream';

export default function useRobotActivity(onCodeReceived) {
    const { t } = useTranslation();
    const [logs, setLogs] = useState([]);
    const appendLog = useCallback(message => {
        setLogs(previous => [...previous, { time: Date.now(), message: String(message) }].slice(-50));
    }, []);
    const clearLogs = () => setLogs([]);
    const receive = useCallback(raw => {
        try {
            const data = JSON.parse(raw);
            if (data?.type === 'execute_received') {
                onCodeReceived?.(data);
                appendLog(t('activity.codeReceived', { count: data.code_length ?? 0 }));
            } else if (data?.type === 'execution_status') {
                appendLog(`${data.status}: ${data.message || ''}`);
            } else {
                appendLog(typeof data === 'string' ? data : (data?.message || JSON.stringify(data)));
            }
        } catch {
            appendLog(raw);
        }
    }, [appendLog, onCodeReceived, t]);
    const unavailable = useCallback(() => appendLog(t('activity.reconnecting')), [appendLog, t]);
    useRobotStream('/ws/events', receive, unavailable);
    return { logs, appendLog, clearLogs };
}
