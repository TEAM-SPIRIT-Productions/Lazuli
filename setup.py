# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
]

setup(
    name="lazuli",
    version="0.0.3",
    description="A Python-based tool for interacting with AzureMSv316-based databases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TEAM-SPIRIT-Productions/Lazuli",
    author="Amos Chua",
    classifiers=classifiers,
    keywords="database, azure, maplestory",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["mysql-connector-python-rf"],
)
