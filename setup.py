import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ('voteit.core',
            'voteit.irl',
            'fanstatic',)

setup(name='sverok_rm',
      version='2015',
      description='sverok_rm',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='VoteIT development team',
      author_email='info@voteit.se',
      url='https://github.com/Sverok',
      keywords='web pyramid pylons voteit sverok',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="sverok_rm",
      entry_points = """\
      [fanstatic.libraries]
      sverok_lib = sverok_rm.fanstaticlib:sverok_lib
      """,
      )

