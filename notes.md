# Notes

## commands

- Install packages: ``poetry add <package>``
- Run the documentation server: ``mkdocs serve``
- Compile the documentation: ``mkdocs build``
- Run a test: ``python -m pici.tests.<testname>``

## TODO

- Adapt report system to new metric implementation          DONE
- Build evaluation framework
- What about visualizations?                                DONE
- Make it easier to visualize reports (one chart per metric?)
- Harvest all the Jupyter stuff
- Integrate into dashboard app --> Streamlit?
- Implement all the indicators

- make report/metrics registries abstract
- put report/metrics decorators in "reporting" / Report obj
- make decorator return "Report" obj with:
  - df
  - labelled option
  - etc.



"""
    Decorator for methods that represent reports (collections of metrics).

    A report method must have ``communities`` parameter and return a list
    of (function, dict) tuples with @metric decorated functions and kwargs.

    Args:
        level (pici.datatypes.CommunityDataLevel): The reports's data level
            determines to which 'view' on [pici.Community][pici.Community]
            the results are appended. All metrics returned by the report
            must measure on the same CommunityDataLevel.
        returntype (pici.datatypes.MetricReturnType): Data type of values
            returned by metrics in report.

    Returns:
        report (pandas.DataFrame or dict): DataFrame or dict populated with
            all metrics' calculated values for each community in
            ``communities``.


    """