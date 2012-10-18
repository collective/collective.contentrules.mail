from setuptools import setup, find_packages

version = '0.7.dev0'

setup(name='collective.contentrules.mail',
      version=version,
      description="Flexible mail content rule",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.rst").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='https://github.com/collective/collective.contentrules.mail',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective','collective.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
