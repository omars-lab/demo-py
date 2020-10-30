import collections
import io
import itertools
import json
import uuid
from typing import Any, AnyStr, Mapping, NamedTuple, Optional

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.core.display import HTML, display
from IPython.display import (JSON, SVG, Image, Javascript, Markdown, Pretty,
                             display_html, display_javascript)

# https://www.datacamp.com/community/tutorials/wordcloud-python

def debug(x):
    print(x)
    return x


highlight_css = {
    "background-color": "yellow", 
    "opacity": "0.75"
}

def construct_column_highlighting_function(column_name, css):
    '''
    highlight the maximum in a Series yellow.
    '''
    css = "; ".join([f"{k}: {v}" for k, v in css.items()])
    def inner(column_of_data):
        return [
            css if column_of_data.name == column_name else ''
            for x in np.arange(len(column_of_data))
        ]
    return inner


def highlight_columns(df, *columns, css=highlight_css):
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Building-Styles-Summary
    # Column wise ...
    if len(columns) < 1:
        return df.style

    return highlight_columns(df, *columns[:-1], css=css).apply(
        construct_column_highlighting_function(columns[-1], css),
        axis=0
    )
    

def bar_chart(values: dict, title="Chart", yaxis="y", xaxis="x", width_factor=60, height_factor=20):
    # https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image
    fig = plt.figure(figsize=(width_factor, height_factor))
    x = list(values.keys())
    bar_num = np.arange(len(x))
    y = list(values.values())
    plt.bar(bar_num, y, alpha=0.5, align='center', width=0.5)
    plt.xticks(bar_num, x)
    # plt.ylabel(yaxis)
    # plt.xlabel(xaxis)
    # plt.title(title)
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    plt.close(fig)
    # plt.show(fig)
    img = widgets.Image(
        value=image.read(),
        format='png',
        width=125*width_factor,
        height=125*height_factor
    )
    img.layout.margin = "0 0 0 0"
    return img

def button(text):
    return widgets.Checkbox(
        value=False,
        description=text,
        disabled=False
    )

def container(stuff):
    return widgets.VBox(stuff)

def to_output(content):
    """
    returns how ipython displays content by default
    """
    x = widgets.Output()
    with x:
        display(content)
    return x

def tab_with_content(content_dict):
    """
    Creates a tab with dicts where keys are tabnames and content are the content of the tab ...
    """
    tab = widgets.Tab()
    keys = list(content_dict.keys())
    tab.children = [content_dict[k] for k in keys]
    for (i,title) in enumerate(keys):
        tab.set_title(i, title)
    return tab

def set_id_for_dom_element_of_output_for_current_cell(_id):
    display(Javascript('console.log(element.get(0)); element.get(0).id = "{}";'.format(_id)))

class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, JSON):
            self.json_str = json_data.data
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid),
            raw=True
        )
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
          renderjson.set_icons('+', '-');
          renderjson.set_show_to_level("2");
          document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)
