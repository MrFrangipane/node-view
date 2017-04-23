import os
import sys
import pydoc
import inspect


def _module_header(module_name):
    return [
        '',
        '# Module `{module_name}`'.format(module_name=module_name)
    ]


def _class_header(class_name):
    return [
        '',
        '## Class `{class_name}`'.format(class_name=class_name)
    ]


def _function_header(function_name):
    return [
        '',
        '### `{function_name}`'.format(function_name=function_name)
    ]


def _function_signature(function):
    args = inspect.getargspec(function).args

    if args[0] == "self":
        args[0] = "_self_"

    return [
        '**{function_name}**({args})'.format(
            function_name=function.__name__,
            args=", ".join(args)
        )
    ]


def _separator():
    return [
        '',
        '***',
        ''
    ]


def _is_function_or_method(object_):
    return inspect.isfunction(object_) or inspect.ismethod(object_)


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
    output = _module_header(module.__name__)

    functions = get_functions(module)

    if functions:
        output.extend(functions)
        output.extend(_separator())

    output.extend(get_classes(module))

    return "\n".join([str(item) for item in output])


def get_functions(item):
    output = list()

    for function_name, function in inspect.getmembers(item, _is_function_or_method):
        if function_name.startswith("_"): continue

        output.extend(_function_header(function_name))
        output.extend(_function_signature(function))

        doc = inspect.getdoc(function)
        if doc is not None:
            output.append(doc)

    return output


def get_classes(item):
    output = list()

    for class_name, class_ in inspect.getmembers(item, inspect.isclass):
        if class_name.startswith("_"): continue

        output.extend(_class_header(class_name))

        doc = inspect.getdoc(class_)
        if doc is not None:
            output.append(doc)

        output.extend(get_functions(class_))
        output.extend(get_classes(class_))

        output.extend(_separator())

    return output


if __name__ == '__main__':
    generate_and_save("nodeview", os.getcwd() + "/doc.md")
