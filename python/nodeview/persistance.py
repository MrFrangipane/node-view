import os
import yaml
from collections import OrderedDict


def _represent_ordered_dict(dumper, ordered_dict):
    value = []

    for item_key, item_value in ordered_dict.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


# Add Representers
yaml.SafeDumper.add_representer(OrderedDict, _represent_ordered_dict)
# Ignore Aliases
yaml.SafeDumper.ignore_aliases = lambda self, data: True


# Save
def document_to_file(document, filepath):
    # Dump
    document_yaml = yaml.safe_dump(document, indent=2)
    # Add Header
    document_yaml = "---\n" + document_yaml
    # Create Folders
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    # Open
    with open(filepath, "w+") as file_document:
        # Write
        file_document.write(document_yaml)


# Load
def document_from_file(filepath):
    # Open
    with open(filepath) as file_document:
        # Read
        document_yaml = file_document.read()

    # Return
    return yaml.load(document_yaml)
