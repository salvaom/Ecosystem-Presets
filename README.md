#Ecosystem-Presets
A very, **very** simple preset manager for  [Ecosystem](https://github.com/PeregrineLabs/Ecosystem)
- - -


After playing with the amazing [Ecosystem](https://github.com/PeregrineLabs/Ecosystem) by [Peregrine*Labs](http://peregrinelabs.com/open-source/) I realized that even if I love to play with the shell and its commands, not everybody is made for that life, and is not that easy to remember the command

```
eco maya2015,yeti1.3.19,mtoa1.2.0.1,deadline7,vray2.40,qt4.8.2,pyside1.2.2
```

 so I decided to write a small preset manager.

Why?
====
Would you like to do this?


```
ecosystem preset -p maya/2015
```
And get all the necessary plugins and envs based on a preset? Would you like to run
```

ecosystem preset -p avatar7/nuke
```
OR
```
ecosystem preset -p avatar7/shot003/maya
```
and get all the specific plugins with the proper versions and then launch your desired software? That's why.

Why the lack of creativity in the name?
==============================

I like to keep my commands as short and self-descriptive as possible. This one is for running presets, based on ecosystem, ergo the name.

Installation
=========
```
python setup.py install
ecosystem preset --help
```


(Optional) Add as many app search folder with the environment variable ``ECO_PRESET_PATH`` (separated by your specific ``os.pathsep``).

How does it work?
==============

This software goes to all folders specified in the ``ECO_PRESET_PATH`` (or the default directory, if not specified) does a recursive scan (python ``os.walk()``) to pick up all JSON files within. When found, it will check that these files are valid JSON files, and if so, it will add them to the list of presets as relative paths. Let's say that we have in ``ECO_PRESET_PATH`` the following folder structure:

```

example
    maya
        2014.json
        2015.json
    myProject
        maya
            2014.json
            2015.json
        shot001
            maya.json
            nuke.json
    nuke
        9.1.json


```

The list of valid command will be the following:

```
ecosystem preset -p example/maya/2014
ecosystem preset -p example/maya/2015
ecosystem preset -p example/myProject/maya/2015
ecosystem preset -p example/myProject/maya/2014
ecosystem preset -p example/myProject/shot001/maya
ecosystem preset -p example/myProject/shot001/nuke
ecosystem preset -p example/nuke/9.1

```

The JSON files contain the following structure:
```
#!json

{
    "requires": [       //All the ecosystem .env files to include.
        "maya2015",
        "mtoa1.2.1.0",
        "yeti1.3.18",
        "deadline7"
    ],
    "launcher": "maya"   //Just for Windows: the launcher name (-r).
}

```
Will build in Windows the command:

``${ECO_ROOT}\bin\eco.cmd -t maya2015,mtoa1.2.1.0,yeti1.3.8,deadline7 -r maya``

And in UNIX based systems:
``${ECO_ROOT}\bin\ecosystem.py maya2015,mtoa1.2.1.0,yeti1.3.8,deadline7 ``


You can also run ``ecosystem preset --list`` to list all available presets.

What about render managers? (WIP)
=============================

If called without ``--preset`` as an argument, the extension will pick the application name and the preset from the environment variable ``ECO_PRESET``. Also, it populates this environment variable in the executed software and passes them to it.

For example, let's say that we want to send a Maya render to Deadline from an application launched from the extension. Well, for instance, if you set up the Deadline Maya executable to be ``ecosystem preset`` and make sure you pass to the slave the environment variables (that will be already in the software), Deadline should be picking up Maya with all the proper plugins.

What about extra arguments for the specific software?
=====================================================

The extension is agnostic of any arguments that you pass. If not ``--from-envs`` specified, the first argument will be the preset name and the rest will be extra, if ``--from-envs`` is specified, all arguments will be passed directly to the software to be launched, and the preset will be picked from the environment variable ``ECO_PRESET``.


ToDo
====

**Preset inheritance**

Enable preset inheritance, so the following will ocur.

``maya/2015.json``
```
#!json

{
    "name": "2015",
    "requires": [
        "maya2015",
        "mtoa1.2.1.0",
        "yeti1.3.18",
        "deadline7"
    ],
    "launcher": "maya"
}

```
``maya/avatar7.json``
```
#!json

{
    "name": "Avatar 7",
    "extends": ["maya", "2015"],
    "requires": [
        "cortex2.0.1"
    ]
}

```

Will render as:
```
#!json

{
    "name": "Avatar 7",
    "requires": [
        "maya2015",
        "mtoa1.2.1.0",
        "yeti1.3.18",
        "deadline7",
        "cortex2.0.1"
    ],
    "launcher": "maya"
}

```

- - -
**Tab autocompletion**

Enable autocompletion on tab press for presets.