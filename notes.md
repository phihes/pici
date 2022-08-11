# Notes

## commands

- Install packages: ``poetry add <package>``
- Run the documentation server: ``mkdocs serve``
- Compile the documentation: ``mkdocs build``
- Run a test: ``python -m pici.tests.<testname>``

## TODO

- [ ] Refactor: move label plot methods to visualizations.py
- [ ] Add tests for label plot methods
- [ ] Make it easier to visualize reports (one chart per metric?)
- [ ] Harvest all the Jupyter stuff
- [ ] Integrate into dashboard app --> Streamlit?
- [ ]Implement all the indicators
- [ ] deal with multiple labellers and conflicting labels.. (rule right now is: use first label...)
- [x] Repair community metric (datalevel=table..)
- [x] Add visualizations overview to documentation
- [x] Refactor: Turn metrics & reports into sklearn transformers & featureunions to be able to use pipelines, hyperparameter optimization etc.
- [x] Adapt report system to new metric implementation
- [x] Build evaluation framework
- [x] What about visualizations?
- [x] make report/metrics registries abstract
- [x] put report/metrics decorators in "reporting" / Report obj
- [x] make decorator return "Report" obj with: df, labelled option etc.


## Examples

- [x] Basic get started example: load toolbox, access tools     DONE
- [ ] Reporting: Generate metrics, generate reports, add rep.
- [ ] Adding new metrics
- [ ] Using the machine learning pipeline
- [ ] Tuning metrics' hyperparameters using the ML pipeline

### Advanced:
- [ ] Adding new communities