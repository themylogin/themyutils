import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()

requires = []

setup(name="themyutils",
      version="0.0",
      description="",
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        ],
      author="themylogin",
      author_email="",
      url="https://github.com/themylogin/themyutils",
      keywords="",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="themyutils",
      install_requires=requires,
      )
