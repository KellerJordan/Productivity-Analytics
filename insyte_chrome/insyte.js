chrome.tabs.onCreated.addListener((tab) => {
    if (tab.url) {
        console.log(`Opened tab ${tab.id} with URL ${tab.url}.`);
    }
});

chrome.tabs.onRemoved.addListener((tabId) => {
    console.log(`Closed tab ${tabId}`);
});

chrome.tabs.onUpdated.addListener((tabId, changes) => {
    if (changes.url) {
        console.log(`URL changed to ${changes.url} in tab ${tabId}.`);
    }
});

window.addEventListener("load", function(){
    // ....
    console.log("TEST");
});