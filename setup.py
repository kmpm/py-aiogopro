from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='aiogopro',
    version='0.0.1a1',
    description='some kind of asyncio library for GoPro',
    url='http://github.com/kmpm/py-aiogopro',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Peter Magnusson',
    author_email='peter@birchroad.net',
    license='MIT',
    packages=['aiogopro'],
    install_requires=[
        'aiohttp==3.4.4'
    ],
    test_suite='tests',
    zip_safe=False)
