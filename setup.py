import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='kaldibin',
    version='0.6.0',
    author='Robert Gale',
    author_email='rcgale@gmail.com',
    packages=[
        'kaldibin',
        'kaldibin.adapters',
    ],
    url='https://github.com/rcgale/kaldibin',
    description='Python wrappers for Kaldi executables. Still in a partially-implemented, proof-of-concept stage.',
    install_requires=[
        "docstring-parser==0.7.3"
    ],
    entry_points={
        'console_scripts': [
            'kaldi-compute-mfcc-feats=kaldibin.featbin:compute_mfcc_feats',
            'kaldibin-config=kaldibin.adapters.context:configure',
        ]
    },

)

