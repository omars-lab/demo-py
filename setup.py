# -*- coding: utf8 -*-

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from subprocess import check_call

# https: // stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools

# Todo ... figure out how to only do these ... if the notebooks extras is installed ...

# class CustomDevelopCommand(develop):
#     """Custom Develop Command"""

#     def run(self):
#         develop.run(self)
#         print("Installing jupyter extension")
#         check_call("jupyter nbextension enable --py widgetsnbextension".split())


# class CustomInstallCommand(install):
#     """Custom Installation Command"""

#     def run(self):
#         install.run(self)
#         check_call("jupyter nbextension enable --py widgetsnbextension".split())


with open("README.md") as fh:
    long_description = fh.read()

setup(
    # Basic info
    name="demo-py",
    version="0.0.1",
    author='Omar Eid',
    author_email='contact.omar.eid@gmail.com',
    url='https://github.com/omars-lab/demo-py',
    description='My Personal Demo Toolbox.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    # cmdclass={
    #     "develop": CustomDevelopCommand,
    #     'install': CustomInstallCommand,
    # },
    # Packages and depencies
    packages=find_packages(include=["demopy", "demopy.*"]),
    install_requires=[
        "typer",        
        "pandas",
    ],
    extras_require={
        "notebooks": [
            "matplotlib",
            "igraph", # https://igraph.org/python/tutorial/0.9.8/install.html
            "plotly==5.18.0", # https://plotly.com/python/getting-started/
            "notebook", # https://jupyter.org/install
            # "ipython", # https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html
            "ipywidgets", # https://pypi.org/project/ipywidgets/
            "jupyter_contrib_nbextensions", # https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html
            "spacy", # https://spacy.io/usage
        ],
        'parsing': [
            'lark-parser'
            "spacy >= 2.3.2",
        ],
        'dev': [
            "mypy",
            "pytest",
            "pytest-pep8",
            "pytest-profiling",  # https://pypi.org/project/pytest-profiling/
            "pstats-view",  # https://github.com/ssanderson/pstats-view
            "flake8",
            # 'manuel',
            # 'pytest-cov',
            # 'coverage',
            # 'mock',
            # "nbconvert==5.5.0",
        ],
        "graph": [
            "py2cytoscape",
            "pycandela",
            "pygraphviz",
        ],
        "ext": [
            "mpldatacursor",  #(https://github.com/joferkington/mpldatacursor)
            "calmap",  #(https://github.com/martijnvermaat/calmap/blob/master/calmap/__init__.py),
            # "ipython[notebook]",
        ],
        "toolz": [
            "attrs",
            "pydantic",
            "toolz",  # https://toolz.readthedocs.io/en/latest/api.html
            "numpy",
            # 'Jinja2', # https://jinja.palletsprojects.com/en/3.0.x/intro/
        ],
        "chatgpt": [
            "openai", # https://platform.openai.com/docs/api-reference?lang=python
            "langchain", 
            "langchain-openai" # https://python.langchain.com/docs/integrations/platforms/openai
        ]
    },
    # Data files
    package_data={},
    # Scripts
    entry_points={
        'console_scripts': [
            'my-puml = demopy.cli.puml:app'
        ],
    },
    # Other configurations
    zip_safe=False,
    platforms='any'
)
