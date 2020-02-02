from distutils.core import setup

setup(
    name='DinnerPartyDatabase',
    version='1',
    packages=['dinner_party_database',],
    long_description=open('README.md').read(),
    install_requires=[
       'pymongo',
        'dnspython',
        'datetime',
        'google-cloud-pubsub'
    ]
)