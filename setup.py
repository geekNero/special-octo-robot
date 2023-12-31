from pathlib import Path
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()


def get_version():
    """Parse package __version__.py to get version."""
    versionpy = (Path('app') / '__version__.py').read_text()
    return versionpy.split("'")[1]


VERSION = get_version()

setup(
    name = 'devcord',
    version = VERSION,
    author = 'Jahan Chaware',
    author_email = 'sg550js@gmail.com',
    license = 'GNU GENERAL PUBLIC LICENSE',
    description = 'Creating my own version of what a CLI Task manager and To-do-list would look like',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/geekNero/special-octo-robot.git',
    py_modules = ['devcord', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        'console_scripts': [
            'devcord=devcord:cli',
        ],
    },
)