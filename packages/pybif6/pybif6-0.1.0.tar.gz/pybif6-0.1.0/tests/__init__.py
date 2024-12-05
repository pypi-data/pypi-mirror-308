import unittest

import numpy as np
from pybif6 import (
    parse_bif6,
    BIF6FileParser,
    BIF6Interval
)

class TestBIF6(unittest.TestCase):
    def test_bif6(self):
        """Test BIF6 parsing"""
        parser: BIF6FileParser = parse_bif6(
            '/path/to/my/local/test/file.bif6',
        )
        self.assertIsInstance(parser, BIF6FileParser)
        x, y = parser.image_size
        interval: BIF6Interval = next(parser)
        self.assertIsInstance(interval, BIF6Interval)
        self.assertEqual(interval.image.shape, (x, y))
        self.assertEqual(interval.image.dtype, np.uint32)
        self.assertTrue(interval.is_tic_image())
        parser.close()


if __name__ == '__main__':
    unittest.main()

