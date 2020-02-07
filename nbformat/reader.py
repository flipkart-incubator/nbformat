"""API for reading notebooks of different versions"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import json

class NotJSONError(ValueError):
    pass

def parse_json(s, **kwargs):
    """Parse a JSON string into a dict."""
    try:
        nb_dict = json.loads(s, **kwargs)
    except ValueError:
        # Limit the error message to 80 characters.  Display whatever JSON will fit.
        raise NotJSONError(("Notebook does not appear to be JSON: %r" % s)[:77] + "...")
    return nb_dict

# High level API

def get_version(nb):
    """Get the version of a notebook.

    Parameters
    ----------
    nb : dict
        NotebookNode or dict containing notebook data.

    Returns
    -------
    Tuple containing major (int) and minor (int) version numbers
    """
    major = nb.get('nbformat', 1)
    minor = nb.get('nbformat_minor', 0)
    return (major, minor)


def reads(s, **kwargs):
    """Read a notebook from a json string and return the 
    NotebookNode object.

    This function properly reads notebooks of any version.  No version 
    conversion is performed.

    Parameters
    ----------
    s : unicode
        The raw unicode string to read the notebook from.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """
    from . import versions, NBFormatError
    
    nb_dict = parse_json(s, **kwargs)
    if not nb_dict.get('new_untitled', False):
        nb_dict['metadata'] = {
          "kernelspec": {
           "display_name": "Python 3",
           "language": "python",
           "name": "python3"
          },
          "language_info": {
           "codemirror_mode": {
            "name": "ipython",
            "version": 3
           },
           "file_extension": ".py",
           "mimetype": "text/x-python",
           "name": "python",
           "nbconvert_exporter": "python",
           "pygments_lexer": "ipython3",
           "version": "3.7.3"
          }
         }
    if 'new_untitled' in nb_dict.keys():
        del nb_dict['new_untitled']
    (major, minor) = get_version(nb_dict)
    if major in versions:
        return versions[major].to_notebook_json(nb_dict, minor=minor)
    else:
        raise NBFormatError('Unsupported nbformat version %s' % major)


def read(fp, **kwargs):
    """Read a notebook from a file and return the NotebookNode object.

    This function properly reads notebooks of any version.  No version 
    conversion is performed.

    Parameters
    ----------
    fp : file
        Any file-like object with a read method.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """
    return reads(fp.read(), **kwargs)
