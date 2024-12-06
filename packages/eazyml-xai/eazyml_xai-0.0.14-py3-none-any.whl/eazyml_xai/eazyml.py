import re

import numpy as np
from . import transparency_api as tr_api
from .xai import exai
import traceback

def ez_explain(mode, outcome, train_file_path,
                      test_file_path, model, options={}):
    """EazyML Explanation API. 
        Accepts a JSON request which should have "train_file_path",
        "test_file_path", "mode", "outcome" and "model_name" as keys.
        train_file_path: Train file on which the the model build.
        test_file_path: Test file on which you want the prediction.
        record_number: The record whose prediction needs to be explained.
        mode: "Classification / Regression"
        outcome: Outcome column which you want to predict.
        model_name: Model which you use for the prediction.
    
    Returns
    -------
    [On success]
        Returns a JSON response with the keys "success" which tells the user
        if the API was successful in fetching the explanation
        "message" to convey additional information and "explanations" which is
        a python dictionary
        containing information about the explanation string, local importance
        dataframe.
    [On Failure]
        Only success and message is returned.
    """
    try:
        data_source = "system"
        if ("data_source" in options and options[
            "data_source"] == "parquet"):
            data_source = "parquet"
        train_data, _ = exai.get_df(train_file_path, data_source=data_source) 
        test_data, _ = exai.get_df(test_file_path, data_source=data_source)
        if outcome not in train_data.columns:
            return {
                    "success": False,
                    "message": "Outcome is not present in training data columns"
                    }
        if mode not in ['classification', 'regression']:
            return {
                    "success": False,
                    "message": "Please provide valid mode.('classification'/'regression')"
                    }
        if not isinstance(options, dict):
            return {
                    "success": False,
                    "message": tr_api.VALID_DATATYPE_DICT.replace(
                        "this", "options"),
                    }
        #Check for valid keys in the options dict
        is_list = lambda x: type(x) == list
        is_string = lambda x: isinstance(x, str)
        if (
            not is_string(mode)
            or not is_string(outcome)
            or not is_string(train_file_path)
            or not is_string(test_file_path)
        ):
            return {
                        "success": False,
                        "message": tr_api.ALL_STR_PARAM
                    }
        if "scaler" in options:
            scaler = options["scaler"]
        else:
            scaler = None
        for key in options:
            if key not in tr_api.EZ_EXPLAIN_OPTIONS_KEYS_LIST:
                return {"success": False, "message": tr_api.INVALID_KEY % (key)}

        if "record_number" in options and options["record_number"]:
            record_number = options["record_number"]

            if is_string(record_number):
                record_number = record_number.split(',')
            if is_list(record_number):
                rec_n = exai.get_records_list(record_number)
                if rec_n != -1:
                    record_number = rec_n
                else:
                    return {"success": False,
                            "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}

            if not is_list(record_number) and not is_string(
                record_number) and not isinstance(record_number, int):
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif is_list(record_number) and not all([(is_string(
                x) and x.isdigit()) or isinstance(x, int) for x in record_number]):
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif is_string(record_number) and not record_number.isdigit():
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif isinstance(record_number, int) and record_number < 0:
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif is_list(record_number) and any([isinstance(
                x, int) and x < 0 for x in record_number]):
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            if is_list(record_number):
                record_number = record_number
            elif isinstance(record_number, int):            
                record_number = [str(record_number)]
            else:
                record_number = [record_number]
            test_data_rows_count = test_data.shape[0]
            for rec_number in record_number:
                if int(rec_number) > test_data_rows_count:
                    return {
                            "success": False,
                            "message": "'record_number' in the 'options' parameter has values more than number of rows in the prediction dataset."
                            }
        else:
            record_number = [1]
        
        body = dict(
                train_data = train_data,
                test_data = test_data,
                outcome = outcome,
                criterion = mode,
                scaler = scaler,
                model = model,
                record_numbers = record_number
            )
        results = exai.get_explainable_ai(body)
        if type(results) != list:
            return {
                        "success": False,
                        "message": tr_api.EXPLANATION_FAILURE
                    }
        return {
                    "success": True,
                    "message": tr_api.EXPLANATION_SUCCESS,
                    "explanations": results,
                }

    except Exception as e:
        print (traceback.print_exc())
        return {"success": False, "message": tr_api.INTERNAL_SERVER_ERROR}