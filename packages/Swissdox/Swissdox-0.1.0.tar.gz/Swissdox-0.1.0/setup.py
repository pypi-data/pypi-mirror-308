from setuptools import find_packages, setup

setup(
    name='Swissdox',
    packages=find_packages(),
    version='0.1.0',
    description='An SDK for the Swissdox@LiRI database.',
    author='nordinbensalem.dari@uzh.ch',
    install_requires=[
        'requests',
        'pyyaml',
        'python-dotenv',
        'jsonschema'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
