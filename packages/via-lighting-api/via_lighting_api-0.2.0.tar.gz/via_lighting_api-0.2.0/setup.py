from setuptools import setup

VERSION_NUM = '0.2.0'

setup(
    name="via-lighting-api",
    version=VERSION_NUM,
    py_modules=['via_lighting_api'],
    packages=['tools'],
    install_requires=[
        "hidapi"
    ],
    entry_points={
        "console_scripts": [
            "via-lighting-api=via_lighting_api:main",
        ],
    },
    author='JerryZhangZZY',
    author_email='JerryZhang20010417@outlook.com',
    description='This Python API provides an interface for controlling the RGB lighting of keyboards that support the VIA protocol. It allows you to dynamically change the brightness, effect, effect speed, and color of the lighting.',
    license='MIT',
    keywords='via api',
    url='https://github.com/JerryZhangZZY/via-lighting-api',
)
