var port = chrome.runtime.connectNative("BackendPython");

function SendMessage(msg) {
    console.log(msg);
    port.postMessage({content: msg});
}

chrome.tabs.onCreated.addListener((tab) => {
    if (tab.url) {
        let msg = `Tab open (ID: ${tab.id}, URL: ${tab.url})`;

        SendMessage(msg);
    }
});

chrome.tabs.onRemoved.addListener((tabId) => {
    let msg = `Tab close ${tabId}`;

    SendMessage(msg);
});

chrome.tabs.onUpdated.addListener((tabId, changes) => {
    if (changes.url) {
        let msg = `Tab ${tabId} went to ${changes.url}`;

        SendMessage(msg);
    }
});

port.onMessage.addListener((msg) => {
    console.log(`Message received: (Counter: ${msg.count}, Content: ${msg.value.content})`);
});
