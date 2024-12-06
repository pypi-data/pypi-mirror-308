from setuptools import setup

setup(
    install_requires=[
        "cffi==1.17.1",
        "cryptography==43.0.3",
        "pycparser==2.22",
        "pyjwt[crypto]==2.9.0",
    ],
    dependency_links=[],
)
