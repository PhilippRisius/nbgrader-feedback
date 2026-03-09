============
Installation
============

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Stable release
--------------

To install nbgrader-feedback, run this command in your terminal:

.. code-block:: console

    python -m pip install nbgrader_feedback

This is the preferred method to install nbgrader-feedback, as it will always install the most recent stable release.


From sources
------------

The sources for nbgrader-feedback can be downloaded from the `Github repo`_.

#. Download the source code from the `Github repo`_ using one of the following methods:

    * Clone the public repository:

        .. code-block:: console

            git clone git@github.com:PhilippRisius/nbgrader-feedback.git

    * Download the `tarball <https://github.com/PhilippRisius/nbgrader-feedback/tarball/main>`_:

        .. code-block:: console

            curl -OJL https://github.com/PhilippRisius/nbgrader-feedback/tarball/main

#. Once you have a copy of the source, you can install it with:

    .. code-block:: console

        python -m pip install .

#. When new changes are made to the `Github repo`_, if using a clone, you can update your local copy using the following commands from the root of the repository:

    .. code-block:: console

        git fetch
        git checkout main
        git pull origin main
        python -m pip install .

    These commands should work most of the time, but if big changes are made to the repository, you might need to remove the environment and create it again.

.. _Github repo: https://github.com/PhilippRisius/nbgrader-feedback
