from setuptools import setup

setup(
    name='fastcli',
    version='0.1',
    py_modules=['fastcli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        fastcli=nafc.__main__:cli
    ''',
)
