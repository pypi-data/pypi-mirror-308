from setuptools import setup, find_packages

setup(
    name="pagify",
    version='1.0.1',
    author='Mohammad Eslami',
    description='A lightweight and flexible pagination package for Python applications.',
    long_description=open('docs/pypi.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mohammad222PR/pagify',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',

    keywords='pagination python api adapter utilities',
)
