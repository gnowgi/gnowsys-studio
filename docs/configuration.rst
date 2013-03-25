======================
Advanced Configuration
======================



* For Unicode Support in different locales,
  One needs to activate the Apache server to recognize these languages.
  By default Gnowsys-Studio requires the server to recognize utf-8, when hosting.

Tested for Debian
Enable the locale, generate it:
  
  locale-gen en_HI

In /etc/apache2/envvars edit the LANG property.

  From:
  LANG=C     // This is the default

  To:  
  LANG=<locale>,

  for  eg.
  LANG=en_IN.UTF-8
