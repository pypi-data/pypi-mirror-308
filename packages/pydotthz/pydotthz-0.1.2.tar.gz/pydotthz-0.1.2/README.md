# Interface with dotThz files using Python

This crate provides an easy way to interface with [dotThz](https://github.com/dotTHzTAG) files in Python.

Install it

```shell
pip install pydotthz
```

and then use like specified in the following example:

```python
from pathlib import Path
import numpy as np

from dotthz import DotthzFile, DotthzMeasurement, DotthzMetaData

if __name__ == "__main__":
    # Sample data
    time = np.linspace(0, 1, 100)  # your time array
    data = np.random.rand(100)  # example 3D data array

    file = DotthzFile()

    measurement = DotthzMeasurement()
    # for thzVer 1.00, we need to transpose the array!
    measurement.datasets = {"Sample": np.array([time, data]).T}

    # set meta_data
    meta_data = DotthzMetaData()
    meta_data.user = "John Doe"
    meta_data.version = "1.00"
    meta_data.instrument = "Toptica TeraFlash Pro"
    meta_data.mode = "THz-TDS/Transmission"

    measurement.meta_data = meta_data

    file.groups["Measurement"] = measurement

    # save the file
    file.save(Path("test.thz"))

    # open the file again
    path = Path("test.thz")
    file = DotthzFile.load(path)

    # read the first group (measurement)
    key = list(file.groups.keys())[0]
    print(file.groups.get(key).meta_data)
    print(file.groups.get(key).datasets)

```
Requires hdf5 to be installed.
