from typing import Sequence
import plotly
import plotly.graph_objects as go
from itertools import zip_longest
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


dark = "#3a4b6f"
black = "#20293d"


def colormap(cm, n):
    """
    colormap: 'autumn', 'cool', 'copper', 'flag', 'gray', 'hot', 'hsv', 'jet', 'pink', 'prism', 'spring',
    'summer', 'winter', 'magma', 'inferno', 'plasma', 'viridis', 'nipy_spectral'
    """
    rgba = []
    cm = plt.get_cmap(cm, n)
    for i in range(cm.N):
        # r, g, b, a = cm(i) * 256
        r, g, b, a = list(map(lambda x: x * 255, cm(i)))
        # rgba.append(f"rgba({r},{g},{b},{a})")
        rgba.append((r,g,b,a))

    return rgba


class ScatterPlot:
    """
    >>> plot = ScatterPlot()
    >>> plot.layout["xaxis"] = {'range': [-1,1]}
    """

    def __init__(
        self,
        *,
        template="plotly_white",
        width=600,
        height=400,
        autosize=True,
        showlegend=False,
        font={"size": 12, "color": black},
        xaxis={
            "title": "",
            "type": "linear",
            "color": black,
            "linewidth": 1,
            "linecolor": black,
            "mirror": True,
            "autorange": True,
            "tickmode": "auto",
        },
        yaxis={
            "title": "",
            "type": "linear",
            "color": black,
            "linewidth": 1,
            "linecolor": black,
            "mirror": True,
            "autorange": True,
            "tickmode": "auto",
        },
        **kwargs,
    ):

        # if np.size(np.shape(y)) == 1:
        #     self.dim = 1
        # elif np.size(np.shape(y)) == 2:
        #     self.dim = np.shape(y)[0]
        # else:
        #     raise ValueError('invalid')
        self.layout = dict(
            template=template,
            width=width,
            height=height,
            autosize=autosize,
            showlegend=showlegend,
            font=font,
            xaxis=xaxis,
            yaxis=yaxis,
        )

        for key, value in kwargs.items():
            self.layout[key] = value

        self.fig = go.Figure(layout=self.layout)

    def save(self, file):
        # fig = {'data': self.data, 'layout': self.layout}
        plotly.io.write_image(self.fig, file)
        return

    def show(self):
        # self.fig.show()
        return

    def plot(
        self,
        x: Sequence,
        y: Sequence,
        *,
        name=None,
        mode="lines+markers",
        line={"width": 2, "color": dark},
        marker={"symbol": "circle", "size": 6, "color": dark},
        showlegend=True,
        cmap="tab20b",
    ):

        if len(np.shape(y)) == 1:
            y = [y]
            total_line = 1
        else:
            total_line = np.shape(y)[0]

        if len(np.shape(x)) == 1:
            _x = [x]

        data = []
        for n, (x, y) in enumerate(zip_longest(_x, y, fillvalue=x)):
            # print(n, x, y)
            color = colormap(cmap, total_line)
            line['color'] =f'rgba{color[n]}'
            marker['color'] =f'rgba{color[n]}'
            # print(f'rgba{color[n]}')
            dt = go.Scatter(
                x=x,
                y=y,
                name=name,
                mode=mode,
                line=line,
                marker=marker,
                showlegend=showlegend,
            )

            data.append(dt)

        self.fig.add_traces(data)
        return

    def update(self, target, props):
        if isinstance(target, str):
            target = [target]

        for t in target:
            for k, v in props.items():
                self.layout[t][k] = v


if __name__ == "__main__":
    x = np.linspace(-5,5)
    y = [np.cos(x), np.sin(x), np.tanh(x), x/5]
    # y = [[2, 4, 6], [5,6,7]]
    plot = ScatterPlot()
    # plot.update(["xaxis", "yaxis"], {'range': [-10,10], 'linewidth': 3})
    # plot.update('yaxis', {'type':'log'})
    # print(plot.layout)

    plot.plot(x, y)
    # plot.save("./test.pdf")
