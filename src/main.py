import os
import src.dbt_test_coverage as dbt_test_coverage
import argparse
from pkg_resources import get_distribution
import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recursive",
        help="If you want to search sub directories for yml-files (default: True)",
   )
    parser.add_argument(
        "--pr",
        help="Folder with PR models",
   		required=True
    ) 
    parser.add_argument(
        "--master",
        help="Folder with Master branch models",
        required=True
    ) 
    parser.add_argument(
        "--doc_thresh",
        help="Percentage to use a threshold to fail for total documentation coverage (default: 0)",
        default=0,
        type=float
    ) 
    parser.add_argument(
        "--test_thresh",
        help="Percentage to use a threshold to fail for total model test test-coverage (default: 0)",
        default=0,
        type=float
    ) 

    args = parser.parse_args()

    if args.recursive:
        recursive = args.recursive
    else:
        recursive = True

    level = logging.INFO
    logging.basicConfig(format='%(message)s',level=level)

    logging.debug("")
    logging.debug("Running dbt-test-coverage " + get_distribution("dbt-test-coverage").version)
    logging.debug("")

    try:
        pr_model_cov     = dbt_test_coverage.test_coverage(args.pr, recursive=recursive,doc_thresh=args.doc_thresh, test_thresh=args.test_thresh)
        master_model_cov = dbt_test_coverage.test_coverage(args.master, recursive=recursive)
        model_delta = pr_model_cov[0] - master_model_cov[0]
        docs_delta  = pr_model_cov[1] - master_model_cov[1]
        tests_delta = pr_model_cov[2] - master_model_cov[2]

        if model_delta <= 0:
            return        

        logging.info("")
        logging.info(f"Models added : {model_delta}")
        logging.info(f"Docs added   : {docs_delta}")
        logging.info(f"Tests added  : {tests_delta}")
        
        if docs_delta < model_delta:
            raise Exception(f"ERROR: Expected {model_delta} new docs, but only got {docs_delta} new docs!")
        if tests_delta < model_delta:
            raise Exception(f"ERROR: Expected {model_delta} new tests, but only got {tests_delta} new tests!")

    except KeyboardInterrupt:
        logging.warning("Interupted by user")

if __name__ == "__main__":
    main()
