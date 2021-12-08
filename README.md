# csce312-cache-sim :computer:

Work for TAMU CSCE 312 Kebo Project - Cache Simulator

**Authors:**

- John Gutierrez
- Cameron Herring

## Usage

Installing this package:

```shell
git clone https://github.com/XDwightsBeetsX/csce312-cache-sim
```

- Running the Cache with python
  - requires input.txt with the input RAM in the form:

    ```txt
    08
    6F
    8D
    6A
    C8
    0C
    D1
    ```

```shell
python cachesimulator.py input.txt
```

## Commands

| command         | arguments | description |
| :--             | :-:       | :--         |
| `init-ram`      | ramStart(hex) ramEnd(hex) | initializes the ram of size (ramEnd-ramStart+1) |
| `cache-read`    | instruction(hex) | `instruction` is decomposed into a *set index*, *tag*, and an *offset*. The cache at this location is read and reported.
| `cache-write`   | instruction(hex) dataToWrite(hex) | Decomposes the `insruction` like cache-read, and writes the `dataToWrite` to that location.
| `cache-flush`   | *none* | replaces the cache contents with all 0s |
| `cache-view`    | *none* | displays the current cache contents. |
| `memory-view`   | *none* | displays the current RAM contents. |
| `cache-dump`    | *none* | writes the current cache contents to file `cache.txt` |
| `memory-dump`   | *none* | writes the current RAM contents to file `ram.txt` |
| `quit`          | *none* | exits the program. |

## Documentation with [Doxygen](https://www.doxygen.nl/manual/docblocks.html#pythonblocks)

- comments -> documentation
