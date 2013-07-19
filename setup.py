from setuptools import setup

setup(
    name='tweedr',
    version='0.0.2',
    packages=['tweedr'],
    install_requires=[
        'colorama',
        'mysql-python',
        'scikit-learn',
        'sqlalchemy',
        'tweepy',
        'tweetstream',
        'twython',
        'ujson',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    tests_require=['pep8'],
    test_suite='tests',
)
