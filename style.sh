#!/bin/sh
set -e
find ./ -name "*.py" | xargs pep8 --show-source --max-line-length=100 --ignore=W191,E128
# TODO: Need to reduce disabled list
find ./ -name "*.py" | xargs pylint3 --max-line-length=100 --indent-string="	" -fparseable \
	-e all -d missing-docstring,invalid-name,bad-continuation,no-member,too-many-ancestors \
	-d too-few-public-methods,no-self-use,wildcard-import,duplicate-code,too-many-arguments \
	-d super-init-not-called,locally-disabled,suppressed-message -r no
