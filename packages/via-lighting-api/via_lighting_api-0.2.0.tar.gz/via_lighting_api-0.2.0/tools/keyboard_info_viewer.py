"""
This tools helps you find your keyboard's vendor id and product id.
The API relies on these ids to communicate with your keyboard.
"""

import hid

def list_devices():
    """
    Print hint
    """
    print("Use \'product_string\' to locate your keyboard and copy it's \'vendor_id\' and \'product_id\':\n")

    for device_dict in hid.enumerate():
        print(device_dict)

if __name__ == '__main__':
    list_devices()
