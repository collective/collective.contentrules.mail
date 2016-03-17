from setuptools import setup, find_packages

version = '0.7'

setup(name='collective.contentrules.mail',
      version=version,
      description="Flexible mail content rule",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
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
          'plone.app.kss',
          'zope.app.form',

      ],
      extras_require = {
        "test": [
            "plone.app.testing>=4.2.3",
            "Products.PloneTestCase"],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
