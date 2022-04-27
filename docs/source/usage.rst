Pycodeanalyzer usage
====================

Dynamic Class diagram view
--------------------------

The goal of Pycodeanalyzer is to allow you to browse interactive Class diagram views of your code source.

The only thing needed to do that is calling Pycodeanalyzer with the path of all the root dirs of the sources.

If you need to precise information for the source analysis, please used a configuration file as described below.

Exporting diagrams
------------------

Pycodeanalyzer allow to export all the class diagrams that could be browsed at once.

Using the exportDiagrams and a path to the folder to contains the diagrams, all diagrams will be exported as textual.

The format of the export can be set using exportFormat option, with the following format supported:
    * MermaidJS syntax
    * PlantUML syntax

The textual files can be used to generate images or be included any content parsed by one of this tools.

To get more inforamtion about those UML tools, please see the following pages:
    * MermaidJS: https://mermaid-js.github.io/mermaid/#/
    * PlantUML: https://plantuml.com/fr/

Nota Bene:
    To export diagrams without interactive view, use the no-ui option

Pycodeanalyzer help
-------------------

The following is the help of pycodeanalyzer::

	usage: pycodeanalyzer [-h] [--config CONFIGFILE] [--create-config TEMPLATEFILE] [--log {CRITICAL,ERROR,WARNING,INFO,DEBUG}] [--exportDiagrams EXPORTPATH] [--exportFormat {mermaid,plantuml}] [--dumpobj]
	                      [--no-ui]
	                      [path [path ...]]
	
	positional arguments:
	  path                  Path of a root directory to be analysed
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --config CONFIGFILE   Configuration file to be used
	  --create-config TEMPLATEFILE
	                        Create a configuration file template. Should be used alone.
	  --log {CRITICAL,ERROR,WARNING,INFO,DEBUG}
	                        Log level to be used
	  --exportDiagrams EXPORTPATH
	                        Export all class diagrams to the path specified
	  --exportFormat {mermaid,plantuml}
	                        Format to be used for exported class diagrams
	  --dumpobj             Serialize objets found, mainly for test purpose
	  --no-ui               Discard UI, mainly for test purpose

To get more information during the run, use log=DEBUG

Pycodeanalyzer configuration file
---------------------------------

Pycodeanalyzer can use a configuration with the config option.
To know about the configuration file see :doc:`configuration file <./config>` page
