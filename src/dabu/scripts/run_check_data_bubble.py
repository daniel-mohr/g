"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-15 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import jsonschema
import os.path
import warnings

from .check_arg_file import check_arg_file


def run_check_data_bubble(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-15 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for path in args.directory:  # for every given directory
        check_arg_file(os.path.join(path, args.dabu_instance_file[0]))
        check_arg_file(os.path.join(path, args.dabu_schema_file[0]))
        with open(os.path.join(path, args.dabu_instance_file[0]),
                  mode='r') as fd:
            instance = json.load(fd)
        with open(os.path.join(path, args.dabu_schema_file[0]),
                  mode='r') as fd:
            schema = json.load(fd)
        # check schema
        # the schema test of jsonschema is insufficient
        if not u"$schema" in schema:
            warnings.warn(
                'No "$schema" keyword in the given schema found. '
                'It is recommended to use this keyword to specifiy the used '
                'JSON version.')
        else:
            if schema[u"$schema"] not in jsonschema.validators.meta_schemas:
                raise NotImplementedError(
                    'Schema "' + schema[u"$schema"] +
                    '" not found in implemented validators of jsonschema.')
        #jsonschema.validate(instance, schema)
        v = jsonschema.Draft4Validator(schema)
        try:
            jsonschema.Draft4Validator.check_schema(schema)
        except jsonschema.exceptions.SchemaError as msg:
            print(msg)
            exit()
        for err in sorted(v.iter_errors(instance), key=str):
            if len(err.path) > 0:
                print('%s in:\n    %s' % (err.message, ' -> '.join(map(str, err.path))))
            else:
                print(err.message)
