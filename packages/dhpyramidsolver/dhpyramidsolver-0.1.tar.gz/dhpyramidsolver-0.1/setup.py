from setuptools import setup, find_packages

setup(
    name="dhpyramidsolver",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'print-flag=dhpyramidsolver.main:print_flag'
        ]
    },
)
