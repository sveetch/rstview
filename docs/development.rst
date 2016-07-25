.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org

===========
Development
===========

Development requirement
***********************

rstview is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using ``flake8``;
* ``Sphinx`` for documentation with enabled `Napoleon`_ extension (using only the *Google style*);

Every requirement is available in file ``dev_requirements.txt``.

Install for development
***********************

First ensure you have `pip`_ and `virtualenv`_ installed, then in your console terminal type this: ::

    mkdir rstview-dev
    cd rstview-dev
    virtualenv --system-site-packages .
    source bin/activate
    pip install -r https://raw.githubusercontent.com/sveetch/rstview/master/requirements/dev.txt

rstview will be installed in editable mode from the last commit on master branch.
