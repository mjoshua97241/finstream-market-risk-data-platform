import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import os
    import pandas as pd
    from pathlib import Path

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Load raw dataset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    run validation rules
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    collect validation errors
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    split dataset > valid | invalid rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    return results
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
