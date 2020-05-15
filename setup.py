from setuptools import setup

setup(
    name='formisp',
    version='0.0.1',
    py_modules=['formisp'],
    entry_points={
        'console_scripts': [
            'formisp=formisp:main',
        ],
    },
)
