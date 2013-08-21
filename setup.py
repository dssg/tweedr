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
from setuptools import setup, find_packages
from distutils import log, core
from distutils.dir_util import remove_tree
import os
import json

here = os.path.dirname(__file__) or os.curdir
package = json.load(open(os.path.join(here, 'package.json')))


class download_ext(core.Command):
    description = 'download external dependencies'
    user_options = []

    def initialize_options(self):
        self.ext_path = None

    def finalize_options(self):
        self.ext_path = os.path.join(here, 'ext')

    def download_ark_tweet_nlp(self):
        import urllib
        import tarfile
        url = 'http://ark-tweet-nlp.googlecode.com/files/ark-tweet-nlp-0.3.2.tgz'
        log.info('Downloading %s', url)
        tgz_filepath, headers = urllib.urlretrieve(url)
        log.info('Opening %s', tgz_filepath)
        with tarfile.open(tgz_filepath, 'r:gz') as tgz:
            # pull all the jars out, flattening them
            for tarinfo in tgz.getmembers():
                if tarinfo.name.endswith('.jar'):
                    tarinfo_name = tarinfo.name
                    local_filepath = os.path.join(self.ext_path, os.path.basename(tarinfo.name))
                    tarinfo.name = local_filepath
                    tgz.extract(tarinfo)
                    log.info('Extracting %s to %s', tarinfo_name, local_filepath)

    def run(self):
        self.mkpath(self.ext_path)
        self.download_ark_tweet_nlp()


class dist_clean(core.Command):
    description = 'remove all files not under version control'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        # set all = True for the benefit of the "clean" subcommand
        self.all = True

    def run(self):
        self.run_command('clean')
        log.debug('removing inessential directories from root')
        for directory in os.listdir(here):
            if directory.endswith(('dist', 'ext', '.egg', '.egg-info')):
                remove_tree(directory, dry_run=self.dry_run)

        log.debug('removing inessential files from project')
        for dirpath, _, filenames in os.walk('.'):
            filepaths = [os.path.join(dirpath, filename) for filename in filenames]
            for filepath in filepaths:
                if filepath.endswith(('.pyc', '.DS_Store')):
                    log.info('rm %s', filepath)
                    if self.dry_run:
                        continue
                    os.remove(filepath)

setup(
    name='tweedr',
    version=str(package['version']),
    url=str(package['homepage']),
    license=open(os.path.join(here, 'LICENSE')).read(),
    packages=find_packages(),
    install_requires=[
        'bottle',
        'colorama',
        'mako',
        'matplotlib',
        'mrjob',
        'mysql-python',
        'pattern',
        'pybloomfiltermmap>=0.3.11',
        'pyper',
        'python-hashes',
        'requests',
        'scikit-learn',
        'scipy',
        'sqlalchemy',
        'ujson',
    ],
    entry_points={
        'console_scripts': [
            'tweedr-ui = tweedr.cli.ui:main',
            'tweedr-database = tweedr.cli.database:main',
            'tweedr-pipeline = tweedr.cli.pipeline:main',
        ],
    },
    cmdclass={
        'download_ext': download_ext,
        'dist_clean': dist_clean,
    },
    tests_require=[
        'nose',
        'pep8',
        'pyflakes',
    ],
    test_suite='nose.collector',
)
