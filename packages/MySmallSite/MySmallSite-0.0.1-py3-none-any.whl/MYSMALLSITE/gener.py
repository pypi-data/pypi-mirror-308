#MySmallSite - gener.py

from os.path import isfile as _if
from os.path import isfile as _id
from os import mkdir as _md
from os.path import splitext as _spt
from sys import argv as _a

'''
# [[MySmallSite]] `gener.py`

    ## VARIALBE & LAMBDAS
        o = open
        w(f) = o(f, 'w')
        cli_app() = the function what works cli_core(sys.argv) (sys.argv = parameter)

    ## function() & @decorator
        \* plz use 'help([target])' to read the menual of it. \*
         - `help(wither)`
    
    ## CLI MENUAL
        ### CLI - MAIN WORK : webpage generating
            `$ python -m mysmallsite/gener.py [*.mys file name] to use.`
        ### CLI - SUB WORK : cli user-style app
            `$ python -m mysmallsite/gener.py work as self-user-input to use it-self`
        ### CLI - PRINTING MENUALS
            `$ python -m mysmallsite/gener.py -(-)h(elp)`
            `$ python -m mysmallsite/gener.py /h(elp)`
            `$ python -m mysmallsite/gener.py /H`
'''

o = open
w = lambda f : o(f, 'w')

def wither(opener = o):
    '''
    # decorator @wither(opener = o)
    
    @wither(opener = o)
    [function declaring part]

     = > the function will work in file-opener's open context manager.

        ## ** details **
            FACT) `wither() `== `wither(o)` == `wither(opener)`
            FACT)
                > ```
                > @[decorator]
                > def [funcname]([argvs]):
                >     ~~~
                > ```
                >
                >
                > works
                >
                >
                > ```
                > [funcname] = [decorator]([funcname])
                > ```
            ABOUT WITHER, `wither(~)` is actually "function" **`with_deco`**.
            so, `with_deco` (wither(~)) works as decorater to Making a with_opener's file context management open manage by opener.
            see `help(wither())`.
    '''
    def with_deco(func):
        '''
        TIPS) see `help(wither)`

        # decorater-core-part **`with_deco`**
        @wither(opener)
        def function_name(file_manager, *argv, **kargv):
            \* WORKS \*
        
        ACTUALLY SIMMULAR)
            function_name(file_name, *argv, **kargv):
                with opener(file_name) as file_manager:
                    \* \~ :) \~ \*
        '''
        def with_opener(file_name, *argv, **kargv):
            '''
            `wither()` (=`with_deco`)'s decorated function result.
            see more about this function by do `help(wither)`!
            '''
            with opener(file_name) as fp: #make file context manager my fp to wrapping the function to decorater work function's work with 'with'
                return func(fp, *argv, **kargv)
        
        return with_opener
    return with_deco

@wither()
def read(file_name, *argv, **kargv):
    '''
    # function `read(filename, *argv, **kargv)`
    
    read file with context-manager as `open(file).read(*argv, **kargv)`

    TIP) it means it loads a file's text or binnary (warn : binarry not alible in windows) value.

    ~ I just start to be lazy....  nah ~
    '''
    return file_name.read(*argv, **kargv)

def write(file_name, value):
    '''
    # function `writer(file_name, value)`

        ## SRC
            ```
            @wither(w)
            def write_value(fp):
                return fp.write(value)
            return write_value(file_name)
            ```
            BAM.
    '''
    @wither(w)
    def write_value(fp):
        return fp.write(value)
    return write_value(file_name)

def formatting_a_Single_Page_Site_form(js_file_url_without_scheme : str) -> str:
    '''
    # function `formatting_a_Single_Page_Site_form(js_file_url_without_scheme : str) -> str`
    
        it just make a html page by formats my-small-site's-format by js-file-url.
    '''
    return f'<meta charset="utf-8"><script src="http://{js_file_url_without_scheme}"></script>'

def cli_core(cli_argv : list, user_inputer = input, user_input_prompt = 'the mys file to compare to website : ', help_menual_logger = print):
    '''
    # function `cli_core(cli_argv : list, user_inputer = input, help_menual_logger = print)`

     > `python -m mysmallsite/gener.py example_file.mys` to make file `mysmallsite.htm`
     > `python -m mysmallsite/gener.py` do it self user-input as function user-inputer
     > `python -m mysmallsite/gener.py -h`, `python -m mysmallsite/gener.py -help`, `python -m mysmallsite/gener.py --h`, `python -m mysmallsite/gener.py --help`, `python -m mysmallsite/gener.py /h', `python -m mysmallsite/gener.py /help`, `python -m mysmallsite/gener.py /H` prints help menual
    '''
    try:
        argv_length = len(cli_argv)
        assert argv_length < 3, TypeError("python -m mysmallsite/gener.py required argument is only one!! the \"*.mys file.\"!!!")
        if argv_length - 1: #length isn't 0 (=1)
            fn = cli_argv[1] #filename
        else:
            fn = user_inputer(user_input_prompt)
        if fn in "-h -help --help --h /h /help /H".split():
            return help_menual_logger('''
# [[CLI MENUAL]]

## CLI - MAIN WORK : webpage generating
    `$ python -m mysmallsite/gener.py [*.mys file name] to use.`
## CLI - SUB WORK : cli user-style app
    `$ python -m mysmallsite/gener.py work as self-user-input to use it-self`
## CLI - PRINTING MENUALS
    `$ python -m mysmallsite/gener.py -(-)h(elp)`
    `$ python -m mysmallsite/gener.py /h(elp)`
    `$ python -m mysmallsite/gener.py /H`
''')
        else:
            assert _if(fn), FileNotFoundError(f"no filename {fn}")
        fn_cor, fn_ext = _spt(fn) #split "[file name].mys" to "[filename], ext(mys)"
        #gui cha na tlqkf
        assert fn_ext == ".mys", TypeError(f"file {fn} isn't *.mys type.");  
    except AssertionError as err:
        raise err
    if not _id(fn_cor): _md(fn_cor)
    return write(f'{fn_cor}/index.htm', formatting_a_Single_Page_Site_form(read(fn)))

cli_app = lambda : cli_core(_a) #see menual.

main = cli_app #main function

if __name__ == "__main__": main()