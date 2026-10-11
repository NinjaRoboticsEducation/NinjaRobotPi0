// Call synchronously from an interface-selection gesture; denial never blocks navigation.
export default function requestAppFullscreen() {
    const root = document.documentElement;
    if (document.fullscreenElement || document.webkitFullscreenElement) return;
    try {
        if (document.fullscreenEnabled && root.requestFullscreen) {
            root.requestFullscreen({ navigationUI: 'hide' }).catch(() => {});
        } else if (document.webkitFullscreenEnabled && root.webkitRequestFullscreen) {
            root.webkitRequestFullscreen()?.catch?.(() => {});
        }
    } catch { /* Unsupported or denied: retain the fitted browser viewport. */ }
}
