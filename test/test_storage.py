import unittest
from unittest import mock
from unittest.mock import patch
from io import StringIO

from pgturbo.storage import Storage
from pgturbo.rect import ZRect


class CannotBeSerialized:
    """Stub to check that setting values in storage errors correctly."""


class StorageStaticMethodsTest(unittest.TestCase):
    def test_dict_with_no_errors(self):
        obj = {'level': 10, 'player_name': 'Daniel'}

        result = list(Storage._get_json_error_keys(obj))
        self.assertEqual(result, [])

    def test_dict_with_errors(self):
        obj = {'level': 10, 'player_name': 'Daniel', 'obj': object()}

        result = list(Storage._get_json_error_keys(obj))
        self.assertEqual(
            result,
            [("storage['obj']", "object")]
        )

    def test_dict_with_nested_dicts_errors(self):
        subobj0 = {'this_key_fails': object()}
        subobj1 = {'a': 10, 'b': {1, 2, 3}, 'c': 30, 'obj': subobj0}
        subobj2 = {'player_name': 'Daniel', 'level': 20, 'states': subobj1}
        obj = {'game': 'my_game', 'state': subobj2}

        result = sorted(Storage._get_json_error_keys(obj))
        self.assertEqual(result, [
            ("storage['state']['states']['b']", 'set'),
            ("storage['state']['states']['obj']['this_key_fails']", 'object'),
        ])

    def test_invalid_list_item(self):
        """We can report the index of an unserialisable list item."""
        obj = {'items': [1, 5, ZRect(0, 0, 10, 10)]}

        result = sorted(Storage._get_json_error_keys(obj))
        self.assertEqual(result, [
            ("storage['items'][2]", 'pgturbo.rect.ZRect'),
        ])


class StorageTest(unittest.TestCase):
    @patch('pgturbo.storage.os.path.exists')
    def setUp(self, exists_mock):
        exists_mock.return_value = True
        self.storage = Storage('asdf')

    def test_load_nothing(self):
        """We can load() when there is no data without issue."""
        self.storage.load()
        # Since there is not data to load, the storage.loaded property stays
        # False.
        self.assertFalse(self.storage.loaded)

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_load(self):
        """We can load existing data correctly."""
        self.assertEqual(list(self.storage.items()), [])
        self.storage.load()
        self.assertEqual(list(self.storage.items()), [("a", "hello")])

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_dict_style_get(self):
        """We can use storage like a normal dictionary to check values."""
        self.storage.load()
        self.assertEqual(self.storage['a'], 'hello')

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_dict_style_set(self):
        """We can use storage like a normal dictionary to set values."""
        self.storage.load()
        self.storage["a"] = "bye"
        self.assertEqual(self.storage['a'], 'bye')

    def test_dict_style_set_errors_on_wrong_types(self):
        """If types that are not JSON serializable are used in storage,
        a descriptive error is thrown."""
        with self.assertRaises(TypeError):
            # Not just any object can be stored.
            self.storage["a"] = CannotBeSerialized()

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_get_with_existing_key(self):
        """We can get values via .get() as well."""
        self.storage.load()
        self.assertEqual(self.storage.get("a"), "hello")

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_get_with_default_value(self):
        """We get a default value with .get() if provided and the key is
        missing from storage."""
        self.storage.load()
        self.assertEqual(self.storage.get("b", "fallback"), "fallback")

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_get_with_no_default_value(self):
        """If we didn't specify a fallback, None is returned by .get()."""
        self.storage.load()
        self.assertIsNone(self.storage.get("b"))

    def test_setdefault_with_empty(self):
        """We can create keys and values via .setdefault if there is no
        previous storage."""
        self.storage.setdefault("a", "bye")
        self.assertEqual(self.storage["a"], "bye")

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_setdefault_with_no_key(self):
        """If there is previous storage, we can still create new keys and
        values with .setdefault()."""
        self.storage.load()
        self.storage.setdefault("b", "c")
        self.assertEqual(self.storage["b"], "c")

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_setdefault_with_existing_key(self):
        """If the same key exists already, .setdefault() does not overwrite
        its value."""
        self.storage.load()
        self.storage.setdefault("a", "bye")
        self.assertEqual(self.storage["a"], "hello")

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_clear(self):
        """We can empty the current storage state."""
        self.storage.load()
        self.assertEqual(self.storage["a"], "hello")
        self.storage.clear()
        self.assertEqual(len(self.storage), 0)

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_clear_does_not_save(self):
        """Clearing current storage does not automatically save the emptied
        state to disk."""
        self.storage.load()
        self.assertEqual(self.storage["a"], "hello")
        self.storage.clear()
        self.assertEqual(len(self.storage), 0)
        self.storage.load()
        self.assertEqual(self.storage["a"], "hello")

    def test_save_with_empty_does_nothing(self):
        """Trying to save when there is no data to save doesn't open any
        files."""
        with patch("builtins.open", mock.mock_open()) as mock_file:
            self.storage.save()
        mock_file.assert_not_called()

    # This patch suppresses the print outputs when saving to files.
    @patch("sys.stdout", new=StringIO())
    def test_save_with_content(self):
        """We can save the storage dict to disk when there is no previous
        file."""
        self.storage["a"] = "hello"
        with patch("builtins.open", mock.mock_open()) as mock_file:
            self.storage.save()
        mock_file.assert_called_once()
        handle = mock_file()
        handle.write.assert_called_once_with('{"a": "hello"}')

    @patch("sys.stdout", new=StringIO())
    @patch('builtins.open', mock.mock_open(read_data='{"a": "hi", "b": "c"}'))
    def test_save_with_overwrite(self):
        """If there is a previous file, saving will overwrite it."""
        self.storage.load()
        self.storage["a"] = "bye"
        with patch("builtins.open", mock.mock_open()) as mock_file:
            self.storage.save()
        mock_file.assert_called_once()
        handle = mock_file()
        handle.write.assert_called_once_with('{"a": "bye", "b": "c"}')

    def test_autosave_default_is_off(self):
        """By default, autosaving for storage is False and thus turned off."""
        self.storage._save = mock.Mock()
        self.assertFalse(self.storage.autosave)
        self.storage["a"] = "hi"
        self.storage._save.assert_not_called()

    def test_autosave(self):
        """If turned on, autosaving will mean .save() is called whenever a
        value is changed via storage[key] = value."""
        self.storage._save = mock.Mock()
        # Simply setting the property should not immediately save.
        self.storage.autosave = True
        self.storage._save.assert_not_called()
        self.storage["a"] = "hi"
        # After having set a value, the autosave should have happened.
        self.storage._save.assert_called_once()

    def test_autosave_type_errors_with_none_boolean(self):
        """If the user tries to set storage.autosave with an illegal value,
        a descriptive error is raised."""
        with self.assertRaises(TypeError):
            self.storage.autosave = 5

    def test_setup_with_empty_before(self):
        """We can use storage.setup() to create our initial storage state."""
        with (patch("builtins.open", mock.mock_open()) as mock_file,
                # We have to mock json.load() as well here since it otherwise
                # reports a parsing error. This is not present in real use
                # since in real use the same logic would block beforehand since
                # no file exists. Here it's only a problem because we have to
                # mock open() and thus the code thinks a file exists to parse.
                patch("json.load", mock.Mock()) as json_mock):
            json_mock.return_value = ""
            self.storage.setup({"a": "hi"})
        self.assertEqual(self.storage["a"], "hi")
        # open() should have been called once to try and load a previously
        # saved state.
        mock_file.assert_called_once()

    def test_setup_with_data_before(self):
        """We can use setup and it will create new keys but not overwrite
        existing values."""
        with (patch("builtins.open", mock.mock_open(read_data='{"a": "bye"}'))
                as mock_file):
            self.storage.setup({"a": "hi", "b": "c"})
        self.assertEqual(self.storage["a"], "bye")
        self.assertEqual(self.storage["b"], "c")
        mock_file.assert_called_once()

    def test_overwrite_with_empty_before(self):
        """We can use storage.overwrite() to quickly set all values of
        storage."""
        self.storage.overwrite({"a": "hi", "b": "c"})

        self.assertEqual(self.storage["a"], "hi")
        self.assertEqual(self.storage["b"], "c")

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hi", "c": "b"}'))
    def test_overwrite_with_content_before(self):
        """If there are existing key value pairs, they are overwritten and
        ones not in the new dict are erased."""
        self.storage.load()
        self.assertEqual(self.storage["a"], "hi")
        self.assertEqual(self.storage["c"], "b")

        self.storage.overwrite({"a": "hi", "b": "c"})

        self.assertEqual(self.storage["a"], "hi")
        self.assertEqual(self.storage["b"], "c")
        with self.assertRaises(KeyError):
            self.storage["c"]

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hi", "c": "b"}'))
    def test_overwrite_does_not_save(self):
        """In contrast to storage.setup(), .overwrite() does not save its
        changes automatically."""
        self.storage.load()
        self.assertEqual(self.storage["a"], "hi")
        self.assertEqual(self.storage["c"], "b")

        self.storage.overwrite({"a": "hi", "b": "c"})

        self.assertEqual(self.storage["a"], "hi")
        self.assertEqual(self.storage["b"], "c")
        with self.assertRaises(KeyError):
            self.storage["c"]

        # New in comparison to test above. These asserts can only work if
        # .overwrite() did not save to disk.
        self.storage.load()
        self.assertEqual(self.storage["a"], "hi")
        self.assertEqual(self.storage["c"], "b")
        with self.assertRaises(KeyError):
            self.storage["b"]
