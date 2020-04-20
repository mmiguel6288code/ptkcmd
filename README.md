# ptkcmd

[View API documentation](http://htmlpreview.github.io/?https://github.com/mmiguel6288code/ptkcmd/blob/master/docs/ptkcmd/index.html)

ptkcmd adapts the built-in cmd.py standard library module to use prompt-toolkit instead of readline

Constructor inputs:
```
from ptkcmd import PtkCmd, Completion, complete_files
class MyCmd(PtkCmd):
    prompt='MyPtkCmd$ ' #change the prompt
    def __init__(self,stdin=None,stdout=None,intro=None,
    	interactive=True,do_complete_cmd=True,
	default_shell=False,**psession_kwargs):
        super().__init__(stdin,stdout,intro,interactive,
		do_complete_cmd,default_shell,**psession_kwargs)
```
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

If default_shell is False, then receiving a command that does not have a "do_" method will result in writing an error to self.stdout.
If default_shell is True, then the command will be used as an 
input to subprocess.run(). The shell input to run() will be 
False.

If additional keyword arguments are provided, they will be passed 
to the PromptSession constructor that is used for prompts.
The only PromptSession keyword argument not allowed is 'completer'.

The following snippet defines a command named 'mycmd'.
The args input is the list of arguments entered after the command.


class MyCmd(PtkCmd):
    ...

    def do_mycmd(self,args)
    	"""
        """
        self.stdout.write('mycmd args were %s\n' % repr(args))

    def complete_mycmd(self,prev_args,curr_arg,document,complete_event):
    	"""

	"""
        yield from complete_files(curr_arg)
```

Regarding the completion method,
prev_args = the arguments prior to the current one being completed
curr_arg = the current argument being completed. 
curr_arg may be an empty string or the start of an argument that from the list of completable arguments.

document and complete_event are as defined in the prompt-toolkit 
    documentation

The completion method must yield Completion objects as defined in prompt-toolkit:
    Completion(text,start_position)
	text = a suggested completion
	start_position = non-positive number representing
	    how many characters from the cursor to go back
	    and overwrite.

complete_files(curr_arg,path=None) provides the a filename completer

Typing 'help mycmd' will show the docstring of do_mycmd().
To add miscellaneous help topics, define a help function:
```
class MyCmd(PtkCmd):
    ...

    def help_mytopic(self):
    	"""
        This is a help topic named 'mytopic'.
        All topics declared in this way will show up when the help 
            command is invoked.

        Typing 'help mytopic' will execute the help function, which 
            typically will write some text to self.stdout
        """
        self.stdout.write('You called help for mytopic\n')
```
