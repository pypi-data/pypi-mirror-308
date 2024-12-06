==============================================================================
A Robot Framework library for starting and stopping Django.
==============================================================================


Introduction
------------

DjangoLaunch is a Robot Framework library for starting and stoppping Django.

It has been forked from
https://github.com/kitconcept/robotframework-djangolibrary


Documentation
-------------

Keywords are documented in `Robot Framework Django Launch Keyword Documentation`_.


Installation
------------

Install with::

  pip install robotframework-djangolaunch

Example
-------

An example using robotframework-browser::

  *** Variables ***

  ${SERVER}               http://localhost:55001


  *** Settings ***

  Documentation   Django Robot Tests
  Library         DjangoLaunch  127.0.0.1  55001  settings=mysite.robotframework_settings
  Library         Browser
  Suite Setup     Open Django and Browser
  Suite Teardown  Close Django and Browser


  *** Keywords ***

  Open Django and Browser
    Start Django
    New Persistent Context

  Close Django and Browser
    Close Browser
    Stop Django


  *** Test Cases ***

  Scenario: As a visitor I can visit the django default page
    New Page  ${SERVER}
    Get Element  text=Hello, World

The `GitHub project main workflow`_  has a live example on how to install
dependencies and runt it.


License
-------

Copyright kitconcept GmbH.

Distributed under the terms of the Apache License 2.0,
robotframework-djangolaunch is free and Open Source software.


Credits
-------

This library was developed by Timo Stollenwerk at kitconcept.

.. image:: kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

.. _`Robot Framework Django Launch Keyword Documentation`: https://mrannanj.github.io/robotframework-djangolaunch/
.. _`GitHub project main workflow`: .github/workflows/main.yml
