async function HandleMessages(msg) {
    switch (msg.action) {
        case ContentAction.BLOCKPAGE: {
            BlockPage(msg.reason);
            break;
        }
        case ContentAction.GETLINKS: {
            let pageLinks = FetchLinks();
            let dumpMsg = {
                type: ContentResponse.GETLINKS,
                links: pageLinks
            };
            await chrome.runtime.sendMessage(dumpMsg);
            break;
        }
        case ContentAction.BLOCKLINKS: {
            let pageLinks = document.getElementsByTagName('a');
            let linkStatus = msg.linkStatus;

            for (var i = 0; i < pageLinks.length; ++i) {
                if (linkStatus[i]) {
                    pageLinks[i].className += ' suspicious-link';
                }
            }
            break;
        }
    }
}

chrome.runtime.onMessage.addListener(HandleMessages);

function FetchLinks() {
	var urls = [];
    var pageLinks = document.getElementsByTagName('a');

    for (var link of pageLinks) {
        if (link.href) {
            urls.push(link.href);
        }
    }
    return urls;
}

function BlockPage() {
    document.body.innerHTML = '<h1>Blocked!</h1><br />';

    if (reason) {
        document.body.innerHTML += 'Reason:' + reason;
    }
}
