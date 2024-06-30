"""
Package setup.
"""


from setuptools import find_packages, setup


with open('README.md', encoding='utf-8') as file:
    long_description = file.read()


setup(
    name = 'pokerpy', # Installation name (pip install <name>)
    version = '0.4.0',
    description = 'Python poker playability framework (under development)',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Andrés Saldarriaga Jordan',
    author_email = 'andresaldarriaga.94@gmail.com',
    maintainer = 'Andrés Saldarriaga Jordan',
    maintainer_email = 'andresaldarriaga.94@gmail.com',
    url = 'https://github.com/jorsaland/pokerpy',
    download_url = 'https://github.com/jorsaland/pokerpy/archive/refs/tags/0.4.0.tar.gz',
    packages = find_packages(),
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    include_package_data = True,
)