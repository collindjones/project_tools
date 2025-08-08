import config
from IPython.display import display as display_fig
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
import numpy as np

ix = pd.IndexSlice
colors = [ \
           (0, 24, 113), \
           (92, 36, 218), \
           (84, 161, 54), \
           (190, 77, 0), \
           (125, 125, 125), \
           (130, 63, 152), \
           (26, 160, 193), \
           (226, 5, 111), \
           (230, 137, 0), \
           (79, 5, 133), \
           (3, 10, 23), \
           (51, 51, 51), \
           (15, 163, 158), \
           (148, 90, 3), \
           (158, 3, 132)]

colors = [(c[0]/255, c[1]/255, c[2]/255) for c in colors]


def plot(ys, x, fig, axs, data = pd.DataFrame(), name = 'last', labels = [],
         dates = [], to_scatter = [], yaxis2 = [], \
         linestyle=[]):
    """
    Plot one or more data series from the same pandas DataFrame. Plots can
    be line plots, scatter plots, or some combination of the two.

    Parameters
    ----------
    ys : list of strings
        Columns from the DataFrame to plot. Should include everything plotted --
        whether in line or scatter.
    x : string
        x-axis variable. Frequently will be a date. Cannot be the index of the
        DataFrame.
    data : pandas DataFrame
        DataFrame including all of the data. The easiest way to implement a
        restriction on the plot (e.g. min or max x value) is to pass an
        already-selected segment.
    name : filename for the plot
        filename for the plot. If blank, no file will be saved.
    labels: list of strings
        labels for each variable, in the order they appeared in ys. If given
        nothing, will use the names of the columns
    output: string
        Directory for file to be saved.
    dates: list of strings
        Columns to convert to datetime, before plotting
    to_scatter: list of strings
        Subset of columns to plot as scatterplot. Default is line.
    yaxis2: list of strings
        Subset of columns to attach to a secondary y-axis. Default is primary
        y-axis

    Returns
    -------
    Nothing

    Examples
    --------
    See example notebook

    """
    plt.close('all')
    date_format = mdates.DateFormatter('%b-%Y')
    legend_loc = (0.5, -0.15)
    for d in dates:
        data[d] = pd.to_datetime(data[d])
    # fig, axs = plt.subplots(1, 1, figsize=(15, 10))
    if len(yaxis2) > 0:
        axs2 = axs.twinx()
    plt.tight_layout(pad=10)

    if len(labels) == 0:
        labels = ys

    if len(linestyle) == 0:
        linestyle = ['-' for i in ys]

    for i, y in enumerate(ys):
        if y not in yaxis2:
            if y not in to_scatter:
                axs.plot(x, y, data=data, label=labels[i], color = colors[i], linestyle=linestyle[i])
            else:
                axs.scatter(data=data, x=x, y=y,
                            label=labels[i], color=colors[i])
        else:
            if y not in to_scatter:
                axs2.plot(x, y, data=data, label=labels[i], color=colors[i], linestyle = linestyle[i])
            else:
                axs2.scatter(data=data, x=x, y=y, label = labels[i],
                             color=colors[i])
    axs.xaxis.set_major_formatter(date_format)
    axs.tick_params(axis='x', labelsize=18)
    axs.tick_params(axis='y', labelsize=18)
    if len(yaxis2) == 0:
        axs.legend(loc='lower center', bbox_to_anchor=legend_loc,
                   ncol=3, fontsize=18)
    else:
        lines_1, labels_1 = axs.get_legend_handles_labels()
        lines_2, labels_2 = axs2.get_legend_handles_labels()
        axs.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower center',
                   bbox_to_anchor=legend_loc, ncol=2,
                   columnspacing=1, fontsize=18)
        axs2.tick_params(axis='y', labelsize=18)
    # if len(name) > 0:
    #     fig.savefig(output / '{}.{}'.format(name, ext), format=ext)
    # plt.close(fig)
    # display_fig(fig)
    return axs


def plot_termstructure(df, y=['yld_last'], output='./', dts_plot=['01-10-2024'], \
                       dt_base=None, mat='till_mat', dt = 'dt', name='', scatter=True, \
                       term_sep = [('originalSecurityTerm', '2-Year'), \
                                   ('originalSecurityTerm', '5-Year'), \
                                   ('originalSecurityTerm', '10-Year'), \
                                   ('type','Bill')]):
    date_format = mdates.DateFormatter('%b-%Y')
    df = df.set_index([dt])
    legend_loc = (0.5, -0.23)
    col_num = min(len(dts_plot), 2)
    row_num = max((int(np.ceil(len(dts_plot)/col_num))), 1)
    fig, axs = plt.subplots(row_num, col_num, figsize=(15, 10))
    if not isinstance(axs, np.ndarray):
        axs = np.array([[axs]])
    elif axs.ndim==1:
        if len(axs) == 2:
            axs = axs[np.newaxis, :]
        else:
            axs = axs[:, np.newaxis]
    for i,d in enumerate(dts_plot):
        r = int(i/col_num)
        c = i % col_num
        for y_i in y:
            try:
                if scatter:
                    axs[r,c].scatter(data=df.loc[ix[d], :], x=mat, y=y_i, label=y_i + ' All')
                    for (field, val) in term_sep:
                        axs[r,c].scatter(data=df.loc[df[field] == val, :].loc[ix[d], :], x=mat, y=y_i, label=y_i + ' {}'.format(val))
                else:
                    axs[r,c].plot(mat, y_i, data=df.loc[ix[d], :], label=y_i + ' All')
                    for (field, val) in term_sep:
                        axs[r,c].plot(mat, y_i, data=df.loc[df[field] == val, :].loc[ix[d], :], label=y_i + ' {}'.format(val))
                    if not dt_base is None:
                        axs[r,c].plot(mat, y_i, data=df.loc[ix[dt_base], :], label=y_i + 'Base')
            except KeyError:
                continue
        axs[r,c].set_title(d)
        axs[r,c].legend(loc='upper right')
    if len(name) > 0:
        fig.savefig(output / '{}.pdf'.format(name), format='pdf')
    plt.close(fig)
    display_fig(fig)
