from os import path
import codecs
from setuptools import setup

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name='django-appconf',
    version=":versiontools:appconf:",
    description='An app configuration object to be used for handling '
                'configuration defaults of packaged apps gracefully.',
    long_description=read(path.join(path.dirname(__file__), 'README.rst')),
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='https://github.com/jezdez/django-appconf/',
    py_modules=['appconf'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    setup_requires=[
        'versiontools >= 1.5',
    ],
)
