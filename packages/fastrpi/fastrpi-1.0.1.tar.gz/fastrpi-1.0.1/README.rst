`fastrpi`: FastrPI client
=========================

The package ``fastrpi`` is the client to interact with the FastrPI, the
Fastr Package Index, where Fastr Networks, Tools and Datatypes are gathered
to use with `Fastr <https://fastr.readthedocs.io>`_.
In the FastrPI repository the Fastr Network, Tool and Datatype definitions are stored,
as well as Dockerized versions of the Fastr Tools. By using the FastrPI client the
networks can easily be retrieved and run using either Docker or Singularity.

The code can be found on `Gitlab <https://gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi>`_
and the documentation is available through `ReadTheDocs <https://fastrpi.readthedocs.io/en/latest/>`_.

The FastrPI repository itself is currently not open to the public.

Install
-------

To use ``fastrpi`` it is necessary to have Git (>=1.7.0) installed and either Docker or Singularity.
Install and set up FastrPI by running:
.. codeblock::

  pip install fastrpi
  fastrpi init

During the initialization process you will be guided through the setup process. To use the private repository and
to publish packages you will need to set an SSH connection with GitLab and have a GitLab API token.
See the documentation for more information.

Usage
-----

The ``fastrpi`` package can be used to install, run, create, edit and publish Fastr Tools and Networks.
Here is a quick introduction to installing and running a network.

Before you can run a Network it needs to be installed. You can do so by using:

.. code-block:: bash

    fastrpi install network network_name -v version

During the installation of this network the necessary Tools will also be installed. With this installation
the Docker containers associated with these Tools will also be pulled using either Docker or Singularity.
The available Networks and Tools in the FastrPI repository can be viewed using ``fastrpi list networks``
and ``fastrpi list tools``.

After installing a Network it can be run using:

.. code-block:: bash

    fastrpi run network_name -v version --source_sink ./source_sink.py

The file ``./source_sink.py`` must contain the functions
``get_source_data()`` and ``get_sink_data()``. These functions must
return dictionaries containing the Sources and Sinks, as described `here <https://fastr.readthedocs.io/en/stable/static/quick_start.html#running-a-network>`_.

Further information about the functionality of FastrPI can be found in the documentation.

Known issues
------------

- The package is not yet tested on Windows.


