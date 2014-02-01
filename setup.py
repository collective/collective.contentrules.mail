from setuptools import setup, find_packages

version = '0.7.dev0'

setup(name='collective.contentrules.mail',
      version=version,
      description="Flexible mail content rule",
      long_description=(open("README.txt").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.2",
          "Framework :: Plone :: 3.3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='https://github.com/collective/collective.contentrules.mail',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.kss'
      ],
      extras_require = {
        "test": ["plone.app.testing>=4.2.3", ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
