# yuxin_helpers

Yuxin's helper package with utilities for diverse tasks.

## Installation

```bash
pip install yuxin_helpers
```

## Usage

### Convert RGB to Hex

```python
from yuxin_helpers.colors import rgb_to_hex

print(rgb_to_hex(255, 0, 0))  # Output: '#ff0000'
```

### Convert Hex to RGB

```python
from yuxin_helpers.colors import hex_to_rgb

print(hex_to_rgb('#ff0000'))  # Output: (255, 0, 0)
```

### Truncate a Colormap

```python
import matplotlib.pyplot as plt
import numpy as np
from yuxin_helpers.colors import truncate_colormap

# Example usage
cmap = plt.get_cmap('viridis')
truncated_cmap = truncate_colormap(cmap, minval=0.2, maxval=0.8, n=200)

# Plotting to visualize the truncated colormap
plt.imshow(np.linspace(0, 1, 100).reshape(10, 10), cmap=truncated_cmap)
plt.colorbar()
plt.show()
```

### Create a Custom Colormap from Data

```python
import matplotlib.pyplot as plt
import numpy as np
from yuxin_helpers.colors import create_cmap_from_data

# Sample data
data = np.random.randn(100, 100)

# Create a custom colormap with a segmentation value
custom_cmap = create_cmap_from_data(data, seg_value=0, cmap='coolwarm')

# Plotting to visualize the custom colormap
plt.imshow(data, cmap=custom_cmap)
plt.colorbar()
plt.show()
```