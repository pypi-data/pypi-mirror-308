from setuptools import find_packages, setup

classifiers = [
    'Development Status :: Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Ubuntu',
    'License :: OSI Approved :: MIT License',
    'Programmming Language :: Python :: 3'
]

setup(
    name='my_bot_library',
    version='0.0.2',
    description='Andromeda Python library',
    long_description=open('README.md').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Susheela',
    license='MIT',
    #classifiers=classifiers,
    keywords='andromeda',
    packages=find_packages(),
)
