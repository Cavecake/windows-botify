**⚠️ Maintenance Notice**

**This repository is still maintained, but the maintainer has switched to Linux.**
**As a result, while pull requests and bug fixes will be managed, the repository can no longer be tested on Windows.**
**Contributions and testing from the community are highly appreciated.**

# windows-botify
A simple package to allow mouse and window automatisation for windows

## Installation
To install the package run
```
pip install windows_botify
```

## Requirements
You will need to use Windows. The package was only tested on windows 10. But may also work on older or newer version

## How to get started
Currently only window interactions are supported.
You can get a screenshot of a window by runing:
```
import windows_botify

img = windows_botify.window.getWindowScreenshot(NAME)
```

Another useful function is to move the window to the foreground/background.
This can be achieved using:
```
import windows_botify

windows_botify.window.moveToForeground("GitHub Desktop")
windows_botify.window.minimizeWindow("GitHub Desktop")
```
To send a mouse click to a window use:
```
import windows_botify

windows_botify.mouse.ButtonDown("GitHub Desktop",windows_botify.mouse.MouseButton.LEFT)
windows_botify.mouse.ButtonUp("GitHub Desktop",windows_botify.mouse.MouseButton.LEFT)
```

## Documentation
For documentation check out our [wiki](https://github.com/Cavecake/windows-botify/wiki)