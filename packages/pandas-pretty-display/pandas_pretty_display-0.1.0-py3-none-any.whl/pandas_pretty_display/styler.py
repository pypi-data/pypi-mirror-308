"""
Module for styling pandas DataFrames with alternating colors and improved formatting.
"""

from IPython.core.display import display, HTML

def style_dataframe():
    """
    Apply a custom style to pandas DataFrames with alternating gold and light blue colors.
    
    This function applies the following styling:
    - Alternating gold and light blue row colors
    - Black text in table cells
    - Red text in table headers
    - Black borders around cells
    - 18px font size
    - Full-width container
    - Scrollable output up to 1000px height
    
    Returns:
        None
    """
    display(HTML("<style>.container { width:100% !important; }</style>"))
    display(HTML("<style>div.output_scroll { height: 1000px; }</style>"))
    display(HTML("<style>.output {color: #7df9ff;}</style>"))
    display(HTML("<style>table.dataframe, .dataframe td {border: 1px solid black; color:black;font-size:18px;}</style>"))
    display(HTML("<style>table.dataframe tr:nth-child(even) {background-color: rgb(253,253,201);}</style>"))
    display(HTML("<style>table.dataframe tr:nth-child(odd) {background-color: rgb(162,255,255);}</style>"))
    display(HTML("<style>.dataframe th {background-color: rgb(253,253,201); border: 1px solid black;color:red;}</style>"))
