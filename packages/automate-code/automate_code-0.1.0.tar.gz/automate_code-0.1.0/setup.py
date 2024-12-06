# setup.py

from setuptools import setup, find_packages

setup(
    name='automate_code',
    version='0.1.0',
    description='A Django management command to generate views and serializers for models automatically',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/automate_code',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['Django>=3.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
    ],
    entry_points={
        'console_scripts': [
            'automate_code=automate_code.management.commands.code_generator:Command',
        ],
    },
)
