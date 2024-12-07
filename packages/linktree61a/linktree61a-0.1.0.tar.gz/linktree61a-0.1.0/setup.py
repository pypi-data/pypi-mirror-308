from setuptools import setup, find_packages

setup(
	name='linktree61a',
	version='0.1.0',
	packages=find_packages(),
	description='CS61A implementations of linked lists and trees',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/NathanDai5287/linktree61a',  # Update with your repository URL
	author='Nathan Dai',  # Update with your name
	author_email='nathandai2000@gmail.com',  # Update with your email
	classifiers=[
		'Programming Language :: Python :: 3',
	],
	python_requires='>=3.6',
)
