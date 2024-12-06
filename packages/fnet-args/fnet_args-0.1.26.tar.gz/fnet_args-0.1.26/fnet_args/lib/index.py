import argparse
import sys
# @hint: pyyaml (channel=pypi)
import yaml

# @hint: jsonschema (channel=pypi)
from jsonschema import Draft202012Validator

# @hint: deepmerge (channel=pypi)
from deepmerge import always_merger

# @hint: rich (channel=pypi)
from rich.console import Console

console = Console()

def parse_args(argv):
    """
    Parse command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser(description="CLI utility for JSON Schema validation.", add_help=False)
    parser.add_argument("--help", action="store_true", help="Display the help menu.")
    parser.add_argument("--version", action="store_true", help="Display the version.")
    parser.add_argument("--config", type=str, help="Path to the JSON Schema file.")
    parser.add_argument("--args", nargs="*", help="Additional arguments in key=value format.")
    return vars(parser.parse_args(argv))

def apply_defaults(schema, data):
    """
    Recursively apply default values from the schema to the given data.
    """
    def set_defaults(properties, obj):
        for key, value in properties.items():
            if isinstance(value, dict) and "properties" in value:
                obj[key] = obj.get(key, {})
                set_defaults(value["properties"], obj[key])
            elif "default" in value and key not in obj:
                obj[key] = value["default"]

    if "properties" in schema:
        set_defaults(schema["properties"], data)

def display_schema_as_yaml(schema):
    """
    Display the JSON Schema as YAML with rich CLI formatting.
    """
    try:
        yaml_str = yaml.dump(schema, default_flow_style=False, sort_keys=False)
        console.print(f"[bold yellow]{yaml_str}[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error displaying schema as YAML: {e}[/bold red]")

def validate_and_enrich(data, schema, validate_func=None):
    """
    Validate and enrich arguments using a JSON Schema.
    """
    # Varsayılan değerleri uygula
    apply_defaults(schema, data)
    
    if validate_func:
        validate_func(data)
    else:
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            for error in errors:
                console.print(f"[bold red]Validation error: {error.message}[/bold red]")
            sys.exit(1)

    console.print("[bold green]Validation successful![/bold green]")
    return data

def merge_args(initial, parsed):
    """
    Merge initial arguments with parsed arguments.
    """
    if initial:
        return always_merger.merge(initial, parsed)
    return parsed

def parse_key_value_args(args):
    """
    Convert key=value formatted arguments into a dictionary.
    """
    parsed_args = {}
    for arg in args:
        try:
            key, value = arg.split("=")
            parsed_args[key] = value
        except ValueError:
            console.print(f"[bold red]Error: Invalid argument format. Expected key=value but got '{arg}'.[/bold red]")
            sys.exit(1)
    return parsed_args

def default(schema, argv=None, validate_func=None, initial=None, exit_on_error=True, package_callback=None):
    """
    Main function to process and validate CLI arguments.
    """
    argv = argv or sys.argv[1:]
    args = parse_args(argv)

    # Display help
    if args.get("help"):
        if package_callback:
            package_info = package_callback()
            console.print(f"[bold cyan]{package_info.get('name')} {package_info.get('version')}[/bold cyan]")
        display_schema_as_yaml(schema)
        sys.exit(0)

    # Display version
    if args.get("version") and package_callback:
        package_info = package_callback()
        console.print(f"[bold cyan]{package_info.get('version')}[/bold cyan]")
        sys.exit(0)

    # Parse arguments from --args
    parsed_args = parse_key_value_args(args.get("args") or [])

    # Merge arguments
    merged_args = merge_args(initial, parsed_args)

    # Enrich and validate arguments
    enriched_args = validate_and_enrich(merged_args, schema, validate_func)

    return enriched_args

# if __name__ == "__main__":
#     # Define a sample JSON Schema
#     schema = {
#         "type": "object",
#         "properties": {
#             "name": {"type": "string", "default": "Guest"},
#             "age": {"type": "integer", "minimum": 0, "default": 18},
#             "is_admin": {"type": "boolean", "default": False}
#         },
#         "required": ["name"]
#     }

#     # Define a sample package callback
#     def package_callback():
#         return {"name": "Test CLI Utility", "version": "1.0.0"}

#     # Example argv inputs for testing
#     result = default(
#         schema=schema,
#         argv=sys.argv[1:],
#         package_callback=package_callback,
#         initial={"is_admin": True}
#     )
#     print("Final Result:", result)
