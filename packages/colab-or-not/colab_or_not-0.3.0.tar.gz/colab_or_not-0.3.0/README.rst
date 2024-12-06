============
colab_or_not
============

``colab_or_not`` is Python package to help make Jupyter notebooks easily runnable in Google Colab or local environments.

Installation
------------

Install the latest version with pip::

    pip install colab-or-not

Overview
---------

If you want to create a Jupyter notebook that can run in Google Colab as well as a local or other environment, there
are several annoying things you need to worry about:

#. Installing required Python packages
#. Installing required system packages
#. Installing required Python modules
#. Loading settings
#. Prompting for input files

This package helps you with all of that.

Example usage::

    %pip install colab-or-not

    from colab_or_not import NotebookBridge

    # Set up our notebook environment
    notebook_env = NotebookBridge(
        github_repo="higherbar-ai/colab-or-not",
        requirements_path="example-requirements.txt",
        system_packages=[],
        module_paths=[
            "src/example_module.py",
        ],
        config_path="~/.hbai/colab-or-not.env",
        config_template={
            "SETTING_1": "setting 1 value",
            "SETTING_2": "setting 2 value",
        }
    )
    notebook_env.setup_environment()

    # Read and output settings
    setting_1 = notebook_env.get_setting("SETTING_1")
    setting_2 = notebook_env.get_setting("SETTING_2")
    print()
    print(f"Setting 1: {setting_1}")
    print(f"Setting 2: {setting_2}")

    # Use a function in a custom module (adding a type hint to ignore an import warning in Google Colab)
    import example_module   # type: ignore[import]
    example_module.example_function()

    # Prompt user for one or more input files
    input_files = notebook_env.get_input_files(prompt="Please select one or more input files")

    # Output the list of selected or uploaded input files
    print()
    if not input_files:
        print("No input files selected or uploaded.")
    for input_file in input_files:
        print(f"Input file: {input_file}")

    # Output the output directory (here, just the user home directory or Colab content root)
    output_dir = notebook_env.get_output_dir(not_colab_dir="~", colab_subdir="")
    print()
    print(f"Output directory: {output_dir}")

For a runnable version of the above, see
`the example.ipynb notebook <https://github.com/higherbar-ai/colab-or-not/blob/main/src/example.ipynb>`_.

Technical details
-----------------

Loading settings
^^^^^^^^^^^^^^^^

To load settings from either a configuration file or Google Colab secrets, initialize a ``NotebookBridge`` object with
a ``config_path`` for the configuration file and, optionally, a ``config_template`` that contains name-value pairs for
default settings. Call the ``setup_environment()`` method and then ``get_setting()`` for each setting you'd like to
read. For example::

    from colab_or_not import NotebookBridge

    notebook_env = NotebookBridge(
        config_path="~/.hbai/colab-or-not.env",
        config_template={
            "SETTING_1": "setting 1 value",
            "SETTING_2": "setting 2 value",
        }
    )

    notebook_env.setup_environment()

    setting_1 = notebook_env.get_setting("SETTING_1")
    setting_2 = notebook_env.get_setting("SETTING_2")

If in Google Colab, the settings will always come from secrets (click the key button in the left sidebar, create
each secret, and be sure to click the toggle to give the notebook access to each secret).

If not in Google Colab, ``setup_environment()`` will look for the configuration file and, if it's there, load its
settings into the local environment (which is where ``get_setting()`` will find them). If the configuration file doesn't
exist, ``setup_environment()`` will raise an exception that tells the user they need to configure settings in that
configuration file before trying again; if you had specified a ``config_template``, a default configuration file will
be written out for the user, based on your template.

Installing Python packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

To install Python packages, you can explicitly add ``%pip install packagename`` lines to your notebook, or you can use
the ``NotebookBridge`` class to automatically install requirements from a ``requirements.txt`` file in your GitHub repo.
For example::

    from colab_or_not import NotebookBridge

    notebook_env = NotebookBridge(
        github_repo="higherbar-ai/colab-or-not",
        requirements_path="example-requirements.txt"
    )
    notebook_env.setup_environment()

Your file can be named anything you like, but it should be in the format of a ``requirements.txt`` file. It also doesn't
have to be in the root of your repo; you can specify a path to it, like ``src/requirements.txt``.

Installing system packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

To install system packages, you can explicitly add `apt-get`, `brew`, or `choco` commands, depending on the system, or
you can use the ``NotebookBridge`` class to automatically install system packages. For example::

    from colab_or_not import NotebookBridge

    notebook_env = NotebookBridge(
        system_packages=[
            "libreoffice",
        ]
    )
    notebook_env.setup_environment()

Each system package will be installed using the appropriate package manager for the current system.

Importing custom modules from your GitHub repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need access to one or more ``.py`` modules from your GitHub repo, you can use the ``NotebookBridge`` class to
automatically download and install them locally when running in Google Colab. For example::

    from colab_or_not import NotebookBridge

    notebook_env = NotebookBridge(
        github_repo="higherbar-ai/colab-or-not",
        module_paths=[
            "src/example_module.py",
        ]
    )
    notebook_env.setup_environment()

    import example_module   # type: ignore[import]
    example_module.example_function()

Each module will be downloaded into the Google Colab content folder and that will be added into the Python system path
so that import statements will work as expected. (Unfortunately, Google Colab will still show a warning in the text
editor about dynamically-loaded modules, which is why we have a ``# type: ignore[import]`` comment in our examples.)

Prompting for input files
^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to read user files in your notebook, you can call the ``get_input_files()`` method. For example::

    from colab_or_not import NotebookBridge

    notebook_env = NotebookBridge()

    input_files = notebook_env.get_input_files(prompt="Please select one or more input files")
    if not input_files:
        print("No input files selected or uploaded.")
    for input_file in input_files:
        print(f"Input file: {input_file}")

When running in Google Colab, the user will be prompted to upload one or more files.

When running locally, the user will be prompted to select one or more files.

Choosing an output directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to write output files in your notebook, you can call the ``get_output_dir()`` method. For example::

    from colab_or_not import NotebookBridge

    notebook_env = NotebookBridge()

    output_dir = notebook_env.get_output_dir(not_colab_dir="~/ai-workflows", colab_subdir="")
    print(f"Output directory: {output_dir}")

Your not-colab directory can be any path you like, though you might want to include `~` to start at the current user's
home directory. For Colab, you can optionally specify a subdirectory within the main content folder. Either way, if the
directory doesn't exist, it will be created automatically.

Adding an Open in Colab badge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add a handy *Open in Colab* button to the top of your Jupyter notebook, add HTML text like this to the beginning
of a Markdown cell at the top::

    <a href="https://colab.research.google.com/github/higherbar-ai/colab-or-not/blob/main/src/example.ipynb" target="_parent">
    <img alt="Open In Colab" src="https://colab.research.google.com/assets/colab-badge.svg"/>
    </a>

Just be sure to update the ``https://colab.research.google.com/github/higherbar-ai/colab-or-not/blob/main/src/example.ipynb``
part to point to your own GitHub repo and notebook.

Known issues
^^^^^^^^^^^^

(None yet!)

Credits
-------

This toolkit was originally developed by `Higher Bar AI, PBC <https://higherbar.ai>`_, a public benefit corporation. To
contact us, email us at ``info@higherbar.ai``.

Full documentation
------------------

See the full reference documentation here:

    https://colab-or-not.readthedocs.io/

Local development
-----------------

To develop locally:

#. ``git clone https://github.com/higherbar-ai/colab-or-not``
#. ``cd colab-or-not``
#. ``python -m venv .venv``
#. ``source .venv/bin/activate``
#. ``pip install -r requirements.txt``
#. ``pip install -e .``

For convenience, the repo includes ``.idea`` project files for PyCharm.

To rebuild the documentation:

#. Update version number in ``/docs/source/conf.py``
#. Update layout or options as needed in ``/docs/source/index.rst``
#. In a terminal window, from the project directory:
    a. ``cd docs``
    b. ``SPHINX_APIDOC_OPTIONS=members,show-inheritance sphinx-apidoc -o source ../src/colab_or_not --separate --force``
    c. ``make clean html``

To rebuild the distribution packages:

#. For the PyPI package:
    a. Update version number (and any build options) in ``/setup.py``
    b. Confirm credentials and settings in ``~/.pypirc``
    c. Run ``/setup.py`` for the ``bdist_wheel`` and ``sdist`` build types (*Tools... Run setup.py task...* in PyCharm)
    d. Delete old builds from ``/dist``
    e. In a terminal window:
        i. ``twine upload dist/* --verbose``
#. For GitHub:
    a. Commit everything to GitHub and merge to ``main`` branch
    b. Add new release, linking to new tag like ``v#.#.#`` in main branch
#. For readthedocs.io:
    a. Go to https://readthedocs.org/projects/colab-or-not/, log in, and click to rebuild from GitHub (only if it
       doesn't automatically trigger)
