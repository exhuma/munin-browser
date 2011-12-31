from setuptools import setup

setup(
    name= "munin-browser",
    version=__import__( "muninbrowser").__version__,
    description= "An alternative web-interface for munin",
    long_description=open("README.rst").read(),
    packages=['muninbrowser'],
    author= "Michel Albert",
    author_email= "michel@albert.lu",
    license="LICENSE.txt",
    include_package_data=True,
    install_requires = [
      'Flask',
      'unittest2',
      ],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['munin-browser = muninbrowser.serve:main']
        },
    test_suite = 'tests'
)

