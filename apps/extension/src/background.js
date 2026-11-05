// TruthLens — service worker minimal (MV3).
// Rôle actuel : état on/off persistant. L'analyse elle-même vit dans
// le content script (locale) ou dans le backend (mode Pro temps réel).
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ truthlensEnabled: true });
});
