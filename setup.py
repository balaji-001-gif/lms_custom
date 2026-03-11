import sys
from setuptools import setup, find_packages

setup(
    name="lms_custom",
    version="0.0.1",
    description="LMS Custom Injector",
    author="Admin",
    author_email="admin@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
