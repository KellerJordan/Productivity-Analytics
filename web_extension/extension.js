browser.tabs.onCreated.addListener((tab) => {
    if (tab.url) {
        console.log(`Opened tab ${tab.id} with URL ${tab.url}.`);
    }
});

browser.tabs.onRemoved.addListener((tabId) => {
    console.log(`Closed tab ${tabId}`);
});

browser.tabs.onUpdated.addListener((tabId, changes) => {
    if (changes.url) {
        console.log(`URL changed to ${changes.url} in tab ${tabId}.`);
    }
});
