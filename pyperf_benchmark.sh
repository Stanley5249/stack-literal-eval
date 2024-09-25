rm -f resources/literal_eval.json resources/stack_literal_eval.json
python pyperf_literal_eval.py -o resources/literal_eval.json
python pyperf_stack_literal_eval.py -o resources/stack_literal_eval.json
python -m pyperf compare_to resources/literal_eval.json resources/stack_literal_eval.json --table