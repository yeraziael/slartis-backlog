#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import jsonschema

REPO = Path(__file__).resolve().parent.parent
SCHEMAS = REPO / "SCHEMAS"
EXAMPLES = REPO / "EXAMPLES"


def load(path):
    with open(path) as f:
        return json.load(f)


def extract_payload(entry):
    if "verdict" in entry:
        return entry["verdict"]
    return entry.get("contract", {})


def validate_invalid_examples(schema, examples_path):
    errors = []
    try:
        examples = load(examples_path)
    except json.JSONDecodeError as e:
        return [f"  FAIL: {examples_path.name} is not valid JSON: {e}"]

    for i, entry in enumerate(examples):
        scenario = entry.get("scenario", f"entry-{i}")
        contract = extract_payload(entry)
        expected_rejection = entry.get("expected_rejection", "")
        expected_constraint = entry.get("expected_constraint", "")

        try:
            jsonschema.validate(contract, schema)
            passed = True
            error_msg = ""
        except jsonschema.ValidationError as e:
            passed = False
            error_msg = e.message

        if expected_rejection == "schema":
            if passed:
                errors.append(
                    f"  FAIL [{scenario}]: expected schema rejection but contract passed validation"
                )
            else:
                if expected_constraint and expected_constraint not in error_msg:
                    errors.append(
                        f"  FAIL [{scenario}]: rejected but for wrong constraint.\n"
                        f"         Expected: {expected_constraint}\n"
                        f"         Got: {error_msg}"
                    )
                else:
                    constraint_ok = f" (constraint: {expected_constraint})" if expected_constraint else ""
                    print(f"  OK [{scenario}]: correctly rejected by schema{constraint_ok}")
        elif expected_rejection == "validation":
            if not passed:
                print(f"  OK [{scenario}]: schema also catches this validation case")
            else:
                print(f"  INFO [{scenario}]: runtime-only validation (passes schema)")
        else:
            if not passed:
                print(f"  INFO [{scenario}]: schema also catches this {expected_rejection} rejection (stricter schema)")
            else:
                print(f"  OK [{scenario}]: passes schema -- rejection is runtime-level ({expected_rejection})")

    return errors


def main():
    exit_code = 0

    schemas = [
        ("trigger-contract.json", "trigger-contract-valid.json", "trigger-contract-invalid.json"),
        ("execution-contract.json", "execution-contract-valid.json", "execution-contract-invalid.json"),
        ("review-verdict.json", "review-verdict-valid.json", "review-verdict-invalid.json"),
    ]

    for schema_name, examples_valid, examples_invalid in schemas:
        schema_path = SCHEMAS / schema_name
        valid_path = EXAMPLES / examples_valid
        invalid_path = EXAMPLES / examples_invalid

        if not schema_path.exists():
            print(f"  FAIL: {schema_path} not found")
            exit_code = 1
            continue

        try:
            schema = load(schema_path)
        except json.JSONDecodeError as e:
            print(f"  FAIL: {schema_name} is not valid JSON: {e}")
            exit_code = 1
            continue

        try:
            jsonschema.Draft7Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            print(f"  FAIL: {schema_name} is not a valid Draft-07 schema: {e}")
            exit_code = 1
            continue
        print(f"  OK: {schema_name} is valid Draft-07 schema")

        if valid_path.exists():
            try:
                contracts = load(valid_path)
            except json.JSONDecodeError as e:
                print(f"  FAIL: {valid_path.name} is not valid JSON: {e}")
                exit_code = 1
                continue

            if not isinstance(contracts, list):
                contracts = [contracts]

            for entry in contracts:
                if "verdict" in entry:
                    contract = entry["verdict"]
                else:
                    contract = entry
                scenario = entry.get("scenario", valid_path.name)
                try:
                    jsonschema.validate(contract, schema)
                    print(f"  OK [{scenario}]: passes schema")
                except jsonschema.ValidationError as e:
                    print(f"  FAIL [{scenario}]: should pass schema but got: {e.message}")
                    exit_code = 1

        if invalid_path.exists():
            errors = validate_invalid_examples(schema, invalid_path)
            for err in errors:
                print(err)
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
