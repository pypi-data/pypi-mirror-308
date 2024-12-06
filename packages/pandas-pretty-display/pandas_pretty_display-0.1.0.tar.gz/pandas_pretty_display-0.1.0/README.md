# Pandas Pretty Display

A simple Python package to make your pandas DataFrames look beautiful in Jupyter notebooks with alternating colors and improved formatting.

## Installation

You can install the package via pip:

```bash
pip install pandas-pretty-display
```

## Usage

```python
from pandas_pretty_display import style_dataframe
import pandas as pd

# Create or load your DataFrame
df = pd.DataFrame(...)

# Apply the styling
style_dataframe()

# Display your DataFrame - it will now have the pretty styling
display(df)
```

## Features

- Alternating gold and light blue row colors
- Black text in table cells
- Red text in table headers
- Black borders around cells
- 18px font size
- Full-width container
- Scrollable output up to 1000px height

## Requirements

- Python >= 3.6
- pandas >= 1.0.0
- IPython >= 7.0.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.
