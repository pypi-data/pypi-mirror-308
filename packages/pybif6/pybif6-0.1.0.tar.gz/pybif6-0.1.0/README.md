# pybif6

This tiny project rewrites [the BIF6 file parsing part] of [the R package `tofsims`] in Python.

[the BIF6 file parsing part]: https://github.com/lorenzgerber/tofsims/blob/master/src/c_importer.cpp
[the R package `tofsims`]: https://github.com/lorenzgerber/tofsims

## Usage

```python
import pybif6

for inteval_image in pybif6.parse_bif6("path/to/bif6/file"):
    print(
        f'id: {inteval_image.id}, '
        f'mz_lower: {inteval_image.mz_lower}, '
        f'mz_middle: {inteval_image.mz_middle}, '
        f'mz_upper: {inteval_image.mz_upper}, '
        f'image: {inteval_image.image.shape}'
    )
    # The image data is stored in `inteval_image.image`, a 2D numpy array.
```
