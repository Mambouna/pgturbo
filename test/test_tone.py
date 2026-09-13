from unittest import TestCase
from unittest.mock import patch, Mock

from pgturbo.tone import _convert_args, play, create, ToneParams
from pygame.mixer import Sound


TEST_NOTES = {
    'A4': dict(val=0, hertz=440, parts=('A', '', 4)),
    'C4': dict(val=-9, hertz=261.63, parts=('C', '', 4)),
    'C0': dict(val=-57, hertz=16.35, parts=('C', '', 0)),
    'B8': dict(val=50, hertz=7902.13, parts=('B', '', 8)),
    'A#4': dict(val=1, hertz=466.16, parts=('A', '#', 4)),
    'Ab4': dict(val=-1, hertz=415.30, parts=('A', 'b', 4)),
    'Bb4': dict(val=1, hertz=466.16, parts=('B', 'b', 4)),
}


class ToneTest(TestCase):
    def test_invalid_note(self):
        """Invalid note names raise descriptive errors."""
        for note in ['A9', 'H4', '4A', 'a4', 'Az4']:
            with self.assertRaises(ValueError):
                _convert_args(note, 1.0, 0.75)

    def test_note_to_hertz(self):
        """Valid note strings are correctly converted to frequencies."""
        for note, val in TEST_NOTES.items():
            params = _convert_args(note, 1.0, 0.75)
            self.assertAlmostEqual(params.hz, val['hertz'], delta=0.1)

    def test_create(self):
        """We can create pygame.mixer.Sound objects with tone.create()."""
        snd = create("A4", 2.0, 0.6)
        self.assertIsInstance(snd, Sound)
        self.assertEqual(snd.get_length(), 2.0)
        # Because pygame represents the sound volume internally with
        # only a range of 128 possible values, precision is always lost.
        self.assertAlmostEqual(snd.get_volume(), 0.6, delta=0.01)

    def test_default_volume(self):
        """By default, volume is 0.75."""
        snd = create("A4", 1.0)
        # Because pygame represents the sound volume internally with
        # only a range of 128 possible values, precision is always lost.
        self.assertAlmostEqual(snd.get_volume(), 0.75, delta=0.01)

    def test_max_length(self):
        """Tones loner than 4 seconds raise an error."""
        # A tone of length 4 seconds is fine.
        snd = create("A4", 4.0)
        self.assertEqual(snd.get_length(), 4.0)
        with self.assertRaises(ValueError):
            # A tone of length greater than 4 seconds is not.
            snd = create("A4", 4.0000001)

    def test_play(self):
        """We can have PGTurbo create and then directly play a tone as well."""
        # Since unittesting threading isn't something I'm familiar with, for
        # now we just make sure play() puts everything in the queue correctly.
        with patch("pgturbo.tone.note_queue.put", Mock()) as mock_queue_put:
            play("A4", 2.0, 0.1)
        mock_queue_put.assert_called_once_with(
            ToneParams(hz=440.0, duration=2.0, volume=0.1)
        )
