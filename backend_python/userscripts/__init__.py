import os
import sys

userFunctions = []
userscriptsDir = os.path.dirname(os.path.abspath(__file__))

for entry in os.scandir(userscriptsDir):
    if not entry.is_file():
        continue

    filename = entry.name

    if not filename.endswith('.py') or filename.startswith('__'):
        continue

    # Remove the .py extension from the basename
    strippedName = entry.name[:-3]
    moduleName = 'userscripts.' + strippedName

    __import__(moduleName)
    userFunctions.append(sys.modules[moduleName].run)

def execute(data):
    results = []

    for fn in userFunctions:
        fnResult = fn(data)

        if fnResult is not None:
            results.append(fnResult)

    return results
