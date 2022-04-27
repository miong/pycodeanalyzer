import codecs
import subprocess
import platform
from distutils.core import run_setup

def updateTemplate(templatePath, outputPath):
    text = ""
    with open(templatePath) as f:
        pythonCmd = 'python'
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            pythonCmd = 'python3'
        lines = f.readlines()
        for line in lines:
            if line == "[[USAGE]]\n":
                helpstr = "\t"+subprocess.check_output([pythonCmd, '-m', "pycodeanalyzer", "-h"]).decode("utf-8")
                text += '\t'.join(helpstr.splitlines(True))
                pass
            elif line == "[[REQUIREMENTS]]\n":
                result = run_setup("./setup.py", stop_after="init")
                for req in result.install_requires:
                    sep = "=="
                    if ">=" in req:
                        sep = ">="
                    item = [req, "latest"]
                    if sep in req:
                        item = req.split(sep)
                    else:
                        sep = ""
                    if sep == "==":
                        sep = "equals"
                    elif sep == ">=":
                        sep = "minimal"
                    else:
                        sep = "the"
                    text += "- .. image:: https://img.shields.io/static/v1?label={}&message={}%20{}&color=blue\n".format(item[0], sep, item[1])
                    text += "    :alt: - {} - {} {}\n".format(item[0], sep, item[1])
            else:
                text += line
    with codecs.open(outputPath, "w", "utf-8") as output:
        output.write(text)
    print(outputPath, "generated from", templatePath)

def updateTemplates():
    updateTemplate('readme.template', 'README.rst')
    updateTemplate('docs/source/install.template', 'docs/source/install.rst')
    updateTemplate('docs/source/usage.template', 'docs/source/usage.rst')

def main():
    updateTemplates()

if __name__ == "__main__":
    main()
