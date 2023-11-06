from setuptools import setup

setup(
	name='chatformat',
	version='1.2',
	packages=[
		'chatformat',
	],
	package_data={
		'chatformat': ['*.yml'],
	},
	requires=[
		'pyyaml'
	]
)