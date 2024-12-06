#  Copyright (c) 2024 Higher Bar AI, PBC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
import requests


@dataclass
class NotebookBridge:
    """
    Class for providing Jupyter notebooks with a simple bridge between Google Colab and other Jupyter environments.

    :param github_repo: GitHub repository in format "username/repo" (required only if you want to install requirements
        or modules)
    :type github_repo: Optional[str]
    :param github_branch: GitHub repo branch to use (defaults to "main")
    :type github_branch: str
    :param requirements_path: Relative path to text file with requirements within repo (if any; e.g.,
        "src/requirements.txt"; requires github_repo be supplied)
    :type requirements_path: Optional[str]
    :param module_paths: List of relative paths to Python modules to fetch in Colab (if any; requires github_repo be
        supplied)
    :type module_paths: Optional[List[str]]
    :param config_path: Full path to local config file (optional; can use ~ for user home directory; only used when
        running outside Google Colab)
    :type config_path: Optional[str]
    :param config_template: Dict of config setting names and default values, for initializing a new config file
        (optional; only used when running outside Google Colab)
    :type config_template: Optional[Dict[str, str]]
    """

    github_repo: Optional[str] = None
    github_branch: str = "main"
    requirements_path: Optional[str] = None
    module_paths: Optional[List[str]] = None
    config_path: Optional[str] = None
    config_template: Optional[Dict[str, str]] = None

    _is_colab: bool = False
    _config_loaded: bool = False
    _dependencies_installed: bool = False
    _modules_fetched: bool = False

    @property
    def is_colab(self) -> bool:
        """
        Return whether we're running in Colab.

        :return: True if running in Colab, False otherwise
        :rtype: bool
        """

        return self._is_colab

    def __post_init__(self):
        """
        Detect environment and initialize configuration.
        """

        # Detect if we're running in Colab
        try:
            # noinspection PyPackageRequirements
            from google.colab import userdata   # type: ignore[import]
            self._is_colab = True
            self._userdata = userdata
        except ImportError:
            self._is_colab = False

        # If we have config file, load it when running locally
        if not self._is_colab and self.config_path:
            self._load_config()

        # Ensure that we have a GitHub repo if we need it
        if not self._is_colab and (self.requirements_path or self.module_paths):
            if not self.github_repo:
                raise ValueError("A GitHub repository must be provided to fetch requirements or modules")

    def _load_config(self) -> None:
        """
        Load configuration from config file when running locally.
        """

        if self._config_loaded or not self.config_path:
            return

        # Expand user directory if needed
        config_path = Path(os.path.expanduser(self.config_path))

        # Create parent directories if needed
        config_path.parent.mkdir(parents=True, exist_ok=True)

        if not config_path.exists():
            if self.config_template:
                # Create template config file
                template = ""
                for key, value in self.config_template.items():
                    template += f"{key}={value}\n"
                config_path.write_text(template)

            raise Exception(f"Please configure settings in {config_path}, then try again")

        import dotenv
        dotenv.load_dotenv(config_path)
        self._config_loaded = True

    def _get_github_raw_url(self, path: str) -> str:
        """
        Convert a repository path to a raw GitHub URL.

        :param path: Path within the repository
        :type path: str
        :return: Full URL to raw file on GitHub
        :rtype: str
        """

        return f"https://raw.githubusercontent.com/{self.github_repo}/{self.github_branch}/{path}"

    def setup_environment(self) -> None:
        """
        Set up the environment by installing dependencies and fetching source files.
        Should be called before any other operations.
        """

        self._install_dependencies()
        if self._is_colab and self.module_paths:
            self._fetch_modules()

    def _install_dependencies(self) -> None:
        """
        Install required dependencies from requirements.txt if specified.
        """

        if self._dependencies_installed or not self.requirements_path:
            return

        try:
            if self._is_colab:
                # Fetch requirements.txt from GitHub
                req_url = self._get_github_raw_url(self.requirements_path)
                response = requests.get(req_url)
                response.raise_for_status()

                # Write requirements to a temporary file
                req_path = Path("/content/requirements.txt")
                req_path.write_text(response.text)
            else:
                # Find project root and use relative path from there
                project_root = self._find_project_root()
                if not project_root:
                    raise FileNotFoundError("Could not find project root directory")

                req_path = project_root / self.requirements_path
                if not req_path.exists():
                    raise FileNotFoundError(f"Requirements file not found at {req_path}")

            # Install requirements
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_path)])
            self._dependencies_installed = True
            print("Dependencies installed successfully.")

        except Exception as e:
            raise Exception(f"Failed to install dependencies: {str(e)}")

    def _fetch_modules(self) -> None:
        """
        Fetch required Python modules from GitHub when running in Colab.
        """

        if not self._is_colab or not self.module_paths or self._modules_fetched:
            return

        for module_path in self.module_paths:
            try:
                # Fetch module from GitHub
                module_url = self._get_github_raw_url(module_path)
                response = requests.get(module_url)
                response.raise_for_status()

                # Determine the output path in Colab
                output_path = Path("/content") / Path(module_path).name
                output_path.write_text(response.text)
                print(f"Downloaded {module_path}")

            except Exception as e:
                raise Exception(f"Failed to fetch {module_path}: {str(e)}")

        # Ensure that current path is in sys.path
        import sys
        import os
        if os.getcwd() not in sys.path:
            sys.path.append(os.getcwd())

        self._modules_fetched = True

    def get_setting(self, setting_name: str, default_value: Any = None) -> Any:
        """
        Get a configuration setting from Colab userdata or local environment variable (which will include anything in
        a configured config file, if specified, since that file's settings are loaded into environment variables).

        :param setting_name: Name of the setting to retrieve
        :type setting_name: str
        :param default_value: Default value to return if setting is not found
        :type default_value: Any
        :return: Value of the setting or default value
        :rtype: Any
        """

        if self._is_colab:
            # noinspection PyBroadException
            try:
                return self._userdata.get(setting_name)
            except Exception:
                return default_value
        else:
            return os.getenv(setting_name.upper(), default_value)

    def _find_project_root(self) -> Optional[Path]:
        """
        Find the project root directory by looking for common project markers.
        Starts from the current working directory and moves up until a marker is found.
        """

        # Common files that indicate project root
        project_markers = [
            self.requirements_path,  # The requirements.txt path we were given
            "pyproject.toml",
            "setup.py",
            ".git",
            ".gitignore",
            "README.md"
        ]

        current = Path.cwd().resolve()

        # Keep going up until we find a marker or hit the root
        while current != current.parent:
            # Check each marker
            for marker in project_markers:
                if (current / marker).exists():
                    return current

            # Move up one directory
            current = current.parent

        return None

    def get_input_files(self, prompt: str) -> List[str]:
        """
        Get list of input files, either via Colab upload or local file selection.

        :param prompt: User prompt (goes in the dialog title for pop-ups, otherwise above the in-notebook prompt)
        :type prompt: str
        :return: List of strings with input file paths
        :rtype: List[str]
        """

        if self._is_colab:
            from IPython.display import display, HTML
            display(HTML(f"<h3>{prompt}</h3>"))
            # noinspection PyPackageRequirements
            from google.colab import files  # type: ignore[import]
            uploaded = files.upload()
            content_dir = Path("/content")
            return [str(content_dir / filename) for filename in uploaded.keys()]
        else:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()  # Hide the main window

            file_paths = filedialog.askopenfilenames(title=prompt)

            return [str(path) for path in file_paths]
