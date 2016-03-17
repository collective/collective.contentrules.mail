============
Introduction
============

.. image:: https://travis-ci.org/collective/collective.contentrules.mail.svg?branch=master
       :target: https://travis-ci.org/collective/collective.contentrules.mail

This package provides an extended content rule "mail" action with many more
variable substitutions available, including the name and email address of
the content owner, making it possible to email the owner of a piece of
content.

It is also possible to provide new "replacers" by writing an interface with
an associated adapter and registering a new `IMailModel` utility. The user
is able to pick the replacer to use on the action edit form.

Compatibility
=============

Plone 4.0 - 4.3
