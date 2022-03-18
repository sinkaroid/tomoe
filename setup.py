import re
from setuptools import setup

version = ''
with open('tomoe/__init__.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md', encoding="utf8") as f:
    readme = f.read()

setup(
    name='tomoe',
    author='sinkaroid',
    author_email='anakmancasan@gmail.com',
    version=version,
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/sinkaroid/tomoe',
    project_urls={
        "Documentation": "https://sinkaroid.github.io/tomoe",
        "Issue tracker": "https://github.com/sinkaroid/tomoe/issues/new/choose",
        "Funding": "https://paypal.me/sinkaroid",
    },
    packages=['tomoe', 'tomoe.utils'],
    license='MIT',
    classifiers=[
        "Framework :: AsyncIO",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Environment :: Console",
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Games/Entertainment",

    ],
    description='A doujinshi downloader for mankind',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tomoe = tomoe:main',
        ]
    },
    install_requires=requirements,
)
