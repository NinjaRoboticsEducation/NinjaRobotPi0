import { useState, useRef, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import useRobotActivity from '../../hooks/useRobotActivity';
import SystemActivity from '../../components/common/SystemActivity';
import styles from './Agent.module.css';

function Agent() {
    const { t, i18n } = useTranslation();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [pendingMessages, setPendingMessages] = useState(0);
    const [isRecording, setIsRecording] = useState(false);
    const speechRecognitionRef = useRef(null);
    const messagesRef = useRef(null);
    const receiveCode = useCallback(data => {
        setMessages(previous => [...previous, { role: 'system', content: data.full_code || '' }]);
    }, []);
    const { logs, appendLog, clearLogs } = useRobotActivity(receiveCode);
    const isLoading = pendingMessages > 0;
    useEffect(() => () => {
        const recognition = speechRecognitionRef.current;
        if (recognition) {
            recognition.onstart = recognition.onend = recognition.onresult = recognition.onerror = null;
            recognition.abort();
            speechRecognitionRef.current = null;
        }
    }, []);
    useEffect(() => {
        if (messagesRef.current) messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }, [messages, pendingMessages]);

    const sendMessage = async () => {
        if (!input.trim()) return;
        const userMessage = input.trim();
        setInput('');
        setMessages(previous => [...previous, { role: 'user', content: userMessage }]);
        setPendingMessages(previous => previous + 1);
        try {
            const response = await fetch('/api/agent/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage, language: i18n.language }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`);
            setMessages(previous => [...previous, { role: 'assistant', content: data.response }]);
            if (data.log) appendLog(data.log);
        } catch {
            setMessages(previous => [...previous, { role: 'assistant', content: t('agent.error') }]);
        } finally { setPendingMessages(previous => Math.max(0, previous - 1)); }
    };
    const handleKeyPress = event => {
        if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing) {
            event.preventDefault();
            sendMessage();
        }
    };

    // Voice Input
    const toggleVoiceRecording = () => {
        if (isRecording) {
            speechRecognitionRef.current?.stop();
            setIsRecording(false);
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert(t('agent.speechNotSupported') || "Speech Recognition not supported.");
            return;
        }

        const recognition = new SpeechRecognition();
        speechRecognitionRef.current = recognition;

        const langMap = { 'en': 'en-US', 'ja': 'ja-JP', 'zh-tw': 'zh-TW', 'zh-cn': 'zh-CN' };
        recognition.lang = langMap[i18n.language.toLowerCase()] || 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => setIsRecording(true);
        recognition.onend = () => {
            if (speechRecognitionRef.current === recognition) speechRecognitionRef.current = null;
            setIsRecording(false);
        };
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            if (transcript) setInput(transcript);
        };
        recognition.onerror = () => setIsRecording(false);

        try {
            setIsRecording(true);
            recognition.start();
        } catch {
            speechRecognitionRef.current = null;
            setIsRecording(false);
        }
    };

    return (
        <div className={styles.agentPage}>
            <section className={styles.chatCard} aria-labelledby="conversation-title">
                <div className={styles.chatHeading}>
                    <h1 id="conversation-title">{t('agent.conversation')}</h1>
                    <button onClick={() => setMessages([])}>{t('agent.clearMessages')}</button>
                </div>
                <div className={styles.chatMessages} ref={messagesRef} role="log" aria-live="polite" aria-relevant="additions">
                    {messages.length === 0 && <div className={`${styles.chatBubble} ${styles.assistant}`}>{t('agent.welcome')}</div>}
                    {messages.map((message, index) => (
                        <div key={index} className={`${styles.chatBubble} ${styles[message.role]}`}>
                            {message.role === 'system' ? <pre>{message.content}</pre> : message.content}
                        </div>
                    ))}
                    {isLoading && <div className={`${styles.chatBubble} ${styles.assistant}`} aria-label={t('agent.replying')}>…</div>}
                </div>
            </section>
            <div className={styles.inputArea}>
                <textarea aria-label={t('agent.placeholder')} value={input} onChange={event => setInput(event.target.value)} onKeyDown={handleKeyPress}
                    placeholder={t('agent.placeholder')} className={styles.textInput} disabled={isRecording} rows={2} />
                <button className={styles.sendButton} onClick={sendMessage} disabled={!input.trim()} aria-label={t('agent.send')}>
                    <span aria-hidden="true">▶</span>
                </button>
            </div>
            <button className={`${styles.voiceButton} ${isRecording ? styles.recording : ''}`} onClick={toggleVoiceRecording}
                aria-label={t('agent.voice')} aria-pressed={isRecording}>
                <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                    <rect x="9" y="2" width="6" height="12" rx="3" />
                    <path d="M5 10v2a7 7 0 0 0 14 0v-2M12 19v3M8 22h8" />
                    {!isRecording && <path d="m2 2 20 20" />}
                </svg>
                {t('agent.voice')}
            </button>
            <SystemActivity logs={logs} onClear={clearLogs} />
        </div>
    );
}

export default Agent;
