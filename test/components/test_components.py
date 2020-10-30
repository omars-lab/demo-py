from demopy.notebook_imports import bar_chart
import logging


logging.basicConfig(level=logging.DEBUG)


def test_bar_chart(test_config):
    bar_chart({"a":1})

