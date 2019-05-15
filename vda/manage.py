#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vda.settings")
    import django

    django.setup()

    # Override default port for `runserver` command
    from django.core.management.commands.runserver import Command as runserver
    #--------- IMPORTANT ---------#
    #Setting port to 8080 as the Container hosting the site is already using the default 8000
    runserver.default_port = "8080"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
