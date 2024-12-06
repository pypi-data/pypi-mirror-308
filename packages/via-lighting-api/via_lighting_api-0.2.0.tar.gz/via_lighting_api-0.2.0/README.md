# via-lighting-api

This Python API provides an interface for controlling the RGB lighting of keyboards that support the VIA protocol. It allows you to dynamically change the brightness, effect, effect speed, and color of the lighting.

## Features

- Set lighting brightness
- Set lighting effect
- Set lighting effect speed
- Set lighting color in RGB or HSV format (HS only)
- Set absolute lighting color (real RGB color instead of HS only)
- Save lighting settings to EEPROM

## Requirements

- Python 3.x

## Installation

```shell
pip install via-lighting-api
```

## Usage

> See a full example code in `example.py`.

### Init

First, import the `ViaLightingAPI` class from the module where it’s defined:

```python
from via_lighting_api import ViaLightingAPI
```

To initialize the API and control the lighting, you need to know the Vendor ID (VID) and Product ID (PID) of your keyboard. If you don't know these values, run: `via-lighting-api --list-devices` and follow the hint to find them.

```python
# Replace with your keyboard's VID and PID
vid = 0x1234
pid = 0xABCD

# Initialize the API
api = ViaLightingAPI(vid, pid)
```

### Set Brightness

```python
# Set brightness to maximum
api.set_brightness(255)
```

### Set Effect

```python
# Set effect to 'Rainbow Moving Chevron'
api.set_effect(15)
```

### Set Effect Speed

```python
# Set effect speed to medium
api.set_effect_speed(127)
```

### Set Color

```python
# Set color to red (in RGB)
api.set_color([255, 0, 0])

# Set color to blue (in HSV)
api.set_color([170, 255])
```

### Set Absolute Color

```python
# Set absolute color to purple
api.set_color_abs([128, 0, 128])
```

### Save Settings

```python
# Save current lighting settings to EEPROM
api.save()
```

## Troubleshooting

If your device is not detected, ensure that it is connected properly and that you have the correct VID and PID. Also, check that your keyboard firmware supports VIA control.

## Disclaimer

This API provides an interface that can send user-defined commands directly to your device, which may cause unexpected results if used improperly. Make sure you fully understand the VIA protocol and the commands you are sending.

## License

This API is open-source and can be used and modified by anyone. Please respect the original author’s work when using or distributing this software.
