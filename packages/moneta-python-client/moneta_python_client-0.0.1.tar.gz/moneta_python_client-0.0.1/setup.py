from setuptools import setup, find_packages
from setuptools.command.install import install
import sys
class PreventInstallCommand(install):
    """Prevent installation for this package."""
    def run(self):
        sys.exit("** THIS PACKAGE IS NOT TO BE DOWNLOADED FROM PUBLIC PYPI REPOSITORY! **")
setup(
    # package metadata
    name="moneta-python-client",
    description="Moneta python client",
    url="https://www.moneylion.com",
    author="moneylion",
    author_email="customercare@moneylion.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # package setup
    packages=find_packages(exclude=("tests", "docs")),
    version="0.0.1",
    # requirements
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'install': PreventInstallCommand,
    },
)
