import argparse


def checkEnv(env):
    """Returns true if environment argument is one of "local", "prod", "preprod"."""
    env_options = ["local", "prod", "preprod"]

    return env in env_options


def add_common_arguments(parser):
    parser.add_argument(
        "--verbose",
        default=False,
        help="Verbose flag for extra info about deploying process",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=None,
        type=str,
        help="Version for tagging of created containers",
    )
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="local",
        help="Environment to deploy. Possible options: local, prod, preprod.",
    )


def defineArgs():
    parser = argparse.ArgumentParser(
        description="""
        cosmctl - utilite for deploying project locally and into cloud.
        All configuration and scripts should be stored in Docker/ directory in root of your project.
    """
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands for cosmctl")

    commands_with_common_args = ["build", "run", "build-run"]

    for cmd in commands_with_common_args:
        subparser = subparsers.add_parser(cmd, help=f"{cmd} project containers")
        add_common_arguments(subparser)

    stop_parser = subparsers.add_parser("stop", help="Stop running containers")
    stop_parser.add_argument(
        "--verbose",
        default=False,
        help="Verbose flag for extra info about the stopping process",
        action="store_true",
    )
    stop_parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="local",
        help="Environment to deploy. Possible options: local, prod, preprod.",
    )
    scan_parser = subparsers.add_parser("scan", help="Scan for .cosmctl directories")
    scan_parser.add_argument(
        "-d",
        "--depth",
        default=1,
        type=int,
        help="Scan directories recursively from the directory where cosmctl is being executed",
    )

    return parser.parse_args()


def getParsedArgs(args):
    command = args.command
    env = getattr(args, "env", None)
    versionTag = args.version if command in ["build", "run", "build-run"] else None
    depth = args.depth if command is "scan" else None
    verboseFlag = args.verbose

    return (env, versionTag, verboseFlag, command, depth)
