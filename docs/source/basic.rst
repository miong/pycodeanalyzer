pycodeanalyzer in a few words
=============================

Presentation
------------

pycodeanalyzer is yet an other dynamic class diagram generator.


It's designed to parse sources once and then let you explore them using diagram or search.
The diagrams are generated on demand so that you don't wait for information you don't need.


But why not using Doxygen ?
---------------------------

Doxygen is a powerfull tool to generate documentation, including generating class diagrams.
Yet, pycodeanalyzer have some advantages and drawbacks compared to doxygen :

* Advantages
    #. Less time to generate, because we do only the class diagrams.
    #. Only pay time for analysis that you asked for
    #. Use no or a simple configuration on any new project
    #. Export Mermaid diagrams to let you use them at convenience
* Drawbacks
    #. Less information available because we do not compile the sources.
    #. Only share information from header file in C/C++

Which languages are supported ?
-------------------------------

The following languages are supported:

#. C/C++
#. Python, if annotation are used

The following languages should be supported:

#. Java
#. Kotlin

How does it works ?
-----------------

Pycodeanalyzer works by :

#. Filtering files from root dirs to keep only handled language files.
#. Parsing each source file and extract abstract objects representing the code.
#. On request, analyzing the code to get dependencies.
#. Generating Mermaid code for class diagram.
#. Use a portable webview to interact and show class diagram.
