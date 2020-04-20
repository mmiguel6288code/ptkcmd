# ptkcmd

[View API documentation](http://htmlpreview.github.io/?https://github.com/mmiguel6288code/ptkcmd/blob/master/docs/ptkcmd/index.html)

ptkcmd adapts the built-in cmd.py standard library module to use prompt-toolkit instead of readline

```
from ptkcmd import PtkCmd, Completion, complete_files

class MyCmd(PtkCmd):
    """
    stdin, stdout, intro are as defined in the standard library cmd.py

    If interactive is True, then the prompt-toolkit prompt() 
	    method will be utilized from a PromptSession.
    If interactive is False, then the prompt will be written 
        to stdout and a line read from stdin

    If do_complete_cmd is True, then completion will be performed
	    for the initial command of each line against the list of known
        commands.
    If do_complete_cmd is False, no completion will be attempted for 
        the initial command.
    In either case, completion can be attempted for the arguments 
        according to any 'complete_' methods defined.

    If default_shell is False, then receiving a command that does not 
        have a "do_" method will result in writing an error to
        self.stdout.
    If default_shell is True, then the command will be used as an 
        input to subprocess.run(). The shell input to run() will be 
        False.

    If additional keyword arguments are provided, they will be passed 
        to the PromptSession constructor that is used for prompts.
    The only PromptSession keyword argument not allowed is 'completer'.
	"""

    prompt='MyPtkCmd$ ' #change the prompt

    def do_mycmd(self,args)
    	"""
        This is a command named 'mycmd'.
        When a command is executed by PtkCmd, the initial line that is 
            entered is split by shlex.split().
        The first item, i.e. the command, is used to determine which 
            "do_" method to call.
        The args input is the list, excluding the command itself.
        All commands will show up when the help command is invoked.

        Typing 'help mycmd' will show the docstring of do_mycmd().

        """
        self.stdout.write('mycmd args were %s\n' % repr(args))

    def help_mytopic(self):
    	"""
        This is a help topic named 'mytopic'.
        All topics declared in this way will show up when the help 
            command is invoked.

        Typing 'help mytopic' will execute the help function, which 
            typically will write some text to self.stdout
        """
        self.stdout.write('You called help for mytopic\n')

    def complete_mycmd(self,prev_args,curr_arg,document,complete_event):
    	"""
        This method defines completion rules for the command named 'mycmd'

        prev_args = the arguments prior to the current one being completed
        curr_arg = the current argument being completed. 
        completed
        May be an empty string or the start of an argument that
            from the list of completable arguments.
        document and complete_event are as defined in the prompt-toolkit 
            documentation
        Should yield Completion objects as defined in prompt-toolkit
            Completion(text,start_position)
                text = a suggested completion
                start_position = non-positive number representing
                    how many characters from the cursor to go back
                    and overwrite.

	"""
        yield from complete_files(curr_arg)
```

