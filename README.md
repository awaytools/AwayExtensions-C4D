AwayExtensions-C4D
==================


## What are Away Extensions C4D ?

Away Extensions C4D are a collection of complimentary tools for use in an Away3D project workflow. 
The current extensions list includes an AWD exporter plugin for Cinema4D R13+, that enables the export of C4D-scenes as AWD-files. 
Like all other Away Extensions, it is free and open source. 


## How should Away Extensions C4D be used ?

Away Extensions C4D can currently be used to create AWD files that can be loaded and used within the Away3D Engine. 
Since some C4D object properties cannot be mapped to Away3D object properties, 
it is recommended to inspect and finalize the exported files using [Away Builder](http://www.awaytools.com/awaybuilder).


## How to install Away Extensions C4D ?

Copy the folder "AwayExtensions-C4D" into your Cinema4D plugin directory. 

In Cinema4D, you should see a menu item for the AWD Exporter plugin in the plugins menu, 
and several tag plugins in the tag menu (right-mouse-click on objects in the object-manager).


## What is the current state of development for the AWD-Tools-C4D ?

Away Extensions C4D is still in a early state of development. 
At the moment there are no dependencies on the [AWD-SDK](https://github.com/awaytools/awd-sdk) libraries or any other resource, 
although this is planned for the future. It is written in python, 
and will soon be refactored to make use of the [ppyAWD](https://github.com/awaytools/awd-sdk/tree/master/python-ppyawd) library.


## Where can i get more information/documentation about Away Extensions C4D?

There is a documentation included in the plugin (Menu: File->Help), although this is still work in progress. 
We will be providing more articles and tutorials about Away Extensions C4D on [our website] (http://www.awaytools.com/awayextensions).

Current Articles / Tutorials:

* [Introducing Away Extensions C4D](http://www.awaytools.com/awayextensions/introducing-awayextensionsc4d)