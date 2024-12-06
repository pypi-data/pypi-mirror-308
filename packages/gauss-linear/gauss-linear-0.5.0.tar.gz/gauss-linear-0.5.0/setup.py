from setuptools import setup, find_packages


from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'gauss-linear',
    version = '0.5.0',
    author = 'Rishi Rao',
    author_email = 'rao068048@gmail.com',
    license = 'MIT License',
    description = 'A simple command line tool to do linear algebra',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/22raor/gauss',
    py_modules = ['entry', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        gauss=entry:query
    '''
)
