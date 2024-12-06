import re
import numpy as np
import pandas as pd
from .exai_main import get_random_train_data
from .exai_main import get_pdf_data
from .exai_main import get_exai_explanations
import traceback
from itertools import islice

from concurrent.futures import ProcessPoolExecutor as Pool
from .. import global_var as g

try:
    from werkzeug import secure_filename
except:
    from werkzeug.utils import secure_filename


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def get_records_list(record_number):
    final_rec = []
    if any(["-" in str(x) for x in record_number]):
        for x in record_number:
            if "-" not in x and len(x.strip().split(" ")) == 1:
                final_rec.append(int(x))
            elif len(str(x).strip().split(" ")) == 1:
                l = [range(int(x.split("-")[0]), int(x.split("-")[1])+1)]
                final_rec.extend(l[0])
            else:
                return -1
        return [i for n, i in enumerate(final_rec) if i not in final_rec[:n]]
    elif any([len(str(x).strip().split(" ")) > 1 for x in record_number]):
        return -1
    else:
        return [int(i) for i in record_number]


def find_delimiter(lst):
    maximum = [None, -1]
    for possible_delimiter in g.ALLOWED_DELIMITERS:
        last_line_size = len(lst[0].split(possible_delimiter))
        for row in lst[1:]:
            if len(row.split(possible_delimiter)) != last_line_size:
                break
            else:
                last_line_size = len(row.split(possible_delimiter))
        if last_line_size > maximum[1] and last_line_size > 1:
            maximum = (possible_delimiter, last_line_size)
    return maximum


def get_df(uploaded_file, data_source="system", is_api=False,
           ip_fname=None, full_path=False):
    df = None
    if  data_source == "system":
        if ip_fname is not None:
            fname = ip_fname
        else:
            fname = secure_filename(uploaded_file)
        ext = get_extension(fname)
        tmp_path = uploaded_file
        try:
            if ext == "csv":
                df = pd.read_csv(tmp_path, na_values=[
                    'n/a', 'na', 'nan', 'null'])
            elif ext == "xlsx" or ext == "xls":
                df = pd.read_excel(tmp_path, na_values=[
                    'n/a', 'na', 'nan', 'null'])
            elif ext == "tsv":
                df = pd.read_table(tmp_path, na_values=[
                    'n/a', 'na', 'nan', 'null'])
            elif ext == "parquet":
                df = pd.read_parquet(tmp_path)
            elif ext == "txt":
                with open(tmp_path) as myfile:
                    head = list(islice(myfile, g.DELIMITER_ROWS_COUNT))
                delimiter = find_delimiter(head)[0]
                if delimiter in g.ALLOWED_DELIMITERS:
                    df = pd.read_csv(tmp_path, sep=delimiter,na_values=[
                        'n/a', 'na', 'nan', 'null'])
                else:
                    print ('Error in loading txt file. Delimiter not found.')
                    return None, None
            elif is_api:
                return df, tmp_path
        except Exception as e:
            print("Exception in loading csv: ", e)
            print(traceback.print_exc())
            return None, None
    else:
        try:
            df = pd.read_parquet(uploaded_file)
            tmp_path = uploaded_file
            if is_api:
                if df.shape[0] >= 1000 or df.shape[1] >= 100:
                    df.to_csv(tmp_path, index=False)
                return df, tmp_path
        except Exception as e:
            print("Exception in reading parquet file: ", e)
            print(traceback.print_exc())
            return None, None
    df = df.replace(r'^\s*$', np.nan, regex=True)
    columns = list(df.columns)
    try:
        columns_stripped = [re.sub('\s+', ' ', str(col)).strip().replace(
            '()','(.)') for col in columns]
    except Exception as e:
        print ("Exception in converting column text to str", e)
        columns_stripped = [re.sub('\s+', ' ', str(col.encode(
            'ascii', 'ignore').decode('ascii'))).strip().replace(
            '()','(.)') for col in columns]
    sql_escape_sequences = g.SQL_ESCAPE_SEQUENCES 
    for i, elem in enumerate(columns_stripped):
        for esc_seq in sql_escape_sequences:
            if esc_seq in elem:
                columns_stripped[i] = elem.replace(esc_seq, '')
    df.columns = columns_stripped
    if any(("[" in x or "]" in x or "<" in x for x in columns_stripped)):
        return g.COLUMN_NAMES_INCOMPATIBLE, None
    return df, None

def get_explanations_all_records(
    train_data, outcome,
    mode, test_point,
    test_point_pred,
    raw_test_point,
    extra_info
    ): 
    t_data = None
    if not g.ONLY_PERTURBED_POINTS or g.LIME_FOR_CLASSIF or g.LIME_FOR_REGR:
        t_data = train_data
    results = []
    for item in range(len(extra_info['record_numbers'])):
        extra_info[g.TEST_PT_PRED] = raw_test_point[outcome].iloc[item]
        raw_test_point_rec = raw_test_point.iloc[item]
        res = get_exai_explanations(
            t_data, outcome, mode,
            test_point[item].reshape(1, -1), raw_test_point_rec,
            extra_info.copy())
        results.append(res)
    response = []
    for item, rec, result in zip(range(len(extra_info['record_numbers'])),
        extra_info['record_numbers'], results):
        res = dict()
        res["record_numbers"] = rec
        res["prediction"] = result[2]
        res["explanation"] = result[1]
        res["explainability_score"] = result[3]
        res["local_importance"] = result[0]
        if "Confidence Score" in raw_test_point.columns:
            res["confidence_score"] = raw_test_point[
                "Confidence Score"].iloc[item]
        response.append(res)
    return response


def get_explainable_ai(input_object):
    try:
        # extracting parameters
        train_data = input_object['train_data']
        test_data_processed = input_object['test_data']
        outcome = input_object['outcome']
        ind = [i-1 for i in input_object['record_numbers']]
        raw_test_point_processed = test_data_processed.iloc[ind]
        tr_cols = train_data.columns.values.tolist()
        if outcome in tr_cols:
            tr_cols.remove(outcome)
        test_point = raw_test_point_processed[tr_cols].values.astype('float64')
        test_point = test_point.reshape(len(input_object['record_numbers']),-1)
        input_object[g.RULE_LIME] = {'columns': tr_cols}
        input_object[g.FEATURES_SELECTED] = tr_cols
        criterion = input_object['criterion']
        is_classification = (criterion == 'classification')
        if is_classification :
             input_object['pred_proba'] = True
        else:
             input_object['pred_proba'] = False
        test_point_pred = test_data_processed.iloc[ind]             
        raw_test_point = test_data_processed 
        try:
            response = get_explanation_bulk(
                                            train_data, outcome, criterion,
                                            test_point, test_point_pred,
                                            raw_test_point,
                                            input_object)
            return response
        except ValueError as e:
            traceback.print_exc()
            return str(e)
        except Exception as e:
            traceback.print_exc()
            return 'Internal Server Error'
    except Exception as e:
        traceback.print_exc()
        return 'Internal Server Error'


def get_explanation_bulk(
               train_data, outcome, mode,
               test_point,
               test_point_pred,
               raw_test_point,
               extra_info):

    # g = DotDict(extra_info)
    tunable_params_dict = {}
    tunable_params_dict['training_data_proportion'] = g.MIN_R1_SAMPLED_TRAINING_DATA_PROPORTION
    np.random.seed(g.DEBUG_SEED_PERTURBATION)
    model_data = {}
    if g.SCALER in extra_info:
        model_data[g.SCALER] = extra_info[g.SCALER]
    else:
        model_data[g.SCALER] = None
        extra_info[g.SCALER] = None

    min_model_data = get_random_train_data(train_data, outcome, extra_info)
    model_data[g.RANDOM_TRAIN_DATA] = min_model_data
    extra_info['model_data'] = model_data
    if "N1_data" not in extra_info:
        if g.MULTINOMIAL_HISTOGRAM or g.EXAI_ENHANCE_PERFORMANCE or\
            (mode == "classification" and not g.LIME_FOR_CLASSIF) or\
            (mode == "regression" and not g.LIME_FOR_REGR):
            get_pdf_data(mode, train_data, outcome,
                         tunable_params_dict,
                         model_data,
                         extra_info
                        )

    return get_explanations_all_records(
                                        train_data, outcome,
                                        mode, test_point,
                                        test_point_pred,
                                        raw_test_point,
                                        extra_info)
