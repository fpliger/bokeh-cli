bokeh-cli
=========

Simple bokeh command line interface prototype

Usage: bokeh-cli.py [OPTIONS]

  Bokeh Command Line Tool is a minimal client to access high level plotting
  functionality provided by Bokeh plotting library.

  Examples:

  >> python bokeh-cli.py --title "My Nice Plot" --series "High,Low,Close"
  --plot_type "circle,line" --palette Reds --source_filename
  sample_data/stocks_data.csv

  >> cat sample_data/stocks_data.csv | python bokeh-cli.py --buffer t

  >> python bokeh-cli.py --help

Options:

  --source_filename TEXT  path to the series data file (i.e.:
                          /source/to/my/data.csv
  --output TEXT           Selects the plotting output, which could either be
                          sent to an html file or a bokeh server instance.
                          Syntax convention for this option is as follows:
                          <output_type>://<type_options>
                          
                          where:
                            -
                          output_type: 'file' or 'server'
                            - 'file' type
                          options: path_to_output_file
                            - 'server' type
                          options syntax: docname[@url][@name]
                          
                          Defaults to:
                          --output file://cli_output.html
                          
                          Examples:
                          --output file://cli_output.html
                              --output
                          file:///home/someuser/bokeh_rocks/cli_output.html
                          --output server://clidemo
  --title TEXT
  --plot_type TEXT
  --x_axis_name TEXT      Name of the data serie to be used as x axis when
                          plotting. By default the first serie found on the
                          input file is taken.
  --tools TEXT
  --series TEXT           Name of the series from the source to include in the
                          plot. If not specified all source series will be
                          included.
  --palette TEXT          Colors palette to use. The following palettes are
                          available:
                          
                          Blues, BrBG, BuGn, BuPu, GnBu, Greens,
                          Greys, OrRd, Oranges, PRGn, PiYG, PuBu, PuBuGn,
                          PuOr, PuRd, Purples, RdBu, RdGy, RdPu, RdYlBu,
                          RdYlGn, Reds, Spectral, YlGn, YlGnBu, YlOrBr, YlOrRd
                          You can also provide your own custom palette by
                          specifying a list colors. I.e.:
                          
                          "#a50026,#d73027,#f
                          46d43,#fdae61,#fee08b,#ffffbf,#d9ef8b,#a6d96a,#66bd6
                          3"
  --buffer TEXT           Reads data source as String from input buffer. Usage
                          example:
                          cat stocks_data.csv | python cli.py
                          --buffer t
  --x_axis_type TEXT
  --help                  Show this message and exit.