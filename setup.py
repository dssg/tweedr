from setuptools import setup, command
import os
import sys
import urllib
import tarfile

'''setuptools works by triggering subcommands from higher level commands.
The default commands 'install' and 'develop' trigger the following sequences:

install:
  1. build
  2. build_py
  3. install_lib
  4. install_egg_info
  5. egg_info
  6. install_scripts

develop:
  1. egg_info
  2. build_ext
'''


def download_ark_tweet_nlp():
    url = 'http://ark-tweet-nlp.googlecode.com/files/ark-tweet-nlp-0.3.2.tgz'
    local_jar_dir = 'ext'
    print >> sys.stderr, 'Downloading', url
    tgz_filepath, headers = urllib.urlretrieve(url)
    print >> sys.stderr, 'Opening', tgz_filepath
    with tarfile.open(tgz_filepath, 'r:gz') as tgz:
        # pull all the jars out, flattening them
        for tarinfo in tgz.getmembers():
            if tarinfo.name.endswith('.jar'):
                tarinfo_name = tarinfo.name
                local_filepath = os.path.join(local_jar_dir, os.path.basename(tarinfo.name))
                tarinfo.name = local_filepath
                tgz.extract(tarinfo)
                print >> sys.stderr, 'Extracting %s to %s' % (tarinfo_name, local_filepath)


class install_data(command.install.install):
    def run(self):
        download_ark_tweet_nlp()


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
        'pattern',
    ],
    entry_points={
        'console_scripts': [
            'tweedr-ui = tweedr.ui:main',
        ],
    },
    cmdclass={
        # this is a built-in command for distutils, but I just override it here
        'install_data': install_data,
    },
    tests_require=['pep8'],
    test_suite='tests',
)
