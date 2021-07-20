import os


base_path = os.environ['SORTLEDTON_PLOTS_DIR']


def blend(color, factor):
    return int(255 - (255 - color) * factor)


def rgb(red, green, blue, factor=1):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (blend(red, factor), blend(green, factor), blend(blue, factor))


colors = {
    'blue': rgb(55, 126, 184),
    'lightblue': rgb(55, 126, 184, 0.6),
    'green': rgb(77, 175, 74),
    'lightgreen': rgb(77, 175, 74, 0.6),
    'orange': rgb(255, 127, 0),
    'lightorange': rgb(255, 127, 0, 0.75),
    'red': rgb(228, 26, 28),
    'lightred': rgb(228, 26, 28, 0.75),
    'black': rgb(0, 0, 0)
}


from matplotlib.ticker import FuncFormatter


def kilos(x, pos):
    """The two args are the value and tick position"""
    return '%1.0f\\,K' % (x * 1e-3)


def millions(x, pos):
    """The two args are the value and tick position"""
    if x:
        return '%1.0f\\,M' % (x * 1e-6)
    else:
        return '0'


def billions(x, pos):
    """The two args are the value and tick position"""
    if x == 0:
        return '0'
    elif x < 1e8:
        return '%1.0f\\,M' % (x * 1e-6)
    elif x < 1e10:
        return '%1.1f\\,G' % (x * 1e-9)
    else:
        return '%1.0f\\,G' % (x * 1e-9)


def billions2(x, pos):
    """The two args are the value and tick position"""
    if x == 0:
        return '0'
    else:
        return '%1.0f\\,G' % (x * 1e-9)

def speedup(x, pos):
    sign = '+' if x > 0 else ''
    return sign + '%.0f' % (x * 100) + '\%'
    
def perc(x, pos):
    return '%.0f' % (x * 100) + '\%'


def perc2(x, pos):
    return '%.0f' % (x) + '\%'


kilos = FuncFormatter(kilos)
mills = FuncFormatter(millions)
gigs = FuncFormatter(billions)
gigs2 = FuncFormatter(billions2)
percent = FuncFormatter(perc)
percent2 = FuncFormatter(perc2)


markers = {
    'circle': 'o',
    'triangle': '^',
    'square': 's',
    'diamond': 'D'
}

def extract(rows: [dict], index: int, xaxis: str, yaxis: str):
    return rows[index][yaxis]


def extract_time(rows: [dict], index: int, xaxis: str, yaxis: str):
    return rows[index]['real_time']


def extract_throughput(rows: [dict], index: int, xaxis: str, yaxis: str):
    if rows[index]['fixture'] == 'Count':
        return rows[index]['n_elements_lookup'] * 1000 / rows[index]['real_time']
    else:
        return rows[index]['n_elements_build'] * 1000 / rows[index]['real_time']


def extract_speedup(rows: [dict], index: int, xaxis: str, yaxis: str):
    return rows[0]['real_time'] / rows[index]['real_time']


yconverter = {
    'time': extract_time,
    'throughput': extract_throughput,
    'speedup': extract_speedup,
    'DTLB-misses': extract,
    'ITLB-misses': extract,
    'L1D-misses': extract,
    'L1I-misses': extract,
    'LLC-misses': extract,
    'branch-misses': extract,
    'cycles': extract,
    'instructions': extract,
    'task-clock': extract,
    'avg_size': extract,
    'size': extract,
    'bits': extract,
    'retries': extract,
    'fpr': extract
}

xscale = {
    'k': 'linear',
    's': 'linear',
    'n_threads': 'linear',
    'n_partitions': 'log',
    'n_elements_build': 'log',
    'n_elements_lookup': 'log',
    'shared_elements': 'linear'
}


import pandas as pd


def read_benchmark(path: str):
    csv = pd.read_csv(path)

    split_name = csv['name'].apply(lambda x: x.split('/')[0].split('_'))

    csv['k'] = split_name.apply(lambda x: int(x[len(x) - 1]))
    csv['fixture'] = csv['name'].apply(lambda x: x.split('/')[1])
    csv['s'] = csv['name'].apply(lambda x: float(x.split('/')[2]) / 100)
    csv['n_threads'] = csv['name'].apply(lambda x: int(x.split('/')[3]))
    csv['n_partitions'] = csv['name'].apply(lambda x: int(x.split('/')[4]))
    csv['n_elements_build'] = csv['name'].apply(lambda x: int(x.split('/')[5]))
    csv['n_elements_lookup'] = csv['name'].apply(lambda x: int(x.split('/')[6]))
    csv['shared_elements'] = csv['name'].apply(lambda x: float(x.split('/')[7]) / 100)

    csv['name'] = split_name.apply(lambda x: "\_".join(x[0:(len(x) - 1)]))

    data = {}
    for _, row in csv.iterrows():
        data_row = {}
        for label, item in row.iteritems():
            data_row[label] = item

        name = row['name']
        if name not in data:
            data[name] = []
        data[name].append(data_row)

    return data


import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FuncFormatter
from matplotlib.patches import Rectangle
import numpy as np


def latexify(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    assert (columns in [1, 2])

    if fig_width is None:
        fig_width = 3.39 if columns == 1 else 6.9  # width in inches

    if fig_height is None:
        golden_mean = (np.sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
        fig_height = fig_width * golden_mean  # height in inches

    MAX_HEIGHT_INCHES = 32.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height +
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {'backend': 'ps',
              'pgf.rcfonts': False,
              'axes.labelsize': 8,  # fontsize for x and y labels (was 10)
              'axes.titlesize': 8,
              'font.size': 8,  # was 10
              'legend.fontsize': 6,  # was 8 # was 10
              'legend.handlelength': 1.5,
              'legend.handletextpad': 0.3,
              'legend.labelspacing': 0.1, # was 0.1
              'legend.columnspacing': 0.3,
              'legend.borderpad': 0.3,
              'xtick.labelsize': 7,
              'ytick.labelsize': 7,
              'axes.labelpad': 1,
              'axes.titlepad': 2,
              'text.usetex': True,
              'figure.figsize': [fig_width, fig_height],
              'font.family': 'sans-serif',
              'text.latex.preamble': r'\usepackage{amssymb} \usepackage{ifsym}',
              'figure.dpi': 400
              }
    
    matplotlib.rcParams.update(params)


def format_axes(ax, xscale='linear', yscale='linear'):
    spine_color = 'black'
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(spine_color)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction='out', color=spine_color)
    
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction='out', color=spine_color)
    ax.yaxis.grid(b=True, which='both')

    ax.tick_params(axis='both', which='major', pad=0.5)

    return ax


def add_line_on_1(plot):
    plot.axhline(y = 1, color="black", linestyle = '-', linewidth=2)

def barAxes(ax):
    ax.set_axisbelow(True)


def cm2inch(value):
    return value / 2.54


def reorderLegend(ax=None, order=None, unique=False):
    if ax is None: ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))  # sort both labels and handles by labels
    if order is not None:  # Sort according to a given list (not necessarily complete)
        keys = dict(zip(order, range(len(order))))
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t, keys=keys: keys.get(t[0], np.inf)))
    if unique:
        labels, handles = zip(*unique_everseen(zip(labels, handles), key=labels))  # Keep only the first of each handle
    return handles, labels


