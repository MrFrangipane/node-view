import os
import sys
import pydoc


def _module_header(module):
    return [
        '# {module_name}'.format(module_name=module.__name__)
    ]


def _class_header(class_, parent):
    return [
        '',
        '## {parent_name}.{class_name}'.format(
            parent_name=parent.__name__,
            class_name=class_.__name__
        )
    ]


def _function_header(function, parent):
    if function.__name__ == '__init__':
        return [
            '',
            '### {parent_name} Constructor'.format(
                parent_name=parent.__name__,
            )
        ]

    return [
        '',
        '### {parent_name}.{function_name}'.format(
            parent_name=parent.__name__,
            function_name=function.__name__
        )
    ]


def _function_signature(function, parent):
    args_specs = pydoc.inspect.getargspec(function)
    args_signature = pydoc.inspect.formatargspec(*args_specs)

    return [
        '```python',
        '{parent}.{function_name}{args_signature}'.format(
            parent=parent.__name__,
            function_name=function.__name__,
            args_signature=args_signature
        ),
        '```'
    ]


def _separator():
    return [
        '',
        '***',
        ''
    ]


def _is_function_or_method(object_):
    return pydoc.inspect.isfunction(object_) or pydoc.inspect.ismethod(object_)


def _format_docstring(docstring):
    output = list()
    lines = docstring.split('\n')

    arg_table_initialized = False

    for line in lines:
        if not line.startswith(':'):
            output.append(line)

        if not arg_table_initialized:
            output.append("")
            output.append("| Argument | Role |")
            output.append("| --- | --- |")

            arg_table_initialized = True

        else:

            _, arg, role = line.split(':')

            output.append("| `{arg}` | {role} |".format(
                arg=arg.replace("param ", ""),
                role=role
            ))

    return output


def genereate(module_name):
    try:
        working_dir = os.getcwd()
        if working_dir not in sys.path:
            sys.path.append(working_dir)

        module = pydoc.safeimport(module_name)

        if module is None:
            print("Module not found")

        return get_markdown(module)

    except pydoc.ErrorDuringImport:
        print("Error while trying to import %s" % module_name)


def generate_and_save(module_name, output_filepath):
    content = genereate(module_name)

    if content is None: return

    with open(output_filepath, "w+") as content_file:
        content_file.write(content)


def get_markdown(module):
    output = _module_header(module)

    doc = pydoc.inspect.getdoc(module)
    if doc is not None:
        output.append(doc)

    functions = get_functions(module)

    if functions:
        output.extend(functions)

    output.extend(get_classes(module))

    return "\n".join([str(item) for item in output])


def get_functions(item):
    output = list()

    for function_name, function in pydoc.inspect.getmembers(item, _is_function_or_method):
        if function_name.startswith("_") and function_name != '__init__': continue

        output.extend(_function_header(function, parent=item))
        output.extend(_function_signature(function, parent=item))

        docstring = pydoc.inspect.getdoc(function)
        if docstring is not None:
            output.extend(_format_docstring(docstring))

    return output


def get_classes(item):
    output = list()

    for class_name, class_ in pydoc.inspect.getmembers(item, pydoc.inspect.isclass):
        if class_name.startswith("_"): continue

        output.extend(_class_header(class_, parent=item))

        doc = pydoc.inspect.getdoc(class_)
        if doc is not None:
            output.append(doc)

        output.extend(get_functions(class_))
        output.extend(get_classes(class_))

    return output


if __name__ == '__main__':
    generate_and_save("nodeview", os.getcwd() + "/doc.md")
