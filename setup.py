import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='kaldibin',
    version='0.3.0',
    author='Robert Gale',
    author_email='rcgale@gmail.com',
    packages=[
        'kaldibin',
        'kaldibin.adapters',
    ],
    url='https://github.com/rcgale/kaldibin',
    description='Python wrappers for Kaldi executables. Still in a partially-implemented, proof-of-concept stage.',
    install_requires=[],
)

