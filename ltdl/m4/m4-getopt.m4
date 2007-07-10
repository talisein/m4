#                                                            -*- Autoconf -*-
# m4-getopt.m4 -- Use the installed version of getopt.h if available.
# Written by Gary V. Vaughan <gary@gnu.org>
#
# Copyright (C) 2005, 2006, 2007 Free Software Foundation, Inc
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

# serial 2

# M4_GETOPT
# ---------
# Use the installed version of getopt.h if available.
AC_DEFUN([M4_GETOPT],
[GETOPT_H=
AC_SUBST([GETOPT_H])

AC_CHECK_HEADERS([getopt.h], [], [GETOPT_H=getopt.h], [AC_INCLUDES_DEFAULT])

if test -z "$GETOPT_H"; then
  AC_CHECK_FUNCS([getopt_long_only], [], [GETOPT_H=getopt.h])
fi

dnl BSD getopt_log uses an incompatible method to reset option processing,
dnl and (as of 2004-10-15) mishandles optional option-arguments.
if test -z "$GETOPT_H"; then
  AC_CHECK_DECL([optreset], [GETOPT_H=getopt.h], [], [#include <getopt.h>])
fi

if test -z "$GETOPT_H"; then
  AC_CACHE_CHECK([for working gnu getopt function], [gl_cv_func_gnu_getopt],
    [AC_RUN_IFELSE(
      [AC_LANG_PROGRAM([#include <getopt.h>],
	[[
	  char *myargv[3];
	  myargv[0] = "conftest";
	  myargv[1] = "-+";
	  myargv[2] = 0;
	  return getopt (2, myargv, "+a") != '?';
	]])],
      [gl_cv_func_gnu_getopt=yes],
      [gl_cv_func_gnu_getopt=no],
      [dnl cross compiling - pessimistically gues based on decls
       dnl Solaris 10 getopt doesn't handle `+' as a leading character in an
       dnl option string (as of 2005-05-05).
       AC_CHECK_DECL([getopt_clip],
	 [gl_cv_func_gnu_getopt=no], [gl_cv_func_gnu_getopt=yes],
	 [#include <getopt.h>])])])
  test X"$gl_cv_func_gnu_getopt" = Xno && GETOPT_H=getopt.h
fi

if test -n "$GETOPT_H"; then
  AC_DEFINE([__GETOPT_PREFIX], [[rpl_]],
    [Define to rpl_ if the getopt replacement function should be used.])
fi

AM_CONDITIONAL([GETOPT], [test -n "$GETOPT_H"])
])# M4_GETOPT
