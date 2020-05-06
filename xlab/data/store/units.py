from typing import NewType

# A practical precision for saving data points.
# This also helps ignore loss of precision in various cases.
Seconds = NewType('Seconds', int)
