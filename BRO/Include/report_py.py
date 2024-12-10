import base64
import io
import pathlib

import matplotlib.pyplot as plt

def html_header():
    return """
<!doctype html>
<html>
<head>
<title>FM payload satellite Checkout</title>
<style>
body {
    font-family: arial;
    font-size: 10pt;
}
td, th {
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 5px;
    padding-right: 5px;
    border: 1px solid black;
    word-wrap: break-word;
}
table {
    border: none;
    border-collapse: collapse;
    width: 990px;
}
table.equalwidth {
    table-layout: fixed;
}
@media screen {
    div.footer {
        display: none;
    }
}
@media print {
    .pagebreak {
        page-break-before: always;
    }
    div.footer {
        position: fixed;
        bottom: 0;
    }
}
</style>
</head>
<body>

<div class="footer">FM payload satelliet Checkout</div>
"""


def html_footer():
    return """
</body>
</html>
"""

def html_page_break():
    return"""
<div class="pagebreak"><div>
"""

def fig_to_html(fig):
    f = io.BytesIO()
    fig.savefig(f, format="png", dpi=90)
    plt.close()
    f.seek(0)
    data = f.read()
    return png_to_html(data=data)

def png_to_html(filename=None, data=None, width=None):
    if filename is not None:
        with open(filename, "rb") as fh:
            data = fh.read()

    assert data is not None, "No filename or data argument"

    args = ""
    if width is not None:
        args += f' width="{width}"'
    return f'<img src="data:image/png;base64, {base64.b64encode(data).decode()}"{args} />'

def dataframe_to_html(df, **kwargs):
    kwargs["classes"] = kwargs.get("classes", "equalwidth")
    kwargs["justify"] = kwargs.get("justify", "center")
    return df.to_html(**kwargs)

def find_matching_file_in_script_directory(pattern):
    here = pathlib.Path(__file__).parent
    paths = list(sorted(here.glob(pattern)))
    if len(paths) == 0:
        return None
    else:
        return paths[-1]

def style_pass_fail(df_style):
    return (
        df_style
        .map(lambda X: "background-color: #ff0000" if X=="Fail" else "background-color: #009900", subset=["Pass/Fail"])
        #.applymap(lambda X: "background-color: #ff0000" if X=="Fail" else "background-color: #009900", subset=["Pass/Fail"])
        #df.style.map(color_negative, color="red", subset=["A", "B"])
    )
