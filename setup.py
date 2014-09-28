from distutils.core import setup

setup(
    name='phabulous',
    version='0.1.2',
    author='Will Larson',
    author_email='lethain@gmail.com',
    packages=['phabulous', 'phabulous.tests'],
    url='http://pypi.python.org/pypi/phabulous/',
    license='LICENSE.txt',
    description='Pythonic abstraction for python-habricator library.',
    long_description=open('README.rst').read(),
    install_requires=[
        "phabricator",
        "lazy",
        ],
)
