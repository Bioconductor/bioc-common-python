# bioc-common-python

[![Build Status](https://travis-ci.org/Bioconductor/bioc-common-python.svg?branch=master)](https://travis-ci.org/Bioconductor/bioc-common-python)
[![Build status](https://ci.appveyor.com/api/projects/status/ohoqikyl85l77db5?svg=true)](https://ci.appveyor.com/project/b-long/bioc-common-python)

Purpose
-------
This module provides common functionality to other Bioconductor python applications, such as 
[packagebuilder](https://github.com/Bioconductor/packagebuilder) and
[spb_history](https://github.com/Bioconductor/spb_history) .

It's important to note that in production, properties are required which are not exposed to 
the public.  Those properties live under [Bioconductor/private](https://github.com/Bioconductor/private).

Installation
------------
Typically, this module is not used by itself.  Instead, it's a PIP dependency of other software.  To include 
this as a dependency, create an entry in the PIP file, such as 
[this one](https://github.com/Bioconductor/spb_history/blob/9a687b1289185d37b40652291a706c3c076b006f/PIP-DEPENDENCIES--spb_history.txt#L1).
