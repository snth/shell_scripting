from setuptools import setup

setup(
    name='ysass',
    version='0.1',
    py_modules=['hello', 'ysass'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hello=hello:hello
        ysass=ysass:cli
    ''',
)

