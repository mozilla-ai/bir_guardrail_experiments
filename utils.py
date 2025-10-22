from any_guardrail import AnyGuardrail, GuardrailName
from any_guardrail.base import Guardrail, GuardrailOutput
from collections import defaultdict
from datetime import datetime
import json
import pandas as pd

def execute_single_input_experiment(guardrail: Guardrail, 
                                    guardrail_name: str, 
                                    benchmark: pd.DataFrame, 
                                    benchmark_name: str, 
                                    target_columns: list[str]) -> dict[str, list[GuardrailOutput]]:
    """Executes a single-input experiment using the provided guardrail on the specified benchmark dataset.

    Args:
        guardrail (Guardrail): The guardrail to be tested.
        guardrail_name (str): The name of the guardrail.
        benchmark (pd.DataFrame): The benchmark dataset containing the target columns.
        benchmark_name (str): The name of the benchmark dataset.
        target_columns (list[str]): List of column names in the benchmark dataset to be tested.
    Returns:
        dict[str, list[GuardrailOutput]]: A dictionary mapping test names to lists of GuardrailOutput results.
    """

    collected_results = defaultdict(list)
    for target_column in target_columns:
        column = benchmark[target_column].values
        test_name = guardrail_name + "_" + target_column + "_" + benchmark_name
        start = datetime.now()
        for entry in column:
            result = guardrail.validate(entry)
            collected_results[test_name].append(result.model_dump_json())
        end = datetime.now()
        print((end-start).total_seconds())
    
    with open("data/{}_results.json".format(test_name), "w") as f:
        json.dump(collected_results, f, indent=4)
    
    return collected_results

def execute_dual_input_experiment(guardrail: Guardrail, 
                                  guardrail_name: str, 
                                  benchmark: pd.DataFrame, 
                                  benchmark_name: str, 
                                  target_columns: list[list[str]],
                                  ground_truth: str,
                                  input_key: str | None = None,
                                  output_key: str | None = None) -> dict[str, list[GuardrailOutput]]:
    """Executes a dual-input experiment using the provided guardrail on the specified benchmark dataset.
    
    Args:
        guardrail (Guardrail): The guardrail to be tested.
        guardrail_name (str): The name of the guardrail.
        benchmark (pd.DataFrame): The benchmark dataset containing the target columns.
        benchmark_name (str): The name of the benchmark dataset.
        target_columns (list[list[str]]): List of pairs of column names in the benchmark dataset to be compared.
        ground_truth (str): The name of the column containing ground truth labels.
        input_keys (list[str] | None, optional): List of input keys for the guardrail. Defaults to None.
        output_keys (str | None, optional): Output key for the guardrail. Defaults to None.
    Returns:
        dict[str, list[GuardrailOutput]]: A dictionary mapping test names to lists of GuardrailOutput results.
    """
    collected_results = defaultdict(list)
    ground_truth_column = benchmark[ground_truth].values
    for pair in target_columns:
        if len(pair) != 2:
            msg = "Must have two, and only two, columns to compare."
            raise ValueError(msg)
        column1 = benchmark[pair[0]].values
        column2 = benchmark[pair[1]].values
        test_name = guardrail_name + "_" + pair[0] + "_" + pair[1] + "_" + benchmark_name
        start = datetime.now()
        for entry1, entry2, gt_label in zip(column1, column2, ground_truth_column):
            if input_key and output_key:
                inputs = [{input_key: entry1}]
                output = {output_key: entry2}
                collected_results[test_name].append(guardrail.validate(inputs, output).model_dump_json())
            else:
                collected_results[test_name].append(guardrail.validate(entry1, entry2).model_dump_json())
        end = datetime.now()
        print((end-start).total_seconds())

    with open("data/{}_results.json".format(test_name), "w") as f:
        json.dump(collected_results, f, indent=4)

    return collected_results