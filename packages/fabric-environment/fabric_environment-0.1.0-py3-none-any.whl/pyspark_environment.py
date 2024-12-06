import os
import IPython

from pyspark.sql import SparkSession


def get_platform():
    return "fabric"


_spark = SparkSession.builder.getOrCreate()
_ipython = IPython.get_ipython()


def get_spark():
    return _spark


def _resolve_notebookutils():
    if not hasattr(_ipython, "user_ns") or "notebookutils" not in _ipython.user_ns:
        raise Exception("dbutils cannot be resolved")

    return _ipython.user_ns["notebookutils"]


_notebookutils = _resolve_notebookutils()


def create_text_widget(name, label, default_value=""):
    pass


def create_combobox_widget(name, options, label, default_value=""):
    pass


def get_widget_value(widget_name):
    return globals()[widget_name]


def _resolve_display():
    return _ipython.user_ns["display"]


_display = _resolve_display()


def display(*args, **kwargs):
    _display(*args, **kwargs)


def _resolve_display_html():
    if not hasattr(_ipython, "user_ns") or "displayHTML" not in _ipython.user_ns:
        raise Exception("displayHTML cannot be resolved")

    return _ipython.user_ns["displayHTML"]


_display_html = _resolve_display_html()


def display_html(html):
    _display_html(html)


_project_dir = "/"


def get_project_dir():
    return _project_dir


def run_notebook(name, params=None, timeout=6000):
    params = params or {}

    file_name = os.path.basename(name)

    _notebookutils.notebook.run(file_name, timeout, params)


def get_notebook_path():
    return "/" + _notebookutils.runtime.context["currentNotebookName"]


def get_current_username():
    return _notebookutils.runtime.context["userName"]


class Filesystem:
    @classmethod
    def cp(cls, from_: str, to: str, recursive: bool = False):
        return _notebookutils.fs.cp(from_, to, recursive)

    @classmethod
    def exists(cls, path: str):
        return _notebookutils.fs.head(path)

    @classmethod
    def head(cls, file: str, maxbytes: int = 65536):
        return _notebookutils.fs.head(file, maxbytes)

    @classmethod
    def ls(cls, path: str):
        return [item.name for item in _notebookutils.fs.ls(path)]

    @classmethod
    def mkdirs(cls, path: str):
        return _notebookutils.fs.mkdirs(path)

    @classmethod
    def mv(cls, from_: str, to: str, recurse: bool = False):
        return _notebookutils.fs.mv(from_, to, recurse)

    @classmethod
    def put(cls, file: str, contents: str, overwrite: bool = False):
        return _notebookutils.fs.put(file, contents, overwrite)

    @classmethod
    def rm(cls, path: str, recursive: bool = False):
        return _notebookutils.fs.rm(path, recursive)
