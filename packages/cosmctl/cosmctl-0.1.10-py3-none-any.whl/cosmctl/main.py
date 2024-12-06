from cosmctl.modules.argsparser import checkEnv, defineArgs, getParsedArgs
from cosmctl.modules.commands import *


def main():
    args = defineArgs()
    environment, versionTag, verboseFlag, command, depth = getParsedArgs(args)
    # print(environment, versionTag, verboseFlag, command)

    # if not checkEnv(environment) and command != "stop":
    #     print(
    #         "Invalid environment argument. Type cosmctl --help to see argument description"
    #     )
    #     return

    if command == "build":
        command_instance = BuildCommand(environment, versionTag, verboseFlag)
    elif command == "run":
        command_instance = RunCommand(environment, versionTag, verboseFlag)
    elif command == "build-run":
        command_instance = BuildRunCommand(environment, versionTag, verboseFlag)
    elif command == "stop":
        command_instance = StopCommand(environment, None, verboseFlag)
    elif command == "scan":
        command_instance = ScanCommand(depth)
    else:
        print("Invalid command. Type cosmctl --help to see commands")
        return

    command_instance.execute()


if __name__ == "__main__":
    main()
