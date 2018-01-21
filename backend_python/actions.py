from collections import namedtuple

class ActionType():
    BlockPage = 0
    GetLinks = 1
    BlockLinks = 2

class MessageType():
    TabOpen = 0
    TabClose = 1
    LinkDump = 2
    UrlGoto = 3

_GenericAction = namedtuple('_GenericAction', 'type')

def GetLinks(tabId):
    return {'type': ActionType.GetLinks, 'id': tabId}

def BlockPage(tabId, reason=None):
    msgObj = {'type': ActionType.BlockPage, 'id': tabId}

    if reason is not None:
        msgObj['reason'] = reason

    return msgObj

def BlockLinks(tabId, linkArray):
    return {'type': ActionType.BlockLinks, 'id': tabId, 'links': linkArray}
