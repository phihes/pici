# Notes

## commands

- Install packages: ``poetry add <package>``
- Run the documentation server: ``mkdocs serve``
- Compile the documentation: ``mkdocs build``
- Run a test: ``python -m pici.tests.<testname>``

## TODO

- Refactor: move label plot methods to visualizations.py
- Add tests for label plot methods
- Make it easier to visualize reports (one chart per metric?)
- Harvest all the Jupyter stuff
- Integrate into dashboard app --> Streamlit?
- Implement all the indicators
- Adapt report system to new metric implementation          DONE
- Build evaluation framework
- What about visualizations?                                DONE
- make report/metrics registries abstract                   DONE
- put report/metrics decorators in "reporting" / Report obj DONE
- make decorator return "Report" obj with:                  DONE
  - df
  - labelled option
  - etc.
- deal with multiple labellers and conflicting labels..
  (rule right now is: use first label...)
- 


