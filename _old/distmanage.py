#!/usr/bin/env python

from manage import env, main
env['DJANGO_SETTINGS_MODULE'] = 'website.settings_no_debug'

if __name__ == '__main__':
    main()
