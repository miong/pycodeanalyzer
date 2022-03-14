import subprocess
from distutils.core import run_setup


def main():
    readme = ""
    with open('readme.template') as f:
        lines = f.readlines()
        for line in lines:
            if line == "[[USAGE]]\n":
                helpstr = "\t"+subprocess.check_output(['python', '-m', "pycodeanalyzer", "-h"]).decode("utf-8")
                readme += '\t'.join(helpstr.splitlines(True))
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
                    readme += "- .. image:: https://img.shields.io/static/v1?label={}&message={}%20{}&color=blue\n".format(item[0], sep, item[1])
                    readme += "    :alt: - {} - {} {}\n".format(item[0], sep, item[1])
            else:
                readme += line
    print(readme)


if __name__ == "__main__":
    main()
