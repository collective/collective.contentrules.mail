Changelog
=========

0.7 (2016-03-17)
----------------

- Ported tests to plone.app.testing
  [tomgross]

- Plone 4.3 compatibiliy
  [tomgross]

- Moved to https://github.com/collective/collective.contentrules.mail
  [maurits]

0.6 (2012-02-23)
----------------

* Remove an extra From header when calling mailhost.secureSend()
  [dimboo]
  
0.5 - 2011-05-20
----------------

* Added an exception in IVocabularyFactory import for Plone >= 4.1.
  [lepri]

0.4 - 2009-09-06
----------------

* Avoid a site error if the mail cannot be sent, e.g. because the mail
  server is down.
  [optilude]

* Avoid throwing an exception on encoded strings in the replacer.
  [optilude]

* Caught workflow exception when trying to get state on object without any
  workflow.
  [tiazma]

* Added cc and bcc fields to IMailAction enabling the use of these fields in 
  mail messages
  [erico_andrei]

* Added new variables to IMailReplacer so it is possible to send emails to 
  users with other roles than owner on the object
  [erico_andrei]

* Made sure Archetypes content implements IDublinCore (It's not the default 
  behavior until AT 1.5.10)
  [erico_andrei]
  
* Correct action mail fail on try to replace bcc or cc when it returns None [lucmult]

0.3 - 2009/03/24
----------------

* Added a note in the UI about how to use variables.
  [optilude]
  
* The 'source' field is not required, but would throw an error if not filled
  in. This is now fixed.
  [optilude]

0.2 - 2009/03/24
----------------

* Made the executor fail gracefully if the content being acted upon is not
  adaptable to the replacer interface.
  [optilude]

* Made the default replacer adapt any Dublin Core-capable content, avoiding
  an unnecessary dependency on Archetypes.
  [optilude]

* Made the default IMailModel implementation more re-usable.
  [optildue]

* Updated documentation and interface specifications.
  [optilude]

* Fixes actions/configure.zcml in order to play nice with GenericSetup


0.1 - Unreleased
----------------

* Initial release

