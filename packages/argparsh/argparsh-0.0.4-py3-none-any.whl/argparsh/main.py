import argparse
import sys
import textwrap
import json
from abc import abstractmethod

from . import utils

commands: dict[str, "Command"] = {}


class Watcher(type):
    """Register all subclasses into the commands global dictionary by their name"""

    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) > 2:
            commands[cls.name()] = cls
        super(Watcher, cls).__init__(name, bases, clsdict)


class Command(metaclass=Watcher):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def help(cls) -> str:
        pass

    @classmethod
    def requires_subparser_arg(cls) -> bool:
        return False

    @classmethod
    def consumes_rest_args(cls) -> bool:
        return False

    @classmethod
    def extend_parser(cls, parser: argparse.ArgumentParser):
        pass

    @classmethod
    @abstractmethod
    def construct(cls, args: argparse.Namespace) -> str:
        pass

    @classmethod
    @abstractmethod
    def run(cls, parser: utils.Parser, data):
        pass

    @classmethod
    def output(cls, data) -> str:
        return utils.output(cls.name(), data)


class New(Command):
    @classmethod
    def name(cls):
        return "new"

    @classmethod
    def help(cls):
        return "Create a new parser with a name and description (see argparsh new -h)"

    @classmethod
    def extend_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument("name", help="Name of script")
        parser.add_argument(
            "-d",
            "--description",
            help="Description of program",
            action="store",
            default="",
        )
        parser.add_argument(
            "-e",
            "--epilog",
            help="Text to display after help text",
            action="store",
            default="",
        )

    @classmethod
    def construct(cls, args: argparse.Namespace) -> str:
        kwargs = {
            "prog": args.name,
            "description": args.description,
            "epilog": args.epilog,
        }
        return cls.output(kwargs)

    @classmethod
    def run(cls, parser: utils.Parser, data):
        parser.initialize(**data)


class AddArg(Command):
    @classmethod
    def name(cls):
        return "add_arg"

    @classmethod
    def help(cls):
        return textwrap.dedent(
            """
                Add an argument to the parser (separate argument aliases and parsing options with '--' ).
                This is a wrapper around ArgumentParser.add_argument. In other
                words, the following invocation:
                    argparsh add_arg [aliases]... -- [--key [value]]...
                Is effectively:
                    parser.add_argument(*[aliases], **[key/values])

                argparsh is generally smart enough to parse and massage extra
                arguments into the correct types.
                e.g.
                    argparsh add_argument -i --intval -- --type int --default 10 --choices "[10, 20, 30]"

                will become:
                    parser.add_argument("-i", "--intval", type=int, default=100, choices=[10, 20, 30])

                note: to add an argument for "-h" or "--help" one will need to
                run `argparsh -- -h ...`
                note: to add an argument to a subparser use the --subparser and
                --parser-arg flags. These flags must come before any aliases
                that are being registered. See the section on subparsers below
                for details.
            """
        )

    @classmethod
    def requires_subparser_arg(cls) -> bool:
        return True

    @classmethod
    def consumes_rest_args(cls) -> bool:
        return True

    @classmethod
    def construct(cls, args: argparse.Namespace) -> str:
        # add an argument to obj by assembling the method to call
        aliases = []
        while len(args.rest) and not args.rest[0] == "--":
            aliases.append(args.rest[0])
            args.rest.pop(0)
        meth_args = aliases

        if len(args.rest):
            args.rest.pop(0)

        meth_kwargs = utils.arglist_to_kwargs(args.rest)
        return cls.output((args.subparser, args.parser_arg, meth_args, meth_kwargs))

    @classmethod
    def run(cls, parser: utils.Parser, data):
        subparser, parser_arg, meth_args, meth_kwargs = data
        p = parser.get_parser(parser_arg, subparser)
        p.add_argument(*meth_args, **meth_kwargs)


class SubparserInit(Command):
    @classmethod
    def name(cls):
        return "subparser_init"

    @classmethod
    def help(cls):
        return textwrap.dedent(
            """
                Initialize a new subparser.
                This is a wrapper around ArgumentParser.add_subparser, all
                keyword arguments are forwarded to python.

                The exceptions are:
                    --metaname   The value provided to metaname
                                 can be used to identify this subparser in
                                 future calls to `add_arg` or `set_defaults`.
                    --parser-arg This optional argument should be the metaname
                                 of some previously created subparser. (See
                                 below)
                    --subparser  This optional argument should be the name of a
                                 command attached to a previously created
                                 subparser that we would like to create a new
                                 subparser under. (See below)

                e.g.
                parser=$({
                    # Create two subcommands `<prog> foo` and `<prog> bar`
                    argparsh subparser_init --metaname foobar --required true
                    argparsh subparser_add foo
                    argparsh subparser_add bar

                    # Attach a subcommand to `foo`, creating
                    #    <prog> foo fee
                    # -and-
                    #    <prog> foo fie
                    argparsh subparser_init --subparser foo --metaname feefie --required true
                    argparsh subparser_add fee
                    argparsh set_defaults --subparser fee --myfooarg fee
                    argparsh subparser_add fie
                    argparsh set_defaults --subparser fie --myfooarg fie

                    # Add a regular argument to foo. Note that we now need to
                    # use the metaname "foobar" so avoid attaching to the wrong
                    # parser. (By default the most recently created parser is
                    # used - in this case the most recently created parser is
                    # feefie)
                    argparsh add_arg --parser-arg foobar --subparser foo "qux"
                    argparsh set_defaults --parser-arg foobar --subparser foo --myarg foo

                    # Attach a regular argument to bar
                    argparsh add_arg --parser-arg foobar --subparser bar "baz"
                    argparsh set_defaults --parser-arg foobar --subparser bar --myarg bar

                    # possible commands supported by this parser:
                    #   <prog> foo fee <qux>
                    #   <prog> foo fie <qux>
                    #   <prog> bar <baz>
                })
            """
        )

    @classmethod
    def consumes_rest_args(cls) -> bool:
        return True

    @classmethod
    def requires_subparser_arg(cls) -> bool:
        return True

    @classmethod
    def extend_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--metaname",
            help="Optional name for argument",
            required=False,
            default=None,
        )

    @classmethod
    def construct(cls, args: argparse.Namespace) -> str:
        data = utils.arglist_to_kwargs(args.rest)
        return cls.output((args.subparser, args.parser_arg, args.metaname, data))

    @classmethod
    def run(cls, parser: utils.Parser, data):
        subparser, parser_arg, metaname, kwargs = data
        parser.add_subparser(subparser, parser_arg, metaname, **kwargs)


class SubparserAdd(Command):
    @classmethod
    def name(cls):
        return "subparser_add"

    @classmethod
    def help(cls):
        return "Add a command to a subparser. See subparser_init for details"

    @classmethod
    def consumes_rest_args(cls) -> bool:
        return True

    @classmethod
    def extend_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--metaname",
            help="Name of subparser to add to (from subparser_init)",
            required=False,
            default=None,
        )
        parser.add_argument("name", help="Name of command")

    @classmethod
    def construct(cls, args: argparse.Namespace) -> str:
        data = utils.arglist_to_kwargs(args.rest)
        return cls.output((args.name, args.metaname, data))

    @classmethod
    def run(cls, parser: utils.Parser, data):
        name, metaname, kwargs = data
        parser.add_parser(metaname, name, **kwargs)


class SetDefault(Command):
    @classmethod
    def name(cls):
        return "set_defaults"

    @classmethod
    def help(cls):
        return textwrap.dedent(
            """
                Set defaults for parser with key/value pairs.

                This is a wrapper around ArgumentParser.set_defaults, and is
                commonly used to attach default values to a subparser to
                determine which subcommand was called. The subparser to attach
                to can be selected using `--subparser` and `--parser-arg`. All
                other key/value pairs are forwarded.

                e.g.:
                    parser=$({
                        argparsh subparser_init --metaname foo --required true

                        argparsh subparser_add fee
                        argparsh set_default --subparser fee --foocmd fee

                        argparsh subparser_add fie
                        argparsh set_default --subparser fee --foocmd fie
                    })

                    eval $(argparsh parse $parser -- "$@")
                    echo "value for foo was: " $foocmd

                If the above is called as `./prog.sh fee` it will print:
                    value for foo was: fee
            """
        )

    @classmethod
    def requires_subparser_arg(cls) -> bool:
        return True

    @classmethod
    def consumes_rest_args(cls) -> bool:
        return True

    @classmethod
    def construct(cls, args: argparse.Namespace) -> str:
        meth_kwargs = utils.arglist_to_kwargs(args.rest)
        return cls.output((args.subparser, args.parser_arg, meth_kwargs))

    @classmethod
    def run(cls, parser: utils.Parser, data):
        subparser, parser_arg, meth_kwargs = data
        p = parser.get_parser(parser_arg, subparser)
        p.set_defaults(**meth_kwargs)


_output_format = {}


def output_format(name: str):
    def deco(f):
        _output_format[name] = f
        return f

    return deco


@output_format("shell")
def output_shell(kv: dict, extra_args: list[str], output):
    parser = argparse.ArgumentParser(
        "argparsh parser --format shell",
        description="Declare a variable for every CLI argument",
    )
    parser.add_argument(
        "-p", "--prefix", help="Prefix to add to every declared variable", default=""
    )
    parser.add_argument(
        "-e",
        "--export",
        action="store_true",
        help="Export declarations to the environment",
    )
    parser.add_argument(
        "-l", "--local", action="store_true", help="declare variable as local"
    )
    args = parser.parse_args(extra_args)

    assert not (
        args.local and args.export
    ), "args cannot be declared as both local and export"
    export = ""
    if args.export:
        export = "export "
    if args.local:
        export = "local "

    for k, v in kv.items():
        print(f"{export}{args.prefix}{k}={repr(v)}", file=output)


@output_format("assoc_array")
def output_assoc_array(kv: dict, extra_args: list[str], output):
    parser = argparse.ArgumentParser(
        "argparsh parser --format assoc_array",
        description="Create an associative array from parsed arguments",
    )
    parser.add_argument(
        "-n", "--name", required=True, help="Name of variable to output into"
    )
    args = parser.parse_args(extra_args)

    print(f"declare -A {args.name}", file=output)
    for k, v in kv.items():
        print(f'{args.name}["{k}"]={repr(v)}', file=output)


@output_format("json")
def output_json(kv: dict, extra_args: list[str], output):
    assert len(extra_args) == 0
    json.dump(kv, output, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """\
                Shell agnostic argument parser leveraging Python's argparse.
                Each command will output the parser state to stdout. Concatenating the states will create a parser which can be passed to the "parse" subcommand.

                Example (assumes the shell is bash):

                    parser=$({
                        # $0 expands to the name of the script
                        argparsh new $0 --description "My program"

                        argparsh add_arg myarg -- --help "Some positional argument"
                        argparsh add_arg -f --flag -- --help "Some keyword argument"
                    })

                    # Pass cli args to the parser constructed above
                    eval $(argparsh parse $parser -- "$@")

                    echo "myarg =" $myarg
                    echo "flag =" $flag

                Most subcommands are wrappers around an argparse function, and will convert command line arguments to keyword arguments in python.
            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(required=True)

    for command in commands.values():
        p = subparsers.add_parser(command.name(), help=command.help())
        p.set_defaults(command=command)
        if command.requires_subparser_arg():
            p.add_argument(
                "--subparser",
                help="Name of subparser command (argument to create)",
                default=None,
            )
            p.add_argument(
                "--parser-arg",
                help="Name of subparser argument (argument to init)",
                default=None,
            )
        command.extend_parser(p)

    p = subparsers.add_parser(
        "parse",
        help=textwrap.dedent(
            """
            Parse command line arguments

            This command should usually be used with `eval` or some equivalent
            to bring the parsed arguments into scope. e.g.:
                eval $(argparsh parse $parser -- "$@")

            Note that `--` is used to separate arguments to `argparsh parse`
            from the arguments being parsed.

            Optionally, the `--format` option can be supplied to change the
            output format.

            --format shell [--prefix PREFIX] [-e/--export] [-l/--local]
                By default, the format is "shell", where every parsed argument
                is created as a shell varaible (with the syntax `KEY=VALUE`).
                Optionally, a prefix can be supplied with `--prefix` or `-p`:
                    # Parse an argument named "value"
                    parser=$(argparsh add_arg value)

                    # Will create an variable named "arg_value"
                    eval $(argparsh parse $parser -p arg_ -- "$@")
                the flags `--export`/`-e` and `--local`/`-l` will respectively
                either declare the variables as "export" (make the variable an
                environment variable) or "local" (bash/zsh only).

            --format assoc_array --name NAME
                This declares a new associative array named `NAME` where every
                argument/value is a key/value entry in the associative array:
                    # Parse an argument named "value"
                    parser=$(argparsh add_arg value)

                    # Will create a associative array (dictionary) variable named "args"
                    eval $(argparsh parse $parser --format assoc_array --name args -- "$@")

                    # Access the "value" key from $args
                    echo ${args["value"]}

            --format json
                outputs the parsed arguments as json

            In any mode on failure to parse arguments for any reason (including
            if the arguments invoked the help text), stdout will contain a
            single line with the contents "exit <code>". And argparsh will exit
            with the exit status also being set to `code`. Note that explit
            invocation of help will result in a code of 0, while failure to
            parse arguments will result in a non-zero code.
        """
        ),
    )
    p.set_defaults(command=None)
    p.add_argument("state", help="Parser program constructed by argparsh calls")
    p.add_argument(
        "--format",
        default="shell",
        choices=_output_format.keys(),
        help="Output format of parsed arguments",
    )

    args, unconsumed = parser.parse_known_args()
    if args.command is not None and not args.command.consumes_rest_args():
        if len(unconsumed):
            raise ValueError(f"Unexpected arguments! {unconsumed}")
    args.rest = unconsumed

    if args.command:
        print(args.command.construct(args), end="")
    else:
        output = sys.stdout
        sys.stdout = sys.stderr

        actions = utils.parse_state(args.state)

        new_parser = utils.Parser()
        for name, data in actions:
            commands[name].run(new_parser, data)

        extra_args = []
        found_sep = False
        while len(args.rest):
            if args.rest[0] == "--":
                args.rest.pop(0)
                found_sep = True
                break
            extra_args.append(args.rest[0])
            args.rest.pop(0)
        if not found_sep:
            args.rest = extra_args
            extra_args = []

        try:
            parsed_args = new_parser.parser.parse_args(args.rest)
            _output_format[args.format](
                dict(parsed_args._get_kwargs()), extra_args, output
            )
        except SystemExit as e:
            print(f"exit {e}", file=output)
            exit(e.code)
