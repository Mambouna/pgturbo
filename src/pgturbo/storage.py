import json
import os
import platform
from hashlib import sha1


__all__ = ['StorageCorruptionException', 'JSONEncodingException', 'Storage']


class StorageCorruptionException(Exception):
    """The data in the storage is corrupted."""


class JSONEncodingException(Exception):
    """The data in the storage is corrupted."""


def _get_platform_pgturbo_path():
    r"""Get the storage directory for pgturbo save data.

    Under Windows, return %APPDATA%\pgturbo. Under Linux/MacOS, return
    ~/.config/pgturbo/saves.

    """
    if platform.system() == 'Windows':
        try:
            appdata = os.environ['APPDATA']
        except KeyError:
            raise KeyError(
                "Couldn't find the AppData directory for Pygame Turbo save "
                "data. Please set the %APPDATA% environment variable."
            )
        return os.path.join(appdata, 'pgturbo')
    return os.path.expanduser(os.path.join('~', '.config/pgturbo/saves'))


class Storage(dict):
    """Behaves like a dictionary that serialises itself to disk.

    The name of the file will be based on the basename of the script plus
    a hash of the script's path, ensuring that each script on the filesystem
    has a unique save file.

    """
    STORAGE_DIR = _get_platform_pgturbo_path()

    # Keep a reference to all defined storages
    storages = []

    def __init__(self, filename=None):
        super().__init__()
        self.loaded = False
        self._save_file = filename
        self.storages.append(self)
        self._autosave = False

    def __setitem__(self, key, value):
        """We override this to allow automatically saving after any change."""
        if not isinstance(value, self.ALL_JSON_SERIALIZABLES):
            raise TypeError("The storage builtin can only contain values of "
                            "the types float, int, string, boolean, list, "
                            "tuple, dict or None, not of type {}."
                            .format(type(value)))
        # If the value is the same as before, we return early (preventing
        # unnecessary autosaving).
        if key in self and value == self[key]:
            return
        # Make the actual change to the dict.
        super().__setitem__(key, value)
        # Then, only if automatic saves are enabled, we save to file.
        if self._autosave:
            self._save(False)

    @property
    def autosave(self):
        return self._autosave

    @autosave.setter
    def autosave(self, value):
        if value in (True, False, 0, 1):
            self._autosave = value
        else:
            raise TypeError("storage.autosave must be one of True, False, 0 "
                            "or 1.")

    @classmethod
    def save_all(cls):
        """Save all instances of Storage."""
        cls._ensure_save_path()
        for storage in cls.storages:
            storage.save()

    @classmethod
    def _ensure_save_path(cls):
        """Ensure that the directory for all save game data exists."""
        try:
            os.makedirs(cls.STORAGE_DIR)
        except (IsADirectoryError, PermissionError):
            pass
        except FileExistsError:
            pass

    def _set_filename_from_path(self, file_path):
        """Set the path to save to from the given filename.

        We include the basename of the game script, to help with identifying
        the save data, as well as the sha1 hash of the full path of the file on
        disk, to ensure that every separate game has its own storage.

        """
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        fn_hash = sha1(file_path.encode('utf-8')).hexdigest()
        base, _ = os.path.splitext(os.path.basename(file_path))
        self._save_file = '{}-{}.json'.format(base, fn_hash)
        self.load()

    @property
    def path(self):
        """Get the path for data data."""
        if self._save_file is None:
            raise ValueError(
                "Cannot save/load storage as no filename is set."
            )
        return os.path.join(self.STORAGE_DIR, self._save_file)

    def load(self):
        """Load data into the storage from disk.

        This replaces all previous contents of the storage. If there is no save
        file found then the storage will be empty.

        """
        self.clear()

        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # If no file exists, it's fine
            pass
        except json.JSONDecodeError:
            raise StorageCorruptionException(
                "Storage is corrupted. Couldn't load the data."
            )
        else:
            self.update(data)
            self.loaded = True

    def _save(self, print_save_info):
        """Save data to disk."""
        if not self and not self.loaded:
            return
        # The save functionality seems to have been broken before this point,
        # since saving manually in the game script did not make sure the save
        # path actually existed. This fixes it.
        Storage._ensure_save_path()
        try:
            data = json.dumps(self)
        except TypeError:
            msgs = [
                "{} - type {}".format(*item)
                for item in self._get_json_error_keys(self)
            ]
            if not msgs:
                # Didn't find an explanation, so let original error propagate
                raise
            raise JSONEncodingException(
                "The following storage entries cannot be stored, because "
                "they are not JSON serializable types:\n{}\n\n"
                "Only the following types of objects are JSON-serialisable: "
                "dict, list/tuple, str, float/int, bool, and None".format(
                    "\n".join(msgs)
                )
            )
        else:
            path = self.path
            with open(path, 'w+') as f:
                f.write(data)
            if print_save_info:
                print("Saved storage to", path)

    def save(self):
        """User facing save function. Just calls the internal one with the
        arg to print a save indication."""
        self._save(True)

    def setup(self, defaults):
        """Function to use for initial setup of storage for a game. Loads
        storage and then sets all given defaults."""
        prev_autosave_setting = self._autosave
        self._autosave = False
        self.load()

        if not isinstance(defaults, dict):
            raise TypeError("storage.setup() takes a single dictionary with "
                            "key value pairs to put into storage as defaults, "
                            "not a {}.".format(type(defaults)))

        # Going through all defaults in the given dict and setting them.
        for key, value in defaults.items():
            self.setdefault(key, value)

        self._autosave = prev_autosave_setting

    def overwrite(self, new_state):
        """Used to completely overwrite storage with the given dictionary.
        Can be used to reset storage to an initial state, for example when
        starting a new game or similar."""
        prev_autosave_setting = self._autosave
        self._autosave = False
        self.clear()

        if not isinstance(new_state, dict):
            raise TypeError("storage.reset() takes a single dictionary with "
                            "key value pairs to overwrite storage with, "
                            "not a {}.".format(type(new_state)))

        self.update(new_state)

        self._autosave = prev_autosave_setting

    # Constants for use with isinstance in _get_json_error_keys()
    JSON_PRIMITIVES = (float, int, str, bool, type(None))
    JSON_SEQ = (list, tuple)
    JSON_MAPPING = dict

    ALL_JSON_SERIALIZABLES = JSON_PRIMITIVES + JSON_SEQ + (JSON_MAPPING, )

    @classmethod
    def _get_json_error_keys(cls, obj, json_path='storage'):
        """Identify the paths with the storage which failed to be JSON encoded.

        Return an iterable of message strings.

        """
        if isinstance(obj, dict):
            # TODO: also check/report that k is a string, as only strings are
            # valid as object keys in JSON.
            for k, v in obj.items():
                if isinstance(v, cls.JSON_PRIMITIVES):
                    continue
                subpath = '{}[{!r}]'.format(json_path, k)
                yield from cls._get_json_error_keys(v, subpath)
        elif isinstance(obj, (list, tuple)):
            for i, value in enumerate(obj):
                if isinstance(value, cls.JSON_PRIMITIVES):
                    continue
                subpath = '{}[{}]'.format(json_path, i)
                yield from cls._get_json_error_keys(value, subpath)
        elif isinstance(obj, cls.JSON_PRIMITIVES):
            return
        else:
            # TODO: Could have a custom JSONEncoder in the future, in which
            # case we would have to actually run json.dumps on it to get the
            # result and possibly even drill down on the parameters we got
            # back, if that object happens to have a list as an attribute, for
            # example.
            t = type(obj)
            if t.__module__ != 'builtins':
                typename = '{t.__module__}.{t.__qualname__}'.format(t=t)
            else:
                typename = t.__qualname__
            yield json_path, typename


storage = Storage()
