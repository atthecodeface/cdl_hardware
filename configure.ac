AC_INIT([CDL hardware],[1.0])
AC_CHECK_HEADER([stdio.h],
  [AC_DEFINE([HAVE_STDIO_H], [1],
    [Define to 1 if you have <stdio.h>])],
  [AC_MSG_ERROR([Sorry...])])

AC_CONFIG_FILES([Makefile])
AC_CONFIG_HEADERS([config.h])
AC_CHECK_HEADERS([png.h])
AC_CHECK_HEADERS([noway.h])
AC_SEARCH_LIBS([png_get_io_ptr],[png],,[AC_MSG_ERROR([Sorry... no libpng])])
AC_SEARCH_LIBS([jpeg_CreateDecompress], [jpeg],,[AC_MSG_ERROR([Sorry... no libjpeg])])
AC_PATH_PROG([CYCLICITY],[bin/linux/cdl],[not_found])
AS_IF([test "$ac_cv_path_CYCLICITY" = "not_found"],[AC_MSG_ERROR(['cdl' not found - try using CYCLICITY=/path/to/cdl])])
AC_OUTPUT
