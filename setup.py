import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ('voteit.core',
            'voteit.irl',)

setup(name='sverok_rm',
      version='2011',
      description='sverok_rm',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='https://github.com/Sverok',
      keywords='web pyramid pylons voteit sverok',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="sverok_rm",
      entry_points = """\
      [console_scripts]
      participants_import = sverok_rm.scripts.participants_import:participants_import
      delegate_numbers = sverok_rm.scripts.delegate_numbers:delegate_numbers
      [fanstatic.libraries]
      sverok_rm_lib = sverok_rm.fanstaticlib:sverok_rm_lib
      """,
      paster_plugins=['pyramid'],
      message_extractors = { '.': [
              ('**.py',   'lingua_python', None ),
              ('**.pt',   'lingua_xml', None ),
              #The ZCML extractor seems broken in lingua, but since it's ZCML is XML this works. /robinharms
              ('**.zcml',   'lingua_xml', None ),
              ]},
      )

