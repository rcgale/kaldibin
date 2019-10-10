from distutils.core import setup

setup(
    name='kaldibin',
    version='0.1.0',
    author='Robert Gale',
    author_email='rcgale@gmail.com',
    packages=[
        'kaldibin',
        'kaldibin.adapters',
    ],
    url='https://www.github.com/galer/kaldibin',
    entry_points={
        'console_scripts': [
        ],
    },
    install_requires=[
    ],
)
