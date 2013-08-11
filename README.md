Little Printer Django Project
=============================

An example django project and library for creating little printer publications.


Motivation
----------

I created this example because I felt the current example code around the web was
missing a trick when it came to parameter validation from BERG Cloud.

One thing Django is really good at is parameter validation using class based forms.
Using forms also allows us to automatically generate meta descriptions for BERG Cloud
making it a simple process to create publications.


Quick Start
-----------

To create a publication simply create a django app within this project and sub class the 
BergCloudPublicationForm from the printer app adding any fields your publication will require.

Then sub class the EditionView from the printer application, set the form class and
override the get_context_data to provide content for your publication.

See the publication app for a full example which implements the Hello World example
from the BERG Cloud developer documentation.


Extras
------

There is also a base template in printer app for you to use to create your publication templates from.
I have provided a test suite that validates the printer views against the BERG Cloud API spec for publications.
Travis CI is used to make it easy for others to collaborate on this project.


