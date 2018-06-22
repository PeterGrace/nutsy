from setuptools import setup, find_packages

setup(
    name='nutsy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'setuptools-lint',
        'pytest',
    ],
    entry_points='''
        [console_scripts]
        nutsy=nutsy.main:main
    ''',
)
