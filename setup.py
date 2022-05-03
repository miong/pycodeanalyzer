import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="pycodeanalyzer",
    version="0.0.6",
    url="https://github.com/miong/pycodeanalyzer",
    license='MIT',
    long_description_content_type="text/x-rst",

    author="Giovanni Mion",
    author_email="mion.ggb@gmail.com",

    description="Code analyzer to get information to help developers to understand how projects works.",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests','tools',)),

    install_requires=[
        "robotpy-cppheaderparser==5.0.16",
        "Flask==2.0.3",
        "Flask-SocketIO==5.1.1",
        "Flask-Classful==0.14.2",
        "flaskwebgui==0.3.4",
        "simple-websocket==0.5.1",
        "injector==0.19.0",
        "pathlib==1.0.1",
        'python-magic-bin==0.4.14;platform_system!="Linux"',
        'python-magic==0.4.25;platform_system=="Linux"',
        "pcpp==1.30",
        "astroid==2.11.0",
        "javalang==0.13.0",
        "kopyt==0.0.2",
        "simplejson==3.17.6",
        "jsonpickle==2.1.0",
    ],

    extras_require={
        'dev': [
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "coverage",
            "black",
            "isort",
            "flake8",
            "mypy",
            "bumpversion",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinxcontrib-mermaid",
            "sphinxcontrib-plantuml",
            "better-apidoc",
            "six",
        ]
    },

    package_dir={'pycodeanalyzer': 'pycodeanalyzer'},
    package_data={'pycodeanalyzer': [
        'ui/web/static/css/*.css',
        'ui/web/static/css/libs/*.css',
        'ui/web/static/js/*.js',
        'ui/web/static/js/libs/*.js',
        'ui/web/templates/*.html'
    ]},

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    entry_points={
        "console_scripts": [
            "pycodeanalyzer=pycodeanalyzer.__main__:main",
        ]
    },
)
