var backendPort = chrome.runtime.connectNative("BackendPython");

chrome.tabs.onCreated.addListener((tab) => {
    if (tab.url) {
        let msg = {
            type: MessageType.TABOPEN,
            id: tab.id,
            url: tab.url
        };
        backendPort.postMessage(msg);
    }
});

chrome.tabs.onRemoved.addListener((tabId) => {
    let msg = {
        type: MessageType.TABCLOSE,
        id: tabId
    };
    backendPort.postMessage(msg);
});

chrome.tabs.onUpdated.addListener((tabId, changes) => {
    if (changes.url) {
        let msg = {
            type: MessageType.URLGOTO,
            id: tabId,
            url: changes.url
        };
        backendPort.postMessage(msg);
    }
});

async function OnBackendMessage(msg) {
    console.log('Messages received:');

    for (let m of msg.messages) {
        console.log(m);

        switch (m.type) {
            case ResponseType.GETLINKS: {
                let dumpMsg = {
                    action: ContentAction.GETLINKS
                };
                let tabId = m.id;

                await chrome.tabs.sendMessage(tabId, dumpMsg);
                break;
            }
            case ResponseType.BLOCKPAGE: {
                let blockMsg = {
                    action: ContentAction.BLOCKPAGE,
                    reason: m.reason
                };
                let tabId = m.id;

                await chrome.tabs.sendMessage(tabId, blockMsg);
                break;
            }
            case ResponseType.BLOCKLINKS: {
                let blockMsg = {
                    action: ContentAction.BLOCKLINKS,
                    linkStatus: m.links
                };
                let tabId = m.id;

                await chrome.tabs.sendMessage(tabId, blockMsg);
                break;
            }
        }
    }
}

backendPort.onMessage.addListener(OnBackendMessage);

function processContentMsg(msg, sender) {
    console.log(`Content message: ${msg}`);

    switch (msg.type) {
        case ContentResponse.GETLINKS:
            let dumpMsg = {
                id: sender.tab.id,
                type: MessageType.LINKDUMP,
                links: msg.links
            };
            console.log(dumpMsg.links);
            backendPort.postMessage(dumpMsg);
            break;
    }
}

chrome.runtime.onMessage.addListener(processContentMsg);
