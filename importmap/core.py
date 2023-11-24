import hashlib
import json
import logging
import os
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from .generator import ImportmapGenerator

logger = logging.getLogger(__name__)


DEFAULT_CONFIG_FILENAME = "pyproject.toml"
DEFAULT_LOCK_FILENAME = "importmap.lock"


def hash_for_data(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


class Importmap:
    def __init__(
        self,
        config_filename=DEFAULT_CONFIG_FILENAME,
        lock_filename=DEFAULT_LOCK_FILENAME,
    ):
        self.config_file = Path(config_filename)
        self.lock_file = Path(lock_filename)
        self.load()

    @classmethod
    def json(cls, *, development=False, extra_imports={}):
        importmap = cls()

        if development:
            imap = importmap.map_dev
            indent = 2
        else:
            imap = importmap.map
            indent = None

        imap.get("imports", {}).update(extra_imports)

        return json.dumps(imap, indent=indent, sort_keys=True)

    def load(self):
        # TODO django check to compare lock and config hash

        self.config = self.load_config()

        if not self.config:
            # No config = no map and no lockfile
            self.map = {}
            self.map_dev = {}
            self.lock_file.unlink(missing_ok=True)
            return

        lockfile = self.load_lockfile()
        if lockfile:
            self.map = lockfile["importmap"]
            self.map_dev = lockfile["importmap_dev"]
        else:
            self.map = {}
            self.map_dev = {}

    def generate(self, force=False):
        config_hash = hash_for_data(self.config)
        lockfile = self.load_lockfile()
        if force or not lockfile or lockfile["config_hash"] != config_hash:
            # Generate both maps now, tag will choose which to use at runtime
            self.map = self.generate_map()
            self.map_dev = self.generate_map(development=True)

            lockfile["config_hash"] = config_hash
            lockfile["importmap"] = self.map
            lockfile["importmap_dev"] = self.map_dev
            self.save_lockfile(lockfile)

    def load_config(self):
        if not self.config_file.exists():
            return {}
        with self.config_file.open("rb") as f:
            pyproject = tomllib.load(f)

        return pyproject["tool"]["importmap"]

    def load_lockfile(self):
        if not self.lock_file.exists():
            return {}

        with self.lock_file.open("r") as f:
            return json.load(f)

    def save_lockfile(self, lockfile):
        with self.lock_file.open("w+") as f:
            json.dump(lockfile, f, indent=2, sort_keys=True)

    def generate_map(self, *args, **kwargs):
        return ImportmapGenerator.from_config(self.config, *args, **kwargs).generate()
