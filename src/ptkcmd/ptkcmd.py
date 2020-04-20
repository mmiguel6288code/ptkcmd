"""
Adapted from cmd.py in python standard library.
"""
import sys, string, shlex, textwrap, os, os.path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

__version__ = '0.0.1'

def complete_files(curr_arg,path=None):
    if path is None:
        path = os.getcwd()
    full_path = os.path.join(path,curr_arg)
    if curr_arg == '' or full_path.endswith('/'):
        if os.path.exists(full_path):
            for item in os.listdir(full_path):
                yield Completion(item,0)
    else:
        dirname,basename = os.path.split(full_path)
        if os.path.exists(dirname):
            for item in os.listdir(dirname):
                if item.startswith(basename):
                    yield Completion(item,-len(basename))

class PtkCmdCompleter(Completer):
    def __init__(self,ptkcmd):
        self.ptkcmd = ptkcmd

    def get_completions(self,document,complete_event):
        yield from self.ptkcmd.complete(document,complete_event)


class PtkCmd():
    identifer_chars = string.ascii_letters + string.digits + '_'
    prompt = '(PtkCmd) '
    style = Style.from_dict({
        'prompt':'#6600ff',
        })
    nohelp = "*** No help on %s"
    doc_leader = ""
    doc_header = "Documented commands (type help <topic>):"
    misc_header = "Miscellaneous help topics:"
    undoc_header = "Undocumented commands:"
    ruler = '='
    def __init__(self,stdin=None,stdout=None,intro=None,interactive=True,do_complete_cmd=True,default_shell=False,**psession_kwargs):
        if stdin is None:
            stdin = sys.stdin
        if stdout is None:
            stdout = sys.stdout
        self.stdin = stdin
        self.stdout = stdout
        if 'completer' in psession_kwargs:
            raise Exception('Custom completer cannot be used')
        self.completer = PtkCmdCompleter(self)
        psession_kwargs['completer'] = self.completer
        if 'style' in psession_kwargs:
            self.style = psession_kwargs['style']
        else:
            psession_kwargs['style'] = self.style
        if not 'key_bindings' in psession_kwargs:
            bindings = KeyBindings()
            @bindings.add('c-d')
            def eof_keypress(event):
                event.app.exit()
            psession_kwargs['key_bindings'] = bindings
        self.psession = PromptSession(**psession_kwargs)
        self.intro = intro
        self.cmdqueue = []
        self.interactive = interactive
        self.do_complete_cmd = do_complete_cmd
        self.default_shell = default_shell
        
        names = dir(self.__class__)
        cmds_doc = set() 
        cmds_undoc = set()
        help_doc = set()
        help_info = {}
        cmds_comp = set()
        for name in names:
            if name.startswith('help_'):
                name = name[5:]
                help_doc.add(name)
            elif name.startswith('do_'):
                if getattr(self,name).__doc__:
                    cmds_doc.add(name[3:])
                else:
                    cmds_undoc.add(name[3:])
            elif name.startswith('complete_'):
                cmds_comp.add(name[9:])
        help_doc -= (cmds_doc | cmds_undoc)
        self.cmds = list(sorted(cmds_doc | cmds_undoc))
        self.cmds_doc = list(sorted(cmds_doc))
        self.cmds_undoc = list(sorted(cmds_undoc))
        self.help_doc = list(sorted(help_doc))
        self.cmds_comp = list(sorted(cmds_comp))
    

    def cmdloop(self,intro=None):
        self.preloop()

        if self.intro is not None:
            self.stdout.write(str(self.intro)+"\n")
        stop = None
        while not stop:
            if len(self.cmdqueue) > 0:
                line = self.cmdqueue.pop(0)
            else:
                if self.interactive:
                    try:
                        line = self.psession.prompt(self.prompt)
                        if line is None:
                            stop = True
                            break
                    except EOFError:
                        line = ''
                else:
                    self.stdout.write(self.prompt)
                    self.stdout.flush()
                    line = self.stdin.readline()
                    if not len(line):
                        line = ''
                    else:
                        line = line.rstrip('\r\n')
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def preloop(self):
        pass
    def precmd(self,line):
        return line
    def onecmd(self, line):
        line = line.strip()
        cmd_args = shlex.split(line)
        if len(cmd_args) == 0:
            return
        cmd = cmd_args[0]
        self.lastcmd = line
        if hasattr(self,'do_'+cmd):
            return getattr(self,'do_'+cmd)(*cmd_args[1:])
        else:
            return self.default(cmd_args,line)

    def default(self,cmd_args,line):
        if line.startswith('?'):
            return self.onecmd('help '+line[1:])

        if self.default_shell:
            if line.startswith('!'):
                cmd_args[0] = cmd_args[0][1:]
                proc = subprocess.run(cmd_args)
                return
            elif line.startswith('$'):
                m = re.search('\\$([^=]+)=(.+)',line)
                if m is not None:
                    var_name,value = m.groups()
                    os.environ[var_name] = value
                    return
            proc = subprocess.run(cmd_args)
        else:
            self.stdout.write('*** Unknown syntax: %s\n'%line)

    def complete(self, document, complete_event):

        """
        cases:
            if stuff after cursor, pretend nothing exists up until cursor
            no arguments typed:
                if  do complete_char then complete names
            =1 argument typed, cursor not on space, nothing later:
                if do_complete_char, then complete names
            =1 argument typed, cursor on space, nothing later:
                call completion for given cmd, prev_args=[], current_arg=''
            >=2 arguments typed, cursor not on space, nothing later:
            >=2 arguments typed, cursor on space, nothing later:

        """
        cmd_args = shlex.split(document.current_line_before_cursor)
        on_whitespace = document.char_before_cursor in ' \t'
        if len(cmd_args) == 0:
            if self.do_complete_cmd:
                prev_args = []
                curr_arg = ''
                yield from self.completenames(prev_args,curr_arg,document,complete_event)
                return
            else:
                #no completion
                return
        elif len(cmd_args) == 1:
            if on_whitespace:
                prev_args = cmd_args
                curr_arg = ''
            else:
                if self.do_complete_cmd:
                    prev_args = []
                    curr_arg = cmd_args[0]
                    yield from self.completenames(prev_args,curr_arg,document,complete_event)
                else:
                    return
        else:
            if on_whitespace:
                prev_args = cmd_args
                curr_arg = ''
            else:
                prev_args = cmd_args[:-1]
                curr_arg = cmd_args[-1]

        cmd = cmd_args[0]
        if cmd in self.cmds_comp:
            #existing command complete
            yield from getattr(self,'complete_'+cmd)(prev_args,curr_arg,document,complete_event)
        else:
            #default complete
            yield from self.completedefault(prev_args,curr_arg,document,complete_event)

    def completedefault(self, prev_args, curr_arg, document, complete_event):
        return
        yield

    def completenames(self, prev_args, curr_arg, document, complete_event):
        if curr_arg == '':
            #all names
            yield from [Completion(name,0) for name in self.cmds]
        else:
            yield from [Completion(name,-len(curr_arg)) for name in self.cmds if name.startswith(curr_arg)]

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop
    def postloop(self):
        pass

    def do_help(self, *args):
        'List available commands with "help" or detailed help with "help cmd".'
        if len(args) == 1:
            arg = args[0]
            if hasattr(self,'help_'+arg):
                getattr(self,'help_'+arg)()
                return
            elif hasattr(self,'do_'+arg):
                doc = getattr(self,'do_'+arg).__doc__
                if doc:
                    self.stdout.write(str(doc)+'\n')
                    return
            self.stdout.write((self.nohelp % arg) + '\n')
        elif len(args) == 0:
            self.stdout.write("%s\n"%str(self.doc_leader))
            self.print_topics(self.doc_header,   self.cmds_doc,   15,80)
            self.print_topics(self.misc_header,  self.help_doc,15,80)
            self.print_topics(self.undoc_header, self.cmds_undoc, 15,80)
        else:
            self.stdout.write('help command not understood\n')

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write("%s\n"%str(header))
            if self.ruler:
                self.stdout.write("%s\n"%str(self.ruler * len(header)))
            self.columnize(cmds, maxcol-1)
            self.stdout.write("\n")
    def columnize(self, inputs, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not inputs:
            self.stdout.write("<empty>\n")
            return

        nonstrings = [i for i in range(len(inputs))
                        if not isinstance(inputs[i], str)]
        if nonstrings:
            raise TypeError("list[i] not a string for i in %s"
                            % ", ".join(map(str, nonstrings)))
        size = len(inputs)
        if size == 1:
            self.stdout.write('%s\n'%str(inputs[0]))
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(inputs)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
                    if i >= size:
                        break
                    x = inputs[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(inputs)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = inputs[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.stdout.write("%s\n"%str("  ".join(texts)))
