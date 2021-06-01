# dbt-test-coverage

Forked from:  for the iFit dbt repo.

cli tool for showing test coverage in [dbt](https://www.getdbt.com) projects.

Tested with dbt 0.15 and newer!

Install with pip:

    pip install git+https://github.com/ifit/data-dbt-test-coverage.git

## Usage
Right now this is only really used in the analytics-dbt repo. You pass in a folder for the PR, and a folder for the master branch. The code will compare how many models/tests/docs were added to ensure that new tests/docs are being created for each PR. 

Example: 

	dbt-test-coverage --pr ../analytics-dbt/models --master ../analytics-dbt-master/models --doc_thresh 90 --test_thresh 50

This will ensure that the 90 percent of models have docs, and 50% of models have tests.


## Misc usage
Go to the folder where you have your dbt schema definitions (your yml-files). To search recursive (the folder you are in and all below) type:

    dbt-test-coverage
To only search in the folder you are in:

    dbt-test-coverage --recursive=False

Output for sources will be something like:

    ...
    Source: my_source_system, Database: my_db, Schema: my_schema, Table: my_table, Model name: my_table_model_name, Tested: False
    Source: my_source_system, Database: my_db2, Schema: my_schema2, Table: my_table2, Model name: my_table_model_name2, Tested: True

    Sources: 34, Tested: 1, Coverage: 3%

Output for models will be something like:

    ...
    Model: my_dbt_model, Tested: False
    Model: my_dbt_model2, Tested: True
    
    Models: 6, Tested: 1, Coverage: 17%

## Good to know
As of now, only the yml-files are parsed. The tool will not include undocumented models in the coverage report.


## Changelog

### v0.0.1
Initial commit
