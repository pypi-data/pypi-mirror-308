
"""
Module to expose more detailed version info for the installed `scikitplot`
"""
git_revision = "932d5d7a4b83a32c2f493f0f9a3ce2d3efdec970"

version = "0.4.0"
__version__ = version
full_version = version
short_version = version.split("+")[0]

release = 'dev' not in version and '+' not in version
if not release:
    version = full_version
