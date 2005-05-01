/* GNU m4 -- A simple macro processor
   Copyright (C) 1989-1994, 1998-1999, 2003 Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301  USA
*/

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "m4private.h"


static const char * skip_space (m4 *, const char *);



/* Give friendly warnings if a builtin macro is passed an
   inappropriate number of arguments.  ARGC/ARGV are the arguments,
   MIN is the minimum number of acceptable arguments, negative if not
   applicable, MAX is the maximum number, negative if not applicable.
   ARGC, MIN, and MAX count ARGV[0], the name of the macro.  */
bool
m4_bad_argc (m4 *context, int argc, m4_symbol_value **argv, int min, int max)
{
  if (min > 0 && argc < min)
    {
      M4WARN ((m4_get_warning_status_opt (context), 0,
	       _("Warning: %s: too few arguments: %d < %d"),
	       M4ARG (0), argc - 1, min - 1));
      return true;
    }

  if (max > 0 && argc > max)
    {
      M4WARN ((m4_get_warning_status_opt (context), 0,
	       _("Warning: %s: too many arguments (ignored): %d > %d"),
	       M4ARG (0), argc - 1, max - 1));
      /* Return false, otherwise it is not exactly `ignored'. */
      return false;
    }

  return false;
}

static const char *
skip_space (m4 *context, const char *arg)
{
  while (m4_has_syntax (M4SYNTAX, *arg, M4_SYNTAX_SPACE))
    arg++;
  return arg;
}

/* The function m4_numeric_arg () converts ARG to an int pointed to by
   VALUEP. If the conversion fails, print error message for macro.
   Return true iff conversion succeeds.  */
bool
m4_numeric_arg (m4 *context, int argc, m4_symbol_value **argv,
		int arg, int *valuep)
{
  char *endp;

  if (*M4ARG (arg) == 0
      || (*valuep = strtol (skip_space (context, M4ARG (arg)), &endp, 10),
	  *skip_space (context, endp) != 0))
    {
      M4WARN ((m4_get_warning_status_opt (context), 0,
	       _("Warning: %s: argument %d non-numeric: %s"),
	       M4ARG (0), arg - 1, M4ARG (arg)));
      return false;
    }
  return true;
}


/* Print ARGC arguments from the table ARGV to obstack OBS, separated by
   SEP, and quoted by the current quotes, if QUOTED is true.  */
void
m4_dump_args (m4 *context, m4_obstack *obs, int argc,
	      m4_symbol_value **argv, const char *sep, bool quoted)
{
  int i;
  size_t len = strlen (sep);

  for (i = 1; i < argc; i++)
    {
      if (i > 1)
	obstack_grow (obs, sep, len);

      m4_shipout_string (context, obs, M4ARG (i), 0, quoted);
    }
}

