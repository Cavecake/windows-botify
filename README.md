# windows-botify
A simple package to allow keyboard and mouse automatisation for windows

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
import windows_botify.window

img = windows_botify.window.getWindowScreenshot(NAME)
```

Another useful function is to move the window to the foreground/background.
This can be achieved using:
```
import windows_botify.window

windows_botify.window.moveToForeground("GitHub Desktop")
windows_botify.window.minimizeWindow("GitHub Desktop")
```