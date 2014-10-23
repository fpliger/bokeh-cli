import sys
from StringIO import StringIO

from collections import OrderedDict

import numpy as np
import pandas as pd

from bokeh.plotting import *
from bokeh.palettes import brewer
from bokeh.objects import HoverTool

import pdb

import click

palettes = u', '.join(sorted(brewer.keys()))

help = u"""Colors palette to use. The following palettes are available:

%s


You can also provide your own custom palette by specifying a list colors. I.e.:

"#a50026,#d73027,#f46d43,#fdae61,#fee08b,#ffffbf,#d9ef8b,#a6d96a,#66bd63"


""" % palettes

@click.command()
@click.option('--source_filename',
              default='stocks_data.csv',
              help='path to the series data file (i.e.: /source/to/my/data.csv')
@click.option('--output_path', default='cli.html',
    #prompt='Your name',
    help='The person to greet.'
)
@click.option('--title', default='Bokeh CLI')
@click.option('--plot_type', default='circle, line')
@click.option(
    '--x_axis_name',
    default='',
    help="Name of the data serie to be used as x axis when plotting. By "
         "default the first serie found on the input file is taken."
)
@click.option(
    '--tools',
    default='pan,wheel_zoom,box_zoom,reset,previewsave,hover',
)
@click.option(
    '--series',
    default='',
    help="Name of the series from the source to include in the plot. "
         "If not specified all source series will be included."
)
@click.option('--palette', default="RdYlGn", help=help)
@click.option(
    '--buffer',
    default='f',
    help="""Reads data source as String from input buffer. Usage example:
     cat stocks_data.csv | python cli.py --buffer t
    """
)
@click.option('--x_axis_type', default='auto')
def cli(source_filename, output_path, title, plot_type, tools, series, palette,
        x_axis_name, buffer, x_axis_type='auto'):
    """
    Bokeh Command Line Tool is a minimal client to access high level plotting
    functionality provided by Bokeh plotting library.

    Examples:

    >> python bokeh-cli.py --title "My Naice Plot" --series "High,Low,Close"
    --plot_type "circle,line" --palette Reds --source_filename stocks_data.csv

    >> cat sample_data/stocks_data.csv | python bokeh-cli.py --buffer t

    >> python bokeh-cli.py --help
    """
    if buffer != 'f':
        data = sys.stdin.read()
        source = pd.read_csv(StringIO(data))

    else:
        # setup data source
        source = pd.read_csv(source_filename)

    # define user selected plot functions
    plot_foos = parse_plot_foos(plot_type)

    # bokeh boilerplate code
    colors = brewer[palette][len(source.columns)]
    output_file(output_path, title = title)
    hold()

    if not x_axis_name:
        # if not source column was picked as x axis we take a default "range"
        #x_axis_name = source.columns[0]
        x_axis_name = 'ranged_x_axis'

        # add the new x range data to the source dataframe
        source[x_axis_name] = range(len(source[source.columns[0]]))

    if x_axis_type == 'datetime':
        # in case the x axis type is datetime that column must be converted to
        # datetime
        source[x_axis_name] = pd.to_datetime(source[x_axis_name])

    series = filter_series(series, x_axis_name, source.columns)

    # define plot options that are to be specified only on the first plot
    extra = dict(tools=tools, x_axis_type=x_axis_type, title=title)

    # generate all the plots
    for i, colname in enumerate(series):
        if colname in series:
            serie = source[colname]
            for plot_foo in plot_foos:
                plot_foo(
                    source[x_axis_name],
                    serie,
                    color=colors[i],
                    legend=colname,
                    **extra
                )

                extra = {}

    # TODO: Hover tools should only be added and configured if hover is
    #       included in the list of the tools enabled

    # add the hover toos
    hover = curplot().select(dict(type=HoverTool))

    hover.tooltips = OrderedDict([
        ('index', "$index"),
        ('(x,y)', "($x,$y)"),
    ])

    show()


def parse_plot_foos(plot_type):
    """
    Receives the plot type(s) specified by the user and build a list of
    the their related functions.

    example:

    >> parse_plot_foos('line,circle')
      [line, circle]
    """
    if ',' in plot_type:
        plot_foos = [globals()[str(pt.strip())] for pt in plot_type.split(',')]

    else:
        plot_foos = [globals()[str(plot_type)]]

    return plot_foos


def filter_series(series, x_axis_name, source_columns):
    """
    If series is empty returns source_columns excluding the column
    where column == x_axis_name.

    Otherwise returns the series.split(',')
    """
    if not series:
        return [c for c in source_columns if c != x_axis_name]

    else:
        return series.split(',')

if __name__ == '__main__':
    cli()




