from setuptools import find_packages, setup

setup(
    name="themyutils",
    version="0.0.0",
    author="themylogin",
    author_email="themylogin@gmail.com",
    packages=find_packages(exclude=["tests"]),
    scripts=[],
    test_suite="nose.collector",
    url="http://github.com/themylogin/themyutils",
    description="Common python utils used in themylogin's software",
    long_description=open("README.md").read(),
    install_requires=[
        "Flask",
        "pytils",
        "redis",
    ],
    setup_requires=[
        "nose>=1.0",
    ],
)
