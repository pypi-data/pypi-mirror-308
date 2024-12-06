from setuptools import setup, find_packages

setup(
	name='voxe',
	version='0.0.2',
	author='aiyojun',
	author_email='aiyojun@gmail.com',
	description='A kind of simple transport layer protocol',
	long_description=open('README.rst').read(),
	url='https://github.com/aiyojun/pysolv',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
	],
	python_requires='>=3.6',
)