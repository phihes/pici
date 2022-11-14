# Notes

## commands

- Install packages: ``poetry add <package>``
- Run the documentation server: ``mkdocs serve``
- Compile the documentation: ``mkdocs build``
- Run a test: ``python -m pici.tests.<testname>``

## notes on pipelines

- non-final steps may be ignored by setting them to string 'passthrough' in params (https://stackoverflow.com/questions/19262621/is-it-possible-to-toggle-a-certain-step-in-sklearn-pipeline)
- The steps to be performed can be selected by index, e.g.: ``_pipe[:-1].fit_transform(X)`` performs all but the last step (https://stackoverflow.com/questions/70173306/how-can-i-transform-with-scikit-learn-pipeline-when-the-last-estimator-is-not-a)

## Tasks

### Doing

- [ ] Pre-processing for text-based indicators --> utils von anna + meine
- [ ] Create buttons for "feedback" --> color
- [ ] Implement all the indicators


### To do

- [ ] Indicator views:
  - initial post,
  - only comments,
  - all posts (incl. initial post)
- [ ] Labelling: drop duplicates (w/o labeller criterion) --> methods: keep first, "sum" heuristic, keep with highest IRA
- [ ] Utility functions for views "initial contibution", "feedback" (+ whole thread)
- [ ] Make it easier to visualize reports (one chart per metric?)
- [ ] deal with multiple labellers and conflicting labels.. (rule right now is: use first label...)

#### Issues

- [ ] fix: indicators "xxx per day" produce inf values --> likely due to quantization of dates & diff=0

#### Testing & documentation

- [ ] Document "pre-processing-enriched" dataframes 
- [ ] Add tests for label plot methods
- [ ] Document data structure

#### Examples

- [ ] Reporting: Generate metrics, generate reports, add rep.
- [ ] Labelling
- [ ] Using the machine learning pipeline
- [ ] Tuning metrics' hyperparameters using the ML pipeline
- [ ] Adding a new forum representation (new network model, e.g., network based on links where two contributors are connected who contributed after each other "answering-network")
- [ ] Loading a Community from Excel
- [ ] Adding new communities

#### Refactoring

- [ ] move label plot methods to visualizations.py

#### Optimization

- [ ] repair pickling to allow n_jobs > 1 in sklearn FeatureUnion (related to registries!?)
- [ ] Add n_jobs parameter globally and to pipelines.py allow parallelization of FeatureUnion
- [ ] optimize graph algorithms https://github.com/gboeing/osmnx/issues/710
- [ ] Use pandas.query for filtering

#### New features

- [ ] Integrate into dashboard app --> Streamlit?


### Done

- [x] Repository: Set up licence
- [x] Should all thread-indicators be calculated at the time of the last contribution to the thread??? --> yes --> this also means re-calculating the network for every unique date of initial post --> quantize time slots... e.g., calc network etc. per week (implemented via 'rounded_dates' preprocessor --> provides 'quantization', resolution can be pipeline parameter)
- [x] Repair community metric (datalevel=table..)
- [x] Add visualizations overview to documentation
- [x] Refactor: Turn metrics & reports into sklearn transformers & featureunions to be able to use pipelines, hyperparameter optimization etc.
- [x] Adapt report system to new metric implementation
- [x] Build evaluation framework
- [x] What about visualizations?
- [x] make report/metrics registries abstract
- [x] put report/metrics decorators in "reporting" / Report obj
- [x] make decorator return "Report" obj with: df, labelled option etc.
- [x] Basic get started example: load toolbox, access tools     DONE
- [x] Example: Adding new metrics



