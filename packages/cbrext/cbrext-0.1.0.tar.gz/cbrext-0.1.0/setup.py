from setuptools import setup, find_packages

setup(
    name='cbrext',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas ~= 2.2.2'
    ],
    entry_points={
        'console_scripts': [
            'cbrext = src.cli:main',
        ],
    },
    author='kimbank',
    author_email='kimbank@kimbank.dev',
    description='This tool extracts the Compressed Beamforming Report data from a PCAP file and saves it to a JSON file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kimbank/cbr-extractor',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
)
