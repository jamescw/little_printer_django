#!/bin/bash

if [ "$1" == "" ]
then
    what="publication"
else
    what="$1"
    shift
fi

find . -name '*.pyc' -exec rm {} \;
coverage run ./django_printer/manage.py test --verbosity=2 --settings=django_printer.settings.test $what $*

if [ $? -eq 1 ]
then
    exit 1
fi

# running on the assumption that little goes into most init files
# and having lots of 100% coverage on empty files can skew results
coverage html --omit="*/settings/*,*/tests/*"

# try to open the page in chrome, but if not present, don't complain
which google-chrome
if [ $? -eq 0 ]
then
  google-chrome htmlcov/index.html
else
  echo "Please see coverage report in file://$PWD/htmlcov/index.html"
fi

cd ..
