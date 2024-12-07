# pyvisacharts

This package wraps [@visa/charts](https://github.com/visa/visa-chart-components/tree/main/packagescharts) web components for use in [Python](https://www.python.org/) and [jupyter notebooks](https://jupyter.org/), leveraging the [widget-cookiecutter](https://github.com/jupyter-widgets/widget-cookiecutter) Python package. You can find pyvisacharts on [pypi](https://pypi.org/project/pyvisacharts/), installation steps provided below.

---

### Installation Steps

- Using `pip`:
  ```
  $ pip install pyvisacharts
  ```
- or `conda`:
  ```
  $ conda install -c conda-forge pyvisacharts
  ```

---

#### Components with `Ready` status in this bundle

- [@visa/bar-chart](https://github.com/visa/visa-chart-components/tree/main/packagesbar-chart)
- [@visa/clustered-bar-chart](https://github.com/visa/visa-chart-components/tree/main/packagesclustered-bar-chart)
- [@visa/stacked-bar-chart](https://github.com/visa/visa-chart-components/tree/main/packagesstacked-bar-chart)
- [@visa/line-chart](https://github.com/visa/visa-chart-components/tree/main/packagesline-chart)
- [@visa/pie-chart](https://github.com/visa/visa-chart-components/tree/main/packagespie-chart)
- [@visa/scatter-plot](https://github.com/visa/visa-chart-components/tree/main/packagesscatter-plot)
- [@visa/heat-map](https://github.com/visa/visa-chart-components/tree/main/packagesheat-map)
- [@visa/circle-packing](https://github.com/visa/visa-chart-components/tree/main/packagescircle-packing)
- [@visa/parallel-plot](https://github.com/visa/visa-chart-components/tree/main/packagesparallel-plot)
- [@visa/dumbbell-plot](https://github.com/visa/visa-chart-components/tree/main/packagesdumbbell-plot)
- [@visa/world-map](https://github.com/visa/visa-chart-components/tree/main/packagesworld-map)
- [@visa/alluvial-diagram](https://github.com/visa/visa-chart-components/tree/main/packagesalluvial-diagram)

## <!-- #### Components with `Development` status -->

#### <a name="Python_components" href="#Python_components">#</a> Use VCC as Python functions

<br>

Step 1: Install:

```
$ pip install pyvisacharts
```

Step 2: Use component as any other Python function

```python
import pyvisacharts as vcc
import pandas as pd

bar_chart_data = pd.read_json("https://github.com/visa/visa-chart-components/tree/main/packages/charts-pythondocs/demo_data/bar_chart_data.json")
line_chart_data = pd.read_json("https://github.com/visa/visa-chart-components/tree/main/packages/charts-pythondocs/demo_data/line_chart_data.json")

vcc.BarChart(
    accessibility={
        "purpose": "Demonstration of a bar chart built with VCC and minimal properties provided.",
        "statisticalNotes": "This chart is using dummy data."
    },
    data=bar_chart_data,
    ordinalAccessor="item",
    valueAccessor="value"
)

vcc.LineChart(
    accessibility={
        "purpose": "Demonstration of a line chart built with VCC and minimal properties provided.",
        "statisticalNotes": "This chart is using dummy data."
    },
    data=line_chart_data, # a pandas data frame
    ordinalAccessor="date",
    valueAccessor="value",
    seriesAccessor="category",
    config={
        "hoverOpacity": 0.25
    }
)
```

See our [VCC Demo Notebook](https://github.com/visa/visa-chart-components/tree/main/packages/charts-pythondocs/VCC%20Demo%20Notebook.ipynb) for more examples.

<hr>

### Development Steps

To the python widget locally, you will need to follow the below installation and build steps to symlink the necessary packages across the monorepo.

```
    $ yarn
    $ yarn dev --i
    $ yarn dev --b
    $ yarn dev --ipy
    $ yarn dev --spy (spins up a local jupyter notebook)
    or
    $ yarn dev --lpy (spins up a local jupyter lab)
```

After running these commands, the js lib `@visa/charts` will by symlink'd and a jupyter notebook will be spun up locally for development and testing work. If you update the js build and/or python code you will likely need to restart/refresh the juptyer notebook to see development changes reflected.

In addition to the core project team, special thanks to Luis Chaves Rodriguez ([@visa](https://github.com/luis-chaves-visa)) for his assistance in development of `pyvisacharts`.
