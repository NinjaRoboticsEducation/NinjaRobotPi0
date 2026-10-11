import { useEffect } from 'react';

// The visual viewport follows mobile browser chrome and the on-screen keyboard.
export default function useAppViewport() {
    useEffect(() => {
        const viewport = window.visualViewport;
        const update = () => {
            const root = document.documentElement;
            root.style.setProperty('--app-height', `${viewport?.height ?? window.innerHeight}px`);
            root.style.setProperty('--app-top', `${viewport?.offsetTop ?? 0}px`);
        };
        update();
        window.addEventListener('resize', update);
        viewport?.addEventListener('resize', update);
        viewport?.addEventListener('scroll', update);
        return () => {
            window.removeEventListener('resize', update);
            viewport?.removeEventListener('resize', update);
            viewport?.removeEventListener('scroll', update);
            document.documentElement.style.removeProperty('--app-height');
            document.documentElement.style.removeProperty('--app-top');
        };
    }, []);
}
