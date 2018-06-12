import argparse

from nxtodo_cli.cmd_parser.arguments_parser.entities import ENTITIES


def without_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}


def parse(arguments):
    parser = argparse.ArgumentParser(description='nxtodo')
    subparsers_for_entity = parser.add_subparsers(dest='entity')
    subparsers_for_entity.required = True

    for entity, commands in ENTITIES.items():
        parser_entity = subparsers_for_entity.add_parser(entity)
        subparsers = parser_entity.add_subparsers(dest='command')
        subparsers.required = True
        for command, args in commands.items():
            parser_command = subparsers.add_parser(command)
            for argument in args:
                parser_command.add_argument(
                    argument['short'],
                    argument['full'],
                    **without_keys(argument, ['short', 'full'])
                )

    args = parser.parse_args(arguments)
    return args
