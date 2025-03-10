from jupyterbook_patches.patches import BasePatch, logger
from sphinx.application import Sphinx
import docutils
import os

class MatplotlibButtonPatch(BasePatch):
    name = "button"

    def initialize(self, app):
        logger.info("Initializing button patch")
        app.connect('html-page-context',add_css_fix,priority=1000)
        app.connect('build-finished',remove_js_fix,priority=1000)

def add_css_fix(app: Sphinx,pagename: str,templatename: str, context: dict[str,any],doctree:list[docutils.nodes.document,None]):

    if 'sourcename' in context:
        if context['sourcename'].endswith('.ipynb'):
            dirpath = app.srcdir
            filename = context['sourcename']
            with open(os.path.join(dirpath,filename),'r') as file:
                for line_number, line in enumerate(file, start=1):
                    try:
                        if line.strip().replace('"','')[0] != '#':
                            if '%matplotlib widget' in line or '%matplotlib ipympl' in line:
                                app.add_css_file('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css',priority=1000,integrity="sha512-5A8nwdMOWrSz20fDsjczgUidUBR8liPYU+WymTZP1lmY9G6Oc7HlZv156XqnsgNUzTyMefFTcsFH/tnJE/+xBg==",crossorigin="anonymous")
                    except:
                        pass

    pass

def remove_js_fix(app: Sphinx, exc):

    builddir = app.outdir
    sourcedir = os.path.join(builddir,'_sources')
    files = []
    # find ipynb sources
    for dirpath, dirnames, filenames in os.walk(sourcedir):
        for filename in filenames:
            if filename.endswith('.ipynb'):
                with open(os.path.join(dirpath,filename),'r') as file:
                    for line_number, line in enumerate(file, start=1):
                        try:
                            if line.strip().replace('"','')[0] != '#':
                                if '%matplotlib widget' in line or '%matplotlib ipympl' in line:
                                    files.append(filename.replace('.ipynb','.html'))
                        except:
                            pass
    
    # for each of the build files, load file found and replace
    for dirpath, dirnames, filenames in os.walk(builddir):
        for file in filenames:
            if file in files:
                file_location = os.path.join(dirpath,file)
                with open(file_location,'r') as html_code:
                    new_html_code = '<!-- HTML code rerendered -->'
                    comment_next_line = False
                    for line_number, line in enumerate(html_code, start=1):
                        if comment_next_line:
                            new_html_code += '<!-- '+line[:-1]+' -->\n'
                        else:
                            new_html_code += line
                        if '<!-- So that users can add custom icons -->' in line:
                            comment_next_line = True
                        else:
                            comment_next_line = False
                # ovewwrite the html page
                with open(file_location,'w') as new_file:
                    new_file.writelines(new_html_code)
    pass