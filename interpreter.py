import re
import json
import sys
from pathlib import Path

def parse_dsl(file_path, variables=None, visited=None):
    workout = {
        "name": "",
        "goal": "",
        "schedule": [],
        "exercises": []
    }
    errors = []
    if variables is None:
        variables = {}
    if visited is None:
        visited = set()

    file_path = Path(file_path).resolve()
    if file_path in visited:
        errors.append(f"Recursive include detected: {file_path}")
        return None, errors
    visited.add(file_path)

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            line = line.strip()

            try:
                if not line or line.startswith("#"):
                    continue  # Skip empty or commented lines

                if line.startswith("let"):
                    match = re.match(r'let (\w+) *= *(\d+)', line)
                    if match:
                        var_name, value = match.groups()
                        variables[var_name] = int(value)
                    else:
                        raise ValueError("Invalid variable declaration")

                elif line.startswith("create workout"):
                    workout["name"] = re.findall(r'"(.*?)"', line)[0]

                elif line.startswith("set goal"):
                    workout["goal"] = re.findall(r'"(.*?)"', line)[0]

                elif line.startswith("add exercise"):
                    line = replace_vars(line, variables)
                    match = re.match(r'add exercise "(.*?)" for (\d+) sets of (\d+)', line)
                    if match:
                        name, sets, reps = match.groups()
                        workout["exercises"].append({"name": name, "sets": int(sets), "reps": int(reps)})
                    else:
                        match = re.match(r'add exercise "(.*?)" for (\d+) seconds', line)
                        if match:
                            name, duration = match.groups()
                            workout["exercises"].append({"name": name, "duration": int(duration)})
                        else:
                            raise ValueError("Invalid format for exercise")

                elif line.startswith("rest"):
                    line = replace_vars(line, variables)
                    match = re.match(r'rest (\d+) seconds', line)
                    if match:
                        seconds = int(match.group(1))
                        workout["exercises"].append({"rest": seconds})
                    else:
                        raise ValueError("Invalid format for rest command")

                elif line.startswith("repeat"):
                    days = [d.strip() for d in line.replace("repeat", "").split(",")]
                    workout["schedule"] = days

                elif line.startswith("include"):
                    included_file = re.findall(r'"(.*?)"', line)
                    if included_file:
                        inc_path = file_path.parent / included_file[0]
                        inc_workout, inc_errors = parse_dsl(inc_path, variables, visited)
                        if inc_errors:
                            errors.extend([f"In {included_file[0]}: {e}" for e in inc_errors])
                        else:
                            workout["exercises"].extend(inc_workout.get("exercises", []))

                elif line.startswith("save workout"):
                    continue  # No operation

                else:
                    raise ValueError("Unknown command")
            except Exception as e:
                errors.append(f"Line {idx+1}: {line} -> {e}")

    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except Exception as e:
        errors.append(str(e))

    return workout if not errors else None, errors

def replace_vars(line, variables):
    for var, val in variables.items():
        line = re.sub(rf'\b{var}\b', str(val), line)
    return line

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <dsl_script_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    workout, errors = parse_dsl(file_path)

    if errors:
        print("Errors encountered while parsing DSL script:")
        for error in errors:
            print(" -", error)
    else:
        print("Parsed Workout:")
        print(json.dumps(workout, indent=2))