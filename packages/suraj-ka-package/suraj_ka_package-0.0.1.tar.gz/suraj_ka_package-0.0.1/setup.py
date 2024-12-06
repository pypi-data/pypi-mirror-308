import setuptools

with open('./README.md','r') as file:
    package_description = file.read()

setuptools.setup(
	name = 'suraj_ka_package',
	version = '0.0.1',
	author = 'Suraj Yadav',
	author_email = 'sam124.sy@gmail.com',
	description = 'Simple Python function',
	long_description = package_description,
	long_description_content_type = 'text/markdown',
	classifiers = [
	'Programming Language :: Python :: 3',
	"Operating System :: OS Independent"],
	python_requires = '>=3.5',
	)
