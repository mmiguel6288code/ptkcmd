from ptkcmd import PtkCmd, Completion, complete_files
class MyPtkCmd(PtkCmd):
    prompt='MyPtkCmd$ '
    def __init__(self,stdin=None,stdout=None,intro=None,interactive=True,do_complete_cmd=True,default_shell=False,**psession_kwargs):
        super().__init__(stdin,stdout,intro,interactive,do_complete_cmd,default_shell,**psession_kwargs)
    def do_mycmd(self,*args):
        """
        This command is documented.
        """
        self.stdout.write('Args were %s\n' % repr(args))

    def do_myundoc(self,*args):
        self.stdout.write('Args were %s\n' % repr(args))

    def help_mytopic(self):
        self.stdout.write('You called help for mytopic\n')

    def complete_mycmd(self,prev_args,curr_arg,document,complete_event):
        yield from complete_files(curr_arg)

def test_ptkcmd():
    MyPtkCmd().cmdloop()


