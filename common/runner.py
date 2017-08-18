#encoding:utf-8

import datetime
import requests

from common import exception, response
from common.client import HttpSession
from common.context import Context

from models import Result
from dbutil import MysqldbHelper

result = Result()
db = MysqldbHelper()

class Runner(object):

    def __init__(self, http_client_session=None):
        self.http_client_session = http_client_session
        self.context = Context()

    def init_config(self, config_dict, level):
        """ create/update context variables binds
        @param (dict) config_dict
            {
                "name": "description content",
                "requires": ["random", "hashlib"],
                "function_binds": {
                    "gen_random_string": \
                        "lambda str_len: ''.join(random.choice(string.ascii_letters + \
                        string.digits) for _ in range(str_len))",
                    "gen_md5": \
                        "lambda *str_args: hashlib.md5(''.join(str_args).\
                        encode('utf-8')).hexdigest()"
                },
                "import_module_functions": ["test.data.custom_functions"],
                "variable_binds": [
                    {"TOKEN": "debugtalk"},
                    {"random": "${gen_random_string(5)}"},
                ]
            }
        @param (str) context level, testcase or testset
        """
        self.context.init_context(level)

        requires = config_dict.get('requires', [])
        self.context.import_requires(requires)

        function_binds = config_dict.get('function_binds', {})
        self.context.bind_functions(function_binds, level)

        module_functions = config_dict.get('import_module_functions', [])
        self.context.import_module_functions(module_functions, level)

        variable_binds = config_dict.get('variable_binds', [])
        self.context.bind_variables(variable_binds, level)

        request_config = config_dict.get('request', {})
        if level == "testset":
            base_url = request_config.pop("base_url", None)
            self.http_client_session = self.http_client_session or HttpSession(base_url)
        else:
            # testcase
            self.http_client_session = self.http_client_session or requests.Session()
        self.context.register_request(request_config, level)

    def run_test(self, testcase, runNum):
        """ run single testcase.
        @param (dict) testcase
            {
                "name": "testcase description",
                "times": 3,
                "requires": [],  # optional, override
                "function_binds": {}, # optional, override
                "variable_binds": {}, # optional, override
                "request": {
                    "url": "http://127.0.0.1:5000/api/users/1000",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json",
                        "authorization": "$authorization",
                        "random": "$random"
                    },
                    "body": '{"name": "user", "password": "123456"}'
                },
                "extract_binds": {}, # optional
                "validators": []     # optional
            }
        @return (tuple) test result of single testcase
            (success, diff_content_list)
        """

        self.init_config(testcase, level="testcase")
        parsed_request = self.context.get_parsed_request()

        try:
            url = parsed_request.pop('url')
            method = parsed_request.pop('method')
        except KeyError:
            raise exception.ParamsError("URL or METHOD missed!")

        #print parsed_request
        if parsed_request.get("files"):
            for key in parsed_request.get("files"):
                parsed_request.get("files")[key] = [None, parsed_request.get("files")[key]]
        #print parsed_request

        run_times = int(testcase.get("times", 1))
        extract_binds = testcase.get("extract_binds", {})
        validators = testcase.get("validators", [])

        for _ in range(run_times):
            resp = self.http_client_session.request(url=url, method=method, **parsed_request)
            resp_obj = response.ResponseObject(resp)

            extracted_variables_mapping_list = resp_obj.extract_response(extract_binds)
            self.context.bind_variables(extracted_variables_mapping_list, level="testset")

            diff_content_list = resp_obj.validate(
                validators, self.context.get_testcase_variables_mapping())

            testResult = 0
            # mockid = mockid + 1
            diff = str(diff_content_list)
            casename = testcase.get("name")
            if not diff_content_list:
                diff = {""}
                testResult = 1

            sql = "insert into auto_result(mockid,name,testresult,reqmethod,rspcode,reqpath,reqhead,reqbody,rsphead,rspbody,diff,ts) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (
                runNum, casename, testResult, resp.request.method, resp.status_code, resp.request.url, resp.request.headers,
                resp.request.body,
                resp.headers, resp.content, diff, datetime.datetime.now())

            count = db.updateByParam(sql, params)
            print count

        return resp_obj.success, diff_content_list

    def run_testset(self, testset):
        """ run single testset, including one or several testcases.
        @param (dict) testset
            {
                "name": "testset description",
                "config": {
                    "name": "testset description",
                    "requires": [],
                    "function_binds": {},
                    "variable_binds": [],
                    "request": {}
                },
                "testcases": [
                    {
                        "name": "testcase description",
                        "variable_binds": {}, # optional, override
                        "request": {},
                        "extract_binds": {},  # optional
                        "validators": {}      # optional
                    },
                    testcase12
                ]
            }
        @return (list) test results of testcases
            [
                (success, diff_content),    # testcase1
                (success, diff_content)     # testcase2
            ]
        """
        results = []

        config_dict = testset.get("config", {})
        self.init_config(config_dict, level="testset")
        testcases = testset.get("testcases", [])
        for testcase in testcases:
            result = self.run_test(testcase)
            results.append(result)

        return results

    def run_testsets(self, testsets):
        """ run testsets, including one or several testsets.
        @param testsets
            [
                testset1,
                testset2,
            ]
        @return (list) test results of testsets
            [
                [   # testset1
                    (success, diff_content),    # testcase11
                    (success, diff_content)     # testcase12
                ],
                [   # testset2
                    (success, diff_content),    # testcase21
                    (success, diff_content)     # testcase22
                ]
            ]
        """
        return [self.run_testset(testset) for testset in testsets]
