**⚠️ Maintenance Notice**

**This repository will not be maintained.**

# windows-botify

A simple package to allow mouse and window automation for Windows

## Installation

To install the package, run:

```pip install windows_botify```

## Requirements

You will need to use Windows. The package was only tested on Windows 10 but may also work on older or newer versions.

## How to Get Started

Currently, only window interactions are supported.

### Get Window Screenshot

You can get a screenshot of a window by running:
```
import windows_botify

img = windows_botify.window.getWindowScreenshot("NAME")
```
### Move Window to Foreground/Background

Move the window to the foreground or minimize it:
```
import windows_botify

windows_botify.window.moveToForeground("GitHub Desktop")
windows_botify.window.minimizeWindow("GitHub Desktop")
```
### Send Mouse Click

To send a mouse click to a window:
```
import windows_botify

windows_botify.mouse.ButtonDown("GitHub Desktop", windows_botify.mouse.MouseButton.LEFT)
windows_botify.mouse.ButtonUp("GitHub Desktop", windows_botify.mouse.MouseButton.LEFT)
```
## Documentation

For more detailed documentation, check out our wiki: [https://github.com/Cavecake/windows-botify/wiki](https://github.com/Cavecake/windows-botify/wiki)
