from distutils.core import setup

try:
    longdescription = open('README.md').read()
except EnvironmentError:
    longdescription = 'web interface'

setup(
    name='web-core',
    version='0.2',
    author='Storj',
    author_email='storj@example.com',
    modules=['accounts', 'index', 'settings', 'cloudsync', ],
    scripts=[],
    url='https://github.com/Storj/web-core',
    license='TBD',
    description='TBD',
    long_description=longdescription,
    install_requires=[
        'pycrypto >= 2.6.1',
    ],
    extras_require={
        'test': [
            'tox',
        ]
    }
)
