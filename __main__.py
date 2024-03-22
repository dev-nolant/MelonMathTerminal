# Dependencies
import contextlib
import io
import ast
import os
import sys

help_commands = ['help', 'clear', 'restart']
# ----------------------------------------------------------------
# io Initializers
f = io.StringIO()
# ----------------------------------------------------------------
# Cog Imports
with contextlib.redirect_stdout(f):
    import cogs
loaded_cogs = f.getvalue()
f.close()
# ----------------------------------------------------------------
# Cog Exception Handler


class CogErrorHandler(Exception):
    """Exceptions raised for errors with cogs.

    Attributes:
        cog -- input cog which caused the error
    """

    def __init__(self, cog: str = None):
        self.cog = cog
        if cog is None:
            self.message = "No cog specified"
        elif cog not in loaded_cogs:
            self.message = f"Cog was not imported. No Cog exists by the name: {cog}"
        else:
            self.message = "Went un-imported."
        super().__init__(f"COG ATTEMPTED: {cog}", self.message)
# Command Exception Handler


class CommandErrorHandler(Exception):
    """Exceptions raised for errors with commands.

    Attributes:
        command -- input command which caused the error
    """

    def __init__(self, command: str = None, additional_message=None):
        self.command = command
        if command is None:
            self.message = "No command specified"
        elif additional_message:
            self.message = f"Command was processed, but returned an error. {additional_message}"
        else:
            self.message = "Went un-executed."
        super().__init__("COMMAND ATTEMPTED: ",
                         f"{command}", "-> ", self.message)

# ----------------------------------------------------------------


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("----------------------------------------")
    print("--------Math Systems Terminal-----------")
    print("--------Designed by: Nolan Taft---------")
    print("--------Email: contact@nolantaft.com----")
    print("----------------------------------------")
# Command Handler


class Cog(object):
    def __init__(self, object):
        # Hard Coded Help Commands

        if(object == "help"):
            self.module_help(object)
            pass
        elif(object == "clear"):
            clear_terminal()
            pass
        elif(object == "exit"):
            sys.exit()
        elif(object == "restart"):
            os.execv(sys.executable, ['python'] + sys.argv)

    # Dynamic Coded Commands
        else:
            if object in loaded_cogs:
                self.string_cog = f"cogs.{object}"
                self.command_method = getattr(cogs, object)
                self.commands = dir(self.command_method)
            elif object not in help_commands:
                print(f"COMMAND NOT FOUND: {object}")
                self.module_help(object)
    '''[Help Module]
    Return help for the user after called.
    This will grab all cogs from \cogs\ and 
    their description in them, then return 
    to the user.
    '''

    def module_help(self, on_cog=None):
        fixed_list = ast.literal_eval(loaded_cogs)
        count_of_cogs = len(fixed_list)
        print(count_of_cogs, "Cogs loaded successfully")
        print("-"*count_of_cogs*10)  # print deliminer
        print("BUILT-IN: ")
        for builtInCommand in help_commands:
            print(builtInCommand)
        print("-"*count_of_cogs*10)  # print deliminer
        counter = 0
        for cog in fixed_list:
            command_method = getattr(cogs, cog)
            try:
                description = command_method.__DESCRIPTION__
                print(f"""{cog.upper()}\n{description}\n""")
            except:
                print(
                    f"""{cog.upper()}\nThere has been no description and usage set.\n""")

        print("-"*count_of_cogs*10)  # print deliminer

    def execute(self, command, *args):

        # Interprets commands from mangle commands
        args_method = getattr(self.command_method, command)

        # Handles command(s)
        if command in self.commands:
            try:
                module_output = args_method(*args)
                if(module_output):
                    print(module_output)
                else:
                    pass
            except Exception as e:
                raise CommandErrorHandler(command, e)

        elif command not in self.commands:
            raise CommandErrorHandler(str(command))
        else:
            raise CommandErrorHandler()


# ----------------------------------------------------------------
if __name__ == "__main__":
    clear_terminal()
    while True:
        user_in = input(">").split()
        if user_in:
            if user_in[0] not in help_commands:
                print("\n")
                cog = Cog(user_in[0].lower())
                args = user_in[1:]
                if args:
                    cog.execute(*args)
            else:
                print("\n")
                Cog(user_in[0])
