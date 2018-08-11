import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

requires = [
    'boto3',
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'transaction',
    'waitress',
]

setup(name='tinyurl',
      version='0.0',
      description='tinyurl',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Eric Hanchrow',
      author_email='eric.hanchrow@gmail.com',
      url='http://teensy.info',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tinyurl',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = tinyurl:main
      [console_scripts]
      initialize_tinyurl_db = tinyurl.scripts.initializedb:main
      """, )
