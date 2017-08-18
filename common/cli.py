#encoding:utf-8
import argparse
import logging
import os

import PyUnitReport

from common.task import create_task


def main():
    """ parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(
        description='interface test framework')
    parser.add_argument(
        'testset_paths', nargs='*',
        help="testset file path")
    parser.add_argument(
        '--log-level', default='DEBUG',
        help="Specify logging level, default is INFO.")
    parser.add_argument(
        '--report-name',
        help="Specify report name, default is generated time.")

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    report_name = args.report_name
    if report_name and len(args.testset_paths) > 1:
        report_name = None
        logging.warning("More than one testset paths specified, \
                        report name is ignored, use generated time instead.")

    args.testset_paths = ["tests\\data\\demo_resource.yml","tests\\data\\demo_department.yml"]

    for testset_path in args.testset_paths:

        testset_path = testset_path.strip('/')
        task_suite = create_task(testset_path)

        output_folder_name = os.path.basename(os.path.splitext(testset_path)[0])
        kwargs = {
            "output": output_folder_name,
            "report_name": report_name,
            "failfast": False
        }
        PyUnitReport.HTMLTestRunner(**kwargs).run(task_suite)
