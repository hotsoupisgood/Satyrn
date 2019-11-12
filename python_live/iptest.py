from IPython.terminal.prompts import Prompts, Token

class CustomPrompt(Prompts):

    def in_prompt_tokens(self, cli=None):

       return [
            (Token.Prompt, 'In <'),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, '>: '),
            ]

    def out_prompt_tokens(self):
       return [
            (Token.OutPrompt, 'Out<'),
            (Token.OutPromptNum, str(self.shell.execution_count)),
            (Token.OutPrompt, '>: '),
        ]
 

from traitlets.config.loader import Config
try:
    get_ipython
except NameError:
    nested = 0
    cfg = Config()
    cfg.TerminalInteractiveShell.prompts_class=CustomPrompt
else:
    print("Running nested copies of IPython.")
    print("The prompts for the nested copy have been modified")
    cfg = Config()
    nested = 1

# First import the embeddable shell class
from IPython.terminal.embed import InteractiveShellEmbed

# Now create an instance of the embeddable shell. The first argument is a
# string with options exactly as you would type them if you were starting
# IPython at the system command line. Any parameters you want to define for
# configuration can thus be specified here.
ipshell = InteractiveShellEmbed(config=cfg,
                       banner1 = 'Dropping into IPython',
                       exit_msg = 'Leaving Interpreter, back to program.')

# Make a second instance, you can have as many as you want.
ipshell2 = InteractiveShellEmbed(config=cfg,
                        banner1 = 'Second IPython instance.')

print('\nHello. This is printed from the main controller program.\n')

# You can then call ipshell() anywhere you need it (with an optional
# message):
ipshell('***Called from top level. '
        'Hit Ctrl-D to exit interpreter and continue program.\n'
        'Note that if you use %kill_embedded, you can fully deactivate\n'
        'This embedded instance so it will never turn on again')

print('\nBack in caller program, moving along...\n')
ipshell.banner2 = 'Entering interpreter - New Banner'
ipshell.exit_msg = 'Leaving interpreter - New exit_msg'

def foo(m):
    s = 'spam'
    ipshell('***In foo(). Try %whos, or print s or m:')
    print('foo says m = ',m)

def bar(n):
    s = 'eggs'
    ipshell('***In bar(). Try %whos, or print s or n:')
    print('bar says n = ',n)
    
# Some calls to the above functions which will trigger IPython:
print('Main program calling foo("eggs")\n')
foo('eggs')

# The shell can be put in 'dummy' mode where calls to it silently return. This
# allows you, for example, to globally turn off debugging for a program with a
# single call.
ipshell.dummy_mode = True
print('\nTrying to call IPython which is now "dummy":')
ipshell()
print('Nothing happened...')
# The global 'dummy' mode can still be overridden for a single call
print('\nOverriding dummy mode manually:')
ipshell(dummy=False)

# Reactivate the IPython shell
ipshell.dummy_mode = False

print('You can even have multiple embedded instances:')
ipshell2()

print('\nMain program calling bar("spam")\n')
bar('spam')

print('Main program finished. Bye!')
