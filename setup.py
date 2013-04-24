from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-agesic',
	version=version,
	description="AGESIC CKAN plugin",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='An\xc3\xadbal Pacheco',
	author_email='anibal.pacheco@agesic.gub.uy',
	url='http://catalogodatos.gub.uy/',
	license='GPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.agesic'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	agesic=ckanext.agesic.plugin:ExampleIDatasetFormPlugin
	""",
)
