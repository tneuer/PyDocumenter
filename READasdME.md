# Documenter

## TODO

### Backend

- ~~Add Start and End line number for codeblocks~~
- ~~Add Line number for comments~~
- ~~Add method functionalities~~
- ~~Append Docstring~~
- ~~multiline function and class header~~
  - ~~Extract (~~
  - ~~Extract center~~
  - ~~Extract )~~
- ~~Dokumentation~~
- ~~Markdown representation~~
- Staticmehtod, classmethod, wrappers
- Fails if last thing in fail is class (instead of code or function)

### Frontend

- ~~Multiple text windows (~3) side by side~~

- Maximum of twelve input files (12 possible columns)

- Style class buttons, better format

- add userManual
  - only works for python files without syntax error
  - Dependencies, usage,...
  - 12 module tops with 15 classes and functions each
  - add graph legend (LoC = Lines of code,...)

- add search window

- ~~append to README or convert to markdown.~~

- ~~save button for every tab~~

- ~~adding of new modules bugfix~~





  # OVERVIEW

Following descriptions are provided:
1. [Module: documenter\_backend.py](#module:-----documenter\_backend.py)
2. [Module: documenter\_frontend.py](#module:-----documenter\_frontend.py)


# Module:     documenter\_backend.py

This module contains:
- 2 [Classes](#classes-of-documenter\_backend.py)
- 0 [Functions](#functions-of-documenter\_backend.py)

| General                      | Value|
| ---------------------------- | ---- |
| Lines of Code (LoC)          | 0966 |
| Lines of documentation (LoD) | 0306 |
| Empty lines (LoN)            | 0139 |
| Number of classes (NoC)      | 0002 |
| Number of functions (NoF)    | 0000 |

## Documentation

|3|"""
|4|    # Author : Thomas Neuer (tneuer)
|5|    # File Name : class_diagram_backend.py
|6|    # Creation Date : Mit 10 Okt 2018 12:54:42 CEST
|7|    # Last Modified : Son 21 Okt 2018 14:15:24 CEST
|8|    # Description : Construct a file tree of connections between modules, classes and
|9|                    functions. Information about every function and class is given. The output dictionary of the first
|10|                    core functionality "parse_file(f)" has the following structure per file "f":
|11|                    {"Classes":
|12|                        { *Class1*:
|13|                            { "Atrributes":
|14|                                { *Attribute1*, *Attribute2*, ...,},
|15|                              "Methods":
|16|                                { *Method1*:
|17|                                    { "Arguments":
|18|                                        [ [Arg1, Default1], [Arg2, Default2], ...],
|19|                                      "Doc" : *docstring*,
|20|                                      "General":
|21|                                        {"Start": *nr*, "End": *nr*, "LoC", *nr*, "LoD": *nr*, "LoN": *nr*},
|22|                                      "Returns" :
|23|                                        [Return1, Return2, ...]
|24|                                    }
|25|                                  *Method2*:
|26|                                    {
|27|                                    ...
|28|                                    }
|29|                                  }
|30|                              "Doc" : *docstring*,
|31|                              "General" :
|32|                                {"Start": *nr*, "End": *nr*, "LoC", *nr*, "LoD": *nr*, "LoN": *nr*},
|33|                              "Inheritance": [Inher1, Inher2, ...]
|34|                            },
|35|                          *Class2*:
|36|                          {
|37|                          ...
|38|                          },
|39|                     "Functions":
|40|                        { *Function1*:
|41|                            { "Arguments":
|42|                                [ [Arg1, Default1], [Arg2, Default2], ...],
|43|                              "Doc" : *docstring*,
|44|                              "General":
|45|                                {"Start": *nr*, "End": *nr*, "LoC", *nr*, "LoD": *nr*, "LoN": *nr*},
|46|                              "Returns" :
|47|                                [ [Return1], [Return2], ...]
|48|                            }
|49|                        },
|50|                     "General":
|51|                        {'LoC': *nr*, 'LoD': *nr*, 'LoN': *nr*, 'NoC': *nr*, 'NoF': *nr*},
|52|                     "Imports":
|53|                        [ [*pack1*, *as*, *ClassOrFunction*], [...], ... ],
|54|                     "Doc": *docstring*,
|55|                     "Modulename": *modulename*
|56|                    }
|57|
|58|        As one can see this result would be "convertible" to .json.
|59|
|60|"""



## Imports

Following packages are imported:

| Package                          | Imported as      | Imported objects                    |
| -------------------------------- | ---------------- | ----------------------------------- |
| re                               | -                | -                                   |
| pprint                           | -                | pprint                              |


# Classes of documenter\_backend.py
This module contains following classes:
1. [FileParser                               (560, 126)](#Class:-----fileparser)
2. [MarkdownConverter                        (318, 117)](#Class:-----markdownconverter)




#### Class:     FileParser

Jump to:
- [Methods](#methods-of-fileparser)
- [Attributes](#attributes-of-fileparser)

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0067 |
| End line (End)               | 0628 |
| Lines of Code (LoC)          | 0560 |
| Lines of documentation (LoD) | 0126 |
| Empty lines (LoN)            | 0069 |
| Number of methods            | 0026 |
| Number of Attributes         | 0001 |
| Number of parents            | 0001 |

##### Documentation

|68|    """ Manages all file (module) information.
|69|
|70|    The result is in json format.
|71|
|72|    A lot of information is used from a file (module), e.g.:
|73|        - Lines of code
|74|        - (Number of) Classes
|75|        - (Number of) Functions
|76|        - Lines per class / function
|77|        - Lines of documentation
|78|        - Imported libraries
|79|    """



##### Inheritance

This class inherits from:



##### Methods of FileParser

This class contains following methods:

1. [\_\_init\_\_](#method:-----\_\_init\_\_)
2. [parse\_file](#method:-----parse\_file)
3. [is\_empty](#method:-----is\_empty)
4. [is\_comment](#method:-----is\_comment)
5. [contains\_docstring\_call](#method:-----contains\_docstring\_call)
6. [is\_import](#method:-----is\_import)
7. [contains\_class\_header](#method:-----contains\_class\_header)
8. [contains\_function\_header](#method:-----contains\_function\_header)
9. [is\_block\_end](#method:-----is\_block\_end)
10. [is\_method\_block\_end](#method:-----is\_method\_block\_end)
11. [is\_input\_end](#method:-----is\_input\_end)
12. [contains\_attribute](#method:-----contains\_attribute)
13. [contains\_method](#method:-----contains\_method)
14. [contains\_returns](#method:-----contains\_returns)
15. [extract\_file\_name](#method:-----extract\_file\_name)
16. [extract\_class\_name](#method:-----extract\_class\_name)
17. [extract\_import\_info](#method:-----extract\_import\_info)
18. [extract\_function\_name](#method:-----extract\_function\_name)
19. [extract\_between\_brackets](#method:-----extract\_between\_brackets)
20. [extract\_arguments\_keywords\_and\_defaults](#method:-----extract\_arguments\_keywords\_and\_defaults)
21. [extract\_attribute](#method:-----extract\_attribute)
22. [extract\_return\_values](#method:-----extract\_return\_values)
23. [extract\_function\_name\_and\_arguments](#method:-----extract\_function\_name\_and\_arguments)
24. [extract\_first\_line\_input](#method:-----extract\_first\_line\_input)
25. [extract\_center\_line\_input](#method:-----extract\_center\_line\_input)
26. [extract\_last\_line\_input](#method:-----extract\_last\_line\_input)
#### Method:     \_\_init\_\_

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0080 |
| End line (End)               | 0083 |
| Lines of Code (LoC)          | 0002 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0001 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |

##### Returns

#### Method:     parse\_file

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0083 |
| End line (End)               | 0396 |
| Lines of Code (LoC)          | 0312 |
| Lines of documentation (LoD) | 0067 |
| Empty lines (LoN)            | 0040 |

##### Documentation

|84|        """ Get functions, classes, docstrings and imports from a module.
|85|
|86|        Parses the code file content for methods, functions, attributes and classes. The python code is NOT checked for
|87|        correct syntax. If weird syntax occurs, well behaved functionality is not guaranteed.
|88|
|89|        Following information is colleceted:
|90|            - General:
|91|                - Lines of Code (LoC)
|92|                - Lines of Documentation (LoD)
|93|                - Empty Lines (LoN)
|94|                - Number of classes
|95|                - Number of functions
|96|            - Classes:
|97|                - Inheritance
|98|                - Docstring
|99|                - Methods
|100|                - Attributes
|101|                - Lines of code info
|102|                - Number of methods
|103|                - Number of attributes
|104|            - Method:
|105|                - Docstring
|106|                - Arguments
|107|                - Returns
|108|                - Lines of code info
|109|                - Number of arguments
|110|            - Imports:
|111|                - names
|112|                - imported as
|113|                - imported functions/classes
|114|
|115|        Parameters
|116|        ----------
|117|        f : List
|118|            Python file.
|119|
|120|        Returns
|121|        -------
|122|        moduleInfo : str
|123|            Containing all relevant information about the module. See above for structure.
|124|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| f                              |                                |

##### Returns

- Return 1:  moduleInfo
#### Method:     is\_empty

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0396 |
| End line (End)               | 0405 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|397|        """ Regexp: "^\s*$"
|398|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     is\_comment

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0405 |
| End line (End)               | 0414 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|406|        """ Regexp: "^\s*#"
|407|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     contains\_docstring\_call

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0414 |
| End line (End)               | 0423 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0001 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     is\_import

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0423 |
| End line (End)               | 0432 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|424|        """ Regexp: "(^\s*import\s)|(^\s*from\s)"
|425|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     contains\_class\_header

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0432 |
| End line (End)               | 0441 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|433|        """ Regexp: "^class "
|434|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     contains\_function\_header

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0441 |
| End line (End)               | 0450 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|442|        """ Regexp: "^def"
|443|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     is\_block\_end

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0450 |
| End line (End)               | 0459 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|451|        """ Regexp: "^\w+"
|452|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     is\_method\_block\_end

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0459 |
| End line (End)               | 0468 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|460|        """ Regexp: "(^    \w+)|(^\w+)"
|461|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     is\_input\_end

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0468 |
| End line (End)               | 0477 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|469|        """ Regexp: "\)"
|470|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     contains\_attribute

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0477 |
| End line (End)               | 0487 |
| Lines of Code (LoC)          | 0009 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|478|        """ Regexp: "self\.\w+\(?"
|479|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     contains\_method

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0487 |
| End line (End)               | 0496 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|488|        """ Regexp: "^    def "
|489|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     contains\_returns

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0496 |
| End line (End)               | 0505 |
| Lines of Code (LoC)          | 0008 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|497|        """ Regexp: "^\s*return "
|498|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  True
- Return 2:  False
#### Method:     extract\_file\_name

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0505 |
| End line (End)               | 0513 |
| Lines of Code (LoC)          | 0007 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|506|        """ Regexp: "\w*\.py"
|507|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| f                              |                                |

##### Returns

- Return 1:  filename
#### Method:     extract\_class\_name

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0513 |
| End line (End)               | 0521 |
| Lines of Code (LoC)          | 0007 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|514|        """ Regexp: "(?<=class )\w+"
|515|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  classname
#### Method:     extract\_import\_info

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0521 |
| End line (End)               | 0541 |
| Lines of Code (LoC)          | 0019 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|522|        """ Regexp: "((?<=^import )\w+)|((?<=^from )\w+)"; "(?<= as )\w+"; "(?<= import )\w+.*"
|523|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  [import_name  &  import_as  &  import_from]
#### Method:     extract\_function\_name

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0541 |
| End line (End)               | 0549 |
| Lines of Code (LoC)          | 0007 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|542|        """ Regexp: "(?<=def )\w+"
|543|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  functionname
#### Method:     extract\_between\_brackets

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0549 |
| End line (End)               | 0559 |
| Lines of Code (LoC)          | 0009 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|550|        """ Regexp: "\(.*\)"
|551|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  m.group(0)[1:-1]
- Return 2:  "multiline_input"
#### Method:     extract\_arguments\_keywords\_and\_defaults

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0559 |
| End line (End)               | 0569 |
| Lines of Code (LoC)          | 0009 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|560|        """ Regexp: ",\s*"; "\s*=\s*"
|561|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  arguments
#### Method:     extract\_attribute

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0569 |
| End line (End)               | 0576 |
| Lines of Code (LoC)          | 0006 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|570|        """ Regexp: "(?<=self\.)\w+"
|571|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  attribute
#### Method:     extract\_return\_values

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0576 |
| End line (End)               | 0583 |
| Lines of Code (LoC)          | 0006 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|577|        """ Regexp: "(?<=return ).*"
|578|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  ret
#### Method:     extract\_function\_name\_and\_arguments

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0583 |
| End line (End)               | 0593 |
| Lines of Code (LoC)          | 0009 |
| Lines of documentation (LoD) | 0003 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|584|        """ Wrapper around extract_function_name(), extract_between_brackets()
|585|        and extract_arguments_keywords_and_defaults()
|586|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  f_name  &  arguments
#### Method:     extract\_first\_line\_input

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0593 |
| End line (End)               | 0604 |
| Lines of Code (LoC)          | 0010 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|594|        """ Regexp: "(\(.*(?=#))|(\(.*)"
|595|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  arguments
- Return 2:  []
#### Method:     extract\_center\_line\_input

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0604 |
| End line (End)               | 0616 |
| Lines of Code (LoC)          | 0011 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0002 |

##### Documentation

|605|        """ Regexp: ".*(?=#)|(.*)"
|606|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  arguments
- Return 2:  []
#### Method:     extract\_last\_line\_input

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0616 |
| End line (End)               | 0628 |
| Lines of Code (LoC)          | 0011 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0002 |

##### Documentation

|617|        """ Regexp: ".*\)"
|618|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| line                           |                                |

##### Returns

- Return 1:  arguments
- Return 2:  []


##### Attributes of FileParser

A list of the used attributes:

0 moduleInfo; 




#### Class:     MarkdownConverter

Jump to:
- [Methods](#methods-of-markdownconverter)
- [Attributes](#attributes-of-markdownconverter)

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0628 |
| End line (End)               | 0947 |
| Lines of Code (LoC)          | 0318 |
| Lines of documentation (LoD) | 0117 |
| Empty lines (LoN)            | 0057 |
| Number of methods            | 0008 |
| Number of Attributes         | 0001 |
| Number of parents            | 0001 |

##### Documentation

|629|    """ Converts the non-human readable summary of the module into readable markdown format.
|630|    """



##### Inheritance

This class inherits from:



##### Methods of MarkdownConverter

This class contains following methods:

1. [\_\_init\_\_](#method:-----\_\_init\_\_)
2. [convert\_to\_md](#method:-----convert\_to\_md)
3. [convert\_module\_to\_md](#method:-----convert\_module\_to\_md)
4. [convert\_classes\_to\_md](#method:-----convert\_classes\_to\_md)
5. [convert\_functions\_to\_md](#method:-----convert\_functions\_to\_md)
6. [convert\_class\_to\_md](#method:-----convert\_class\_to\_md)
7. [convert\_function\_to\_md](#method:-----convert\_function\_to\_md)
8. [mash\_markdown\_files](#method:-----mash\_markdown\_files)
#### Method:     \_\_init\_\_

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0632 |
| End line (End)               | 0635 |
| Lines of Code (LoC)          | 0002 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0001 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |

##### Returns

#### Method:     convert\_to\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0635 |
| End line (End)               | 0688 |
| Lines of Code (LoC)          | 0052 |
| Lines of documentation (LoD) | 0020 |
| Empty lines (LoN)            | 0010 |

##### Documentation

|636|        """ Converts the input from the FileParser().parse_file(f) to a markdown string.
|637|
|638|        Parameters
|639|        ----------
|640|        parsed_file : Output of the FileParser.parse_file(f) method
|641|        mode : None, "Module", "Method" or "Class" [None]
|642|            "Module" : The whole module/code file is converted to Markdown format. Argument "name" is ignored.
|643|            "Classes": Only classes are converted into Markdown format. Argument "name" is ignored.
|644|            "Methods": Only functions are converted into Markdown format. Argument "name" is ignored.
|645|            "Class": Only a single class is converted to Markdown format. Argument "name" must be provided.
|646|            "Method": Only a single function is converted to Markdown format. Argument "name" must be provided.
|647|        name : str or None [None]
|648|            Only used if "mode"=="Class" or "mode"=="Method". Constructs Markdown file of a single class or function
|649|            indicated by the name of the class or function.
|650|
|651|        Returns
|652|        -------
|653|        mdstring : str
|654|            Markdown format string of the indicated code block.
|655|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| parsed_file                    |                                |
| mode                           | "Module"                       |
| name                           | None                           |

##### Returns

- Return 1:  mdstring
#### Method:     convert\_module\_to\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0688 |
| End line (End)               | 0728 |
| Lines of Code (LoC)          | 0039 |
| Lines of documentation (LoD) | 0012 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|689|        """ Convert a module to a .md file.
|690|
|691|        Parameters
|692|        ----------
|693|        parsed : dict
|694|            parsed information about the module
|695|
|696|        Returns
|697|        -------
|698|        mdstring : str
|699|            Module information as markdown file.
|700|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| parsed                         |                                |

##### Returns

- Return 1:  mdstring
#### Method:     convert\_classes\_to\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0728 |
| End line (End)               | 0762 |
| Lines of Code (LoC)          | 0033 |
| Lines of documentation (LoD) | 0015 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|729|        """ Convert all classes of a module to a .md file.
|730|
|731|        Parameters
|732|        ----------
|733|        parsed : dict
|734|            parsed information about classes
|735|        show_module : bool
|736|            show_module name only for single plotted classes, not when this function is called from within
|737|            a module.md creation function.
|738|
|739|        Returns
|740|        -------
|741|        mdstring : str
|742|            Classes information as markdown file.
|743|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| parsed                         |                                |
| show_module                    |                                |

##### Returns

- Return 1:  mdstring
#### Method:     convert\_functions\_to\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0762 |
| End line (End)               | 0796 |
| Lines of Code (LoC)          | 0033 |
| Lines of documentation (LoD) | 0015 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|763|        """ Convert all functions of a module to a .md file.
|764|
|765|        Parameters
|766|        ----------
|767|        parsed : dict
|768|            parsed information about functions
|769|        show_module : bool
|770|            show_module name only for single plotted functions, not when this function is called from within
|771|            a module.md creation function.
|772|
|773|        Returns
|774|        -------
|775|        mdstring : str
|776|            Methods information as markdown file.
|777|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| parsed                         |                                |
| show_module                    |                                |

##### Returns

- Return 1:  mdstring
#### Method:     convert\_class\_to\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0796 |
| End line (End)               | 0862 |
| Lines of Code (LoC)          | 0065 |
| Lines of documentation (LoD) | 0017 |
| Empty lines (LoN)            | 0009 |

##### Documentation

|797|        """ Convert the information about a single class of a module to a md file.
|798|
|799|        Parameters
|800|        ----------
|801|        parsed : dict
|802|            parsed information about classes
|803|        name : str
|804|            name of the class to be converted
|805|        show_module : bool
|806|            show_module name only for single plotted classes, not when this function is called from within
|807|            a classes.md creation function.
|808|
|809|        Returns
|810|        -------
|811|        mdstring : str
|812|            Class information as markdown file.
|813|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| parsed                         |                                |
| name                           |                                |
| show_module                    | True                           |

##### Returns

- Return 1:  mdstring
#### Method:     convert\_function\_to\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0862 |
| End line (End)               | 0908 |
| Lines of Code (LoC)          | 0045 |
| Lines of documentation (LoD) | 0017 |
| Empty lines (LoN)            | 0005 |

##### Documentation

|863|        """ Convert the information about a single function of a module to a md file.
|864|
|865|        Parameters
|866|        ----------
|867|        parsed : dict
|868|            parsed information about functions
|869|        name : str
|870|            name of the function to be converted
|871|        show_module : bool
|872|            show_module name only for single plotted functions, not when this function is called from within
|873|            a functions.md creation function.
|874|
|875|        Returns
|876|        -------
|877|        mdstring : str
|878|            Method information as markdown file.
|879|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| parsed                         |                                |
| name                           |                                |
| show_module                    | True                           |

##### Returns

- Return 1:  mdstring
#### Method:     mash\_markdown\_files

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0908 |
| End line (End)               | 0947 |
| Lines of Code (LoC)          | 0038 |
| Lines of documentation (LoD) | 0019 |
| Empty lines (LoN)            | 0010 |

##### Documentation

|909|        """ Used to mash markdown texts from individual functions.
|910|
|911|        Mainly called by the frontend to combine informations from different modules or to combine module with each other.
|912|        This function mainly creates the header for these kind of things.
|913|
|914|        Parameters
|915|        ----------
|916|        misc_mds : list
|917|            List of miscellaneous markdown files.
|918|        names : list
|919|            Same length as misc_md. Corresponding names of the functions.
|920|        md_types : list
|921|            Same length as misc_md. Corresponding type of .md file ("Module", "Class", "Method").
|922|
|923|        Returns
|924|        -------
|925|        mdstring : str
|926|            Method information as markdown file.
|927|        """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| self                           |                                |
| misc_mds                       |                                |
| names                          |                                |
| md_types                       |                                |

##### Returns

- Return 1:  mdstring


##### Attributes of MarkdownConverter

A list of the used attributes:

0 module_name; 






# Functions of documenter\_backend.py
This module contains following functions:







# Module:     documenter\_frontend.py

This module contains:
- 0 [Classes](#classes-of-documenter\_frontend.py)
- 27 [Functions](#functions-of-documenter\_frontend.py)

| General                      | Value|
| ---------------------------- | ---- |
| Lines of Code (LoC)          | 1401 |
| Lines of documentation (LoD) | 0505 |
| Empty lines (LoN)            | 0203 |
| Number of classes (NoC)      | 0000 |
| Number of functions (NoF)    | 0027 |

## Documentation

|3|"""
|4|    # Author : Thomas Neuer (tneuer)
|5|    # File Name : class_diagram_frontend.py
|6|    # Creation Date : Son 21 Okt 2018 00:38:41 CEST
|7|    # Last Modified : Mit 24 Okt 2018 00:31:17 CEST
|8|    # Description : Frontend with Dash for code review. As a tutorial this includes:
|9|        - Enabling and disabling of button (Submit)
|10|        - Dynamic creation of button fields (module-, class- and function buttons)
|11|        - Dynamic Textwindows
|12|        - Drag & Drop file parsing
|13|"""
|895|        """ Populate the trigger inputs.
|896|
|897|        If the trigger inputs are filled with a value, the function open_and_close_tab(*args) is called, due to the change
|898|        in the children property of the trigger. Curiously in this version (06.11.2018) the dcc.Input value that is directed
|899|        to the output. e.g. with this function, is NOT the same as the "value" key when looking at dcc.Input().__dict__.
|900|        This "feature/bug" is used here to mark the newly added buttons as "added". So in this function simultaneously two
|901|        value properties of the dcc.Inputs are set. Once via the callback output und once directly within the function body.
|902|        But these two properties are independent.
|903|
|904|        When I tried to let these buttons directly communicate with "tabs"->"children" it did not work, probably because
|905|        the buttons are dynamically created and can't interact with one static output. (06.11.2018)
|906|
|907|        Parameters
|908|        ----------
|909|        clicks : int
|910|            Number of clicks on the corresponding module, class or function button. Serves as trigger.
|911|        idx : str
|912|            Identifier of the pressed buttons with the following format "{1}{2}{3}":
|913|                - {1} : Module number in order of input
|914|                - {2} : Either "Module", "Class" or "Function"
|915|                - {3} : Class or function number within the module in order of appearance, does not exist for modules.
|916|
|917|        Returns
|918|        -------
|919|        idx : same as parameter input
|920|        """



## Imports

Following packages are imported:

| Package                          | Imported as      | Imported objects                    |
| -------------------------------- | ---------------- | ----------------------------------- |
| os                               | -                | -                                   |
| re                               | -                | -                                   |
| dash                             | -                | -                                   |
| time                             | -                | -                                   |
| shutil                           | -                | -                                   |
| base64                           | -                | -                                   |
| datetime                         | -                | -                                   |
| dash_core_components             | dcc              | -                                   |
| dash_html_components             | html             | -                                   |
| textwrap                         | -                | indent, dedent                      |
| dash                             | -                | Input, Output, State                |
| documenter_backend               | -                | FileParser, MarkdownConverter       |


# Classes of documenter\_frontend.py
This module contains following classes:






# Functions of documenter\_frontend.py
This module contains following functions:
1. [update\_dropdown                         (59, 24)](#function:-----update\_dropdown)
2. [update\_text\_content1                   (38, 15)](#function:-----update\_text\_content1)
3. [update\_text\_header1                    (29, 16)](#function:-----update\_text\_header1)
4. [update\_text\_content2                   (25, 2)](#function:-----update\_text\_content2)
5. [update\_text\_header2                    (18, 5)](#function:-----update\_text\_header2)
6. [update\_text\_content3                   (25, 2)](#function:-----update\_text\_content3)
7. [update\_text\_header3                    (18, 5)](#function:-----update\_text\_header3)
8. [enable\_submit\_button                   (24, 13)](#function:-----enable\_submit\_button)
9. [draw\_class\_diagram                     (54, 28)](#function:-----draw\_class\_diagram)
10. [populate\_input\_folder\_with\_files     (31, 16)](#function:-----populate\_input\_folder\_with\_files)
11. [populate\_module\_information            (29, 19)](#function:-----populate\_module\_information)
12. [construct\_Module\_Buttons               (52, 28)](#function:-----construct\_module\_buttons)
13. [construct\_general\_elements             (49, 27)](#function:-----construct\_general\_elements)
14. [construct\_Buttons                       (82, 27)](#function:-----construct\_buttons)
15. [construct\_both                          (48, 22)](#function:-----construct\_both)
16. [open\_and\_close\_tab                    (49, 22)](#function:-----open\_and\_close\_tab)
17. [open\_and\_delete\_tab                   (41, 21)](#function:-----open\_and\_delete\_tab)
18. [switch\_Tab\_on\_click                   (37, 21)](#function:-----switch\_tab\_on\_click)
19. [wait\_for\_module\_information           (6, 0)](#function:-----wait\_for\_module\_information)
20. [display\_information                     (55, 18)](#function:-----display\_information)
21. [enable\_path\_entry\_sct                 (6, 0)](#function:-----enable\_path\_entry\_sct)
22. [enable\_path\_entry\_saat                (6, 0)](#function:-----enable\_path\_entry\_saat)
23. [enable\_path\_entry\_sa                  (11, 0)](#function:-----enable\_path\_entry\_sa)
24. [save\_md\_files                          (112, 33)](#function:-----save\_md\_files)
25. [get\_md\_from\_ID                        (39, 20)](#function:-----get\_md\_from\_id)
26. [create\_new\_md\_file                    (50, 21)](#function:-----create\_new\_md\_file)
27. [append\_to\_readme\_md                   (29, 17)](#function:-----append\_to\_readme\_md)




#### Function:     update\_dropdown

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0294 |
| End line (End)               | 0354 |
| Lines of Code (LoC)          | 0059 |
| Lines of documentation (LoD) | 0024 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|295|    """ Checks input in drag&drop window and adds in to the dropdown.
|296|
|297|    Only python files are added to the dropdown menu.
|298|    The important global variables are:
|299|        - input_filenames : list of the module names
|300|        - input_filecontents : list of the actual code content as a string
|301|    To each input file an integer value is assigned as identifier for other functions. This assignment is directly saved
|302|    in the "value" field of the Dropdown menu.
|303|
|304|    Parameters
|305|    ----------
|306|    contents : str
|307|        Code content of the file which needs to be decoded and parsed.
|308|    filenames : str
|309|        Module names.
|310|
|311|    Returns
|312|    -------
|313|    drpdwn : dcc.Dropdown()
|314|        Updated dropdown menu with input filenames.
|315|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| contents                       |                                |
| filenames                      |                                |

##### Returns

- Return 1:  drpdwn



#### Function:     update\_text\_content1

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0354 |
| End line (End)               | 0393 |
| Lines of Code (LoC)          | 0038 |
| Lines of documentation (LoD) | 0015 |
| Empty lines (LoN)            | 0004 |

##### Documentation

|355|    """ Update the code revie text block with the code of the last entered file.
|356|
|357|    Take the code content of the last entered file and append line numbers. Then print this for the user.
|358|
|359|    Parameters
|360|    ----------
|361|    selected_options : list
|362|        List of integer values, each corresponding to a certain file as assigned by the function
|363|        update_dropdown(*args, **kwargs). The last one of those is then chosen and line numbers are inserted.
|364|
|365|    Returns
|366|    -------
|367|    textwindow : dcc.Textarea
|368|        Contains the code including the line numbers
|369|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| selected_options               |                                |

##### Returns

- Return 1:  textwindow



#### Function:     update\_text\_header1

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0393 |
| End line (End)               | 0423 |
| Lines of Code (LoC)          | 0029 |
| Lines of documentation (LoD) | 0016 |
| Empty lines (LoN)            | 0005 |

##### Documentation

|394|    """ Updates the header of the code rewiev block.
|395|
|396|    Parameters
|397|    ----------
|398|    selected_options : list
|399|        List of integer values, each corresponding to a certain file as assigned by the function
|400|        update_dropdown(*args, **kwargs). The last one of those is then chosen and line numbers are inserted.
|401|
|402|    Returns
|403|    -------
|404|    shown_text : str
|405|        Name of the latest file to be printed as header for the code review field.
|406|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| selected_options               |                                |

##### Returns

- Return 1:  shown_text



#### Function:     update\_text\_content2

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0423 |
| End line (End)               | 0449 |
| Lines of Code (LoC)          | 0025 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|424|    """ Same as in update_text_content1(*args, **kwargs), but with second last code file.
|425|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| selected_options               |                                |

##### Returns

- Return 1:  textwindow



#### Function:     update\_text\_header2

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0449 |
| End line (End)               | 0468 |
| Lines of Code (LoC)          | 0018 |
| Lines of documentation (LoD) | 0005 |
| Empty lines (LoN)            | 0003 |

##### Documentation

|450|    """ As in update_text_header1(*args, **kwargs)
|451|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| selected_options               |                                |

##### Returns

- Return 1:  shown_text



#### Function:     update\_text\_content3

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0468 |
| End line (End)               | 0494 |
| Lines of Code (LoC)          | 0025 |
| Lines of documentation (LoD) | 0002 |
| Empty lines (LoN)            | 0001 |

##### Documentation

|469|    """ Same as in update_text_content1(*args, **kwargs), but with second last code file.
|470|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| selected_options               |                                |

##### Returns

- Return 1:  textwindow



#### Function:     update\_text\_header3

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0494 |
| End line (End)               | 0513 |
| Lines of Code (LoC)          | 0018 |
| Lines of documentation (LoD) | 0005 |
| Empty lines (LoN)            | 0003 |

##### Documentation

|495|    """ As in update_text_header1(*args, **kwargs)
|496|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| selected_options               |                                |

##### Returns

- Return 1:  shown_text



#### Function:     enable\_submit\_button

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0513 |
| End line (End)               | 0538 |
| Lines of Code (LoC)          | 0024 |
| Lines of documentation (LoD) | 0013 |
| Empty lines (LoN)            | 0004 |

##### Documentation

|514|    """ Enables the submit button if files have been added.
|515|
|516|    Parameters
|517|    ----------
|518|    value : list
|519|        List of integer values, each corresponding to a certain file as assigned by the function
|520|        update_dropdown(*args, **kwargs).
|521|
|522|    Returns
|523|    -------
|524|    bool :
|525|        True if files have been added, else false.
|526|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| value                          |                                |

##### Returns

- Return 1:  True
- Return 2:  False



#### Function:     draw\_class\_diagram

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0538 |
| End line (End)               | 0593 |
| Lines of Code (LoC)          | 0054 |
| Lines of documentation (LoD) | 0028 |
| Empty lines (LoN)            | 0008 |

##### Documentation

|539|    """ Core functionality which combines most of the other core functions.
|540|
|541|    Takes the selected values from the dropdown menu for the module names and converts those into a interactive diagram
|542|    with moduleinformation like lines of code, functions and classes.
|543|    The global variables are:
|544|        - input_filenames : Module names ending with .py
|545|        - buttons : filled with the buttons for the functions and classes later on
|546|        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
|547|
|548|    Parameters
|549|    ----------
|550|    n_clicks : int
|551|        Number of times clicked on the submit button.
|552|    drawComponents : list
|553|        Determines which information is shown. Possibel are:
|554|            - "GENERAL": General information of module like LinesOfCode, LinesOfDocumentation & LinesOfNothing (empty)
|555|            - "CLASSES": Classes of the module are shown
|556|            - "FUNCTIONS": Functions of the module are shown
|557|    inputfiles : list
|558|        List of integer values, each corresponding to a certain file as assigned by the function
|559|        update_dropdown(*args, **kwargs).
|560|
|561|    Returns
|562|    -------
|563|    c_diagram : list
|564|        List of html divisions containing the newly created buttons for the modules, functions and classes.
|565|
|566|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| n_clicks                       |                                |
| drawComponents                 |                                |
| inputfiles                     |                                |

##### Returns

- Return 1:  c_diagram



#### Function:     populate\_input\_folder\_with\_files

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0593 |
| End line (End)               | 0625 |
| Lines of Code (LoC)          | 0031 |
| Lines of documentation (LoD) | 0016 |
| Empty lines (LoN)            | 0005 |

##### Documentation

|594|    """ Saves the currently used files into a TEMPORARY folder within the working directory.
|595|    The global variables are:
|596|        - input_filenames : Module names ending with .py
|597|        - input_filecontents : list of the actual code content as a string
|598|
|599|    Parameters
|600|    ----------
|601|    values : list
|602|        List of integer values, each corresponding to a certain file as assigned by the function
|603|        update_dropdown(*args, **kwargs).
|604|
|605|    Returns
|606|    -------
|607|    filepaths : list
|608|        List of strings indicating the filepath to the file content in the TEMPORARY folder.
|609|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| values                         |                                |

##### Returns

- Return 1:  filepaths



#### Function:     populate\_module\_information

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0625 |
| End line (End)               | 0655 |
| Lines of Code (LoC)          | 0029 |
| Lines of documentation (LoD) | 0019 |
| Empty lines (LoN)            | 0006 |

##### Documentation

|626|    """ Interact with the backend, with the parser so to say. Get the information about the parsed code.
|627|
|628|    The global variables are:
|629|        - input_filenames : Module names ending with .py
|630|
|631|    Parameters
|632|    ----------
|633|    values : list
|634|        List of integer values, each corresponding to a certain file as assigned by the function
|635|        update_dropdown(*args, **kwargs).
|636|    filepaths : list
|637|        List of filepaths to the selected code content in the TEMPORARY folder.
|638|
|639|    Returns
|640|    -------
|641|    module_informations : dict
|642|        Dictionary with keys of the module names (e.g. test.py) and the parsed file content. If you are interested in
|643|        the backend and the parsing, see the documentation of class_diagram_backend.py
|644|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| values                         |                                |
| filepaths                      |                                |

##### Returns

- Return 1:  module_informations



#### Function:     construct\_Module\_Buttons

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0655 |
| End line (End)               | 0708 |
| Lines of Code (LoC)          | 0052 |
| Lines of documentation (LoD) | 0028 |
| Empty lines (LoN)            | 0006 |

##### Documentation

|656|    """ Construct the buttons for the module names.
|657|
|658|    This will later call the full documentation of the module with all classes and fucntions.
|659|    The global variables are:
|660|        - input_filenames : Module names ending with .py
|661|        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
|662|        scaling of the 12 possible html columns.
|663|        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
|664|
|665|    Parameters
|666|    ----------
|667|    values : list
|668|        List of integer values, each corresponding to a certain file as assigned by the function
|669|        update_dropdown(*args, **kwargs).
|670|    module_informations : dict
|671|        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
|672|        code file content.
|673|    drawComponents : list
|674|        Determines which information is shown. Possibel are:
|675|            - "GENERAL": General information of module like LinesOfCode, LinesOfDocumentation & LinesOfNothing (empty)
|676|            - "CLASSES": Classes of the module are shown
|677|            - "FUNCTIONS": Functions of the module are shown
|678|
|679|    Returns
|680|    -------
|681|    module_buttons : html.Div
|682|        HTML division containing all buttons for the module properly scaled, side by side.
|683|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| values                         |                                |
| module_informations            |                                |
| drawComponents                 |                                |

##### Returns

- Return 1:  module_buttons



#### Function:     construct\_general\_elements

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0708 |
| End line (End)               | 0758 |
| Lines of Code (LoC)          | 0049 |
| Lines of documentation (LoD) | 0027 |
| Empty lines (LoN)            | 0006 |

##### Documentation

|709|    """ Construct the general information about the code file content.
|710|
|711|    General information contains:
|712|        - LoC (Lines of Code) : Total number of rows in code file
|713|        - LoD (Lines of Documentaion) : Number of documentation-ONLY columns. This includes multiple line comments as
|714|                                        well as single line comments via "#", but only if no executable code is also
|715|                                        present on the line.
|716|        - LoN (Lines of Nothing) : Empty lines or only white spaces. Also the empty lines within documentations are counted
|717|    The global variables are:
|718|        - input_filenames : Module names ending with .py
|719|        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
|720|        scaling of the 12 possible html columns.
|721|
|722|    Parameters
|723|    ----------
|724|    values : list
|725|        List of integer values, each corresponding to a certain file as assigned by the function
|726|        update_dropdown(*args, **kwargs).
|727|    module_informations : dict
|728|        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
|729|        code file content.
|730|
|731|    Returns
|732|    -------
|733|    general_elements : html.Div
|734|        HTML division containing all the general information about a module located below the module name.
|735|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| values                         |                                |
| module_informations            |                                |

##### Returns

- Return 1:  general_elements



#### Function:     construct\_Buttons

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0758 |
| End line (End)               | 0841 |
| Lines of Code (LoC)          | 0082 |
| Lines of documentation (LoD) | 0027 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|759|    """ Construct the class and function buttons to trigger the tab opening.
|760|
|761|    The global variables are:
|762|        - input_filenames : Module names ending with .py
|763|        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
|764|        scaling of the 12 possible html columns.
|765|        - buttons : List to be filled with the available buttons for modules, classes and functions.
|766|        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
|767|
|768|    Parameters
|769|    ----------
|770|    values : list
|771|        List of integer values, each corresponding to a certain file as assigned by the function
|772|        update_dropdown(*args, **kwargs).
|773|    module_informations : dict
|774|        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
|775|        code file content.
|776|    key : "Class" or "Function"
|777|        Indicates if a function header or class header should be used. Also responsible for button binding naming.
|778|    mode : "both" or None [None]
|779|        If "both" only half the width of the module width is used. One half is for class buttons, the other for function buttons.
|780|
|781|    Returns
|782|    -------
|783|    buttons : html.Div
|784|        Containing all the class or function buttons used for later interaction.
|785|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| values                         |                                |
| module_informations            |                                |
| key                            |                                |
| mode                           | None                           |

##### Returns

- Return 1:  column
- Return 2:  buttons



#### Function:     construct\_both

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0841 |
| End line (End)               | 0890 |
| Lines of Code (LoC)          | 0048 |
| Lines of documentation (LoD) | 0022 |
| Empty lines (LoN)            | 0010 |

##### Documentation

|842|    """ Construct both class and function buttons to trigger the tab opening.
|843|
|844|    Basically a wrapper around construct_buttons twice (once with key="Class", the other with key="Function").
|845|    The global variables are:
|846|        - input_filenames : Module names ending with .py
|847|        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
|848|        scaling of the 12 possible html columns.
|849|
|850|    Parameters
|851|    ----------
|852|    values : list
|853|        List of integer values, each corresponding to a certain file as assigned by the function
|854|        update_dropdown(*args, **kwargs).
|855|    module_informations : dict
|856|        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
|857|        code file content.
|858|
|859|    Returns
|860|    -------
|861|    class_and_function_buttons : html.Div
|862|        HTML division containing the class and function buttons per module side by side.
|863|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| values                         |                                |
| module_informations            |                                |

##### Returns

- Return 1:  class_and_function_buttons



#### Function:     open\_and\_close\_tab

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0932 |
| End line (End)               | 0982 |
| Lines of Code (LoC)          | 0049 |
| Lines of documentation (LoD) | 0022 |
| Empty lines (LoN)            | 0009 |

##### Documentation

|933|    """ Create a dropdown menu for clicked buttons.
|934|
|935|    This dropwdown menu communicates with the tabs divison and tells the tabs div which tabs should currently be
|936|    displayed.
|937|    The global variables are:
|938|        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
|939|
|940|    Parameters
|941|    ----------
|942|    args : list
|943|        List of identifiers of the pressed buttons with the following format "{1}{2}{3}":
|944|                - {1} : Module number in order of input
|945|                - {2} : Either "Module", "Class" or "Function"
|946|                - {3} : Class or function number within the module in order of appearance, does not exist for modules.
|947|
|948|    Returns
|949|    -------
|950|    drpdwn : dxx.Dropdown
|951|        Updated dropdown menu for code block inspection. The ones which are deleted are set to None again by the function
|952|        switch_Tab_on_click().
|953|
|954|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| *args                          |                                |

##### Returns

- Return 1:  drpdwn



#### Function:     open\_and\_delete\_tab

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 0982 |
| End line (End)               | 1024 |
| Lines of Code (LoC)          | 0041 |
| Lines of documentation (LoD) | 0021 |
| Empty lines (LoN)            | 0009 |

##### Documentation

|983|    """ Opens and closes tabs.
|984|
|985|    The global variables are:
|986|        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
|987|        - TABDICT : dictonary of all tabs where the identifiers are the keys and the tabs are the values.
|988|        - PREVIOUS_TABS : The tabs previously selected. Used for filtering out the deleted tabs.
|989|
|990|    Parameters
|991|    ----------
|992|    available_tabs : list
|993|        List of identifiers of the pressed buttons with the following format "{1}{2}{3}":
|994|                - {1} : Module number in order of input
|995|                - {2} : Either "Module", "Class" or "Function"
|996|                - {3} : Class or function number within the module in order of appearance, does not exist for modules.
|997|
|998|    Returns
|999|    -------
|1000|    tabs : list
|1001|        List of tabs available for selection
|1002|
|1003|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| available_tabs                 |                                |

##### Returns

- Return 1:  tabs



#### Function:     switch\_Tab\_on\_click

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1024 |
| End line (End)               | 1062 |
| Lines of Code (LoC)          | 0037 |
| Lines of documentation (LoD) | 0021 |
| Empty lines (LoN)            | 0008 |

##### Documentation

|1025|    """ Deals with tab switching and updating.
|1026|
|1027|    If a new ta is opened, this one should be visible to the user.
|1028|    If the current visible tab is closed, the home tab is headed for.
|1029|    If some tab is closed the system should remain in the current position.
|1030|
|1031|    Parameters
|1032|    ----------
|1033|    available_tabs : list
|1034|        List of identifiers of the pressed buttons with the following format "{1}{2}{3}":
|1035|            - {1} : Module number in order of input
|1036|            - {2} : Either "Module", "Class" or "Function"
|1037|            - {3} : Class or function number within the module in order of appearance, does not exist for modules.
|1038|    currently_selected_tab : str
|1039|        Identifier of currently open tab
|1040|
|1041|    Returns
|1042|    -------
|1043|    go_to_tab : str
|1044|        Identifier to the next tab
|1045|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| available_tabs                 |                                |
| currently_selected_tab         |                                |

##### Returns

- Return 1:  go_to_tab



#### Function:     wait\_for\_module\_information

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1062 |
| End line (End)               | 1069 |
| Lines of Code (LoC)          | 0006 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0002 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| clicks                         |                                |

##### Returns

- Return 1:  "Unused"



#### Function:     display\_information

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1069 |
| End line (End)               | 1125 |
| Lines of Code (LoC)          | 0055 |
| Lines of documentation (LoD) | 0018 |
| Empty lines (LoN)            | 0012 |

##### Documentation

|1070|    """ Get the necessary information for the clicked block from the backend.
|1071|
|1072|    The global variables are:
|1073|        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
|1074|
|1075|    Parameters
|1076|    ----------
|1077|    tab : str
|1078|        Identifier for the selected method.
|1079|        tab[0] := module number
|1080|        tab[1:-1] := "Module", "Class" or "Function"
|1081|        tab[-1] := Class or function number
|1082|
|1083|    Returns
|1084|    -------
|1085|    tab_content : dcc.Markdown
|1086|        Markdown environment containing the information about the selected tab.
|1087|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| tab                            |                                |
| unused_trigger                 |                                |

##### Returns

- Return 1:  markdown
- Return 2:  markdown



#### Function:     enable\_path\_entry\_sct

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1125 |
| End line (End)               | 1132 |
| Lines of Code (LoC)          | 0006 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0000 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| value                          |                                |

##### Returns

- Return 1:  False
- Return 2:  True



#### Function:     enable\_path\_entry\_saat

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1132 |
| End line (End)               | 1139 |
| Lines of Code (LoC)          | 0006 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0000 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| value                          |                                |

##### Returns

- Return 1:  False
- Return 2:  True



#### Function:     enable\_path\_entry\_sa

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1139 |
| End line (End)               | 1151 |
| Lines of Code (LoC)          | 0011 |
| Lines of documentation (LoD) | 0000 |
| Empty lines (LoN)            | 0002 |

##### Documentation

_No documentation available_

##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| value                          |                                |

##### Returns

- Return 1:  False
- Return 2:  True



#### Function:     save\_md\_files

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1151 |
| End line (End)               | 1264 |
| Lines of Code (LoC)          | 0112 |
| Lines of documentation (LoD) | 0033 |
| Empty lines (LoN)            | 0016 |

##### Documentation

|1152|    """
|1153|
|1154|    Parameters
|1155|    ----------
|1156|    clicks : int
|1157|        Number of clicks on the save button. Serves as trigger for saving.
|1158|    options : list
|1159|        Corresponds to the save options:
|1160|            - sct : save current tab
|1161|            - saat : save all active tabs
|1162|            - sa : save all tabs
|1163|    fmode : list
|1164|        Can be "readme", "new" or both. Determines if appended to a README.md file in the current folder path or a new
|1165|        .md file is created. If README.md does not exits it is created.
|1166|    path_curr : str
|1167|        Path where the currently open tab should be saved if options contains "sct".
|1168|    path_active : str
|1169|        Path where all the active tabs should be saved if options contains "saat".
|1170|    path_all : str
|1171|        Path where all module should be saved if options contains "sa".
|1172|    tab_curr : str
|1173|        Identifier of the currently selected tab.
|1174|    tab_active : list
|1175|        List of tab objects containing among other things the identifier of the module, class or function
|1176|
|1177|    Returns
|1178|    -------
|1179|    exitcode : str
|1180|        Confim message if all files could be saved, else explanatory merror message.
|1181|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| clicks                         |                                |
| option                         |                                |
| fmode                          |                                |
| path_curr                      |                                |
| path_active                    |                                |
| path_all                       |                                |
| tab_curr                       |                                |
| tab_active                     |                                |

##### Returns

- Return 1:  "Nothing  &  done  &  yet"
- Return 2:  ret_message



#### Function:     get\_md\_from\_ID

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1264 |
| End line (End)               | 1304 |
| Lines of Code (LoC)          | 0039 |
| Lines of documentation (LoD) | 0020 |
| Empty lines (LoN)            | 0010 |

##### Documentation

|1265|    """ Get the markdown text and function name from the identifier.
|1266|
|1267|    Interacts with the MarkdownConverter of the backend.
|1268|
|1269|    Parameters
|1270|    ----------
|1271|    idx : str
|1272|        Identifier of the module, class or function with the following form:
|1273|            idx[0] := module number
|1274|            idx[1:-1] := "Module", "Class" or "Function"
|1275|            idx[-1] := Class or function number
|1276|
|1277|    Returns
|1278|    -------
|1279|    fname : str
|1280|        Name of the module, class or function. Only used if the filepath is a directory.
|1281|    tab_md : str
|1282|        String of the markdown description of the module, class or function
|1283|
|1284|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| idx                            |                                |

##### Returns

- Return 1:  fname  &  tab_md



#### Function:     create\_new\_md\_file

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1304 |
| End line (End)               | 1355 |
| Lines of Code (LoC)          | 0050 |
| Lines of documentation (LoD) | 0021 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|1305|    """ Create the new .md file and deal with false user input.
|1306|
|1307|    If the path is a directory a descriptive name is chosen, e.g for a class:
|1308|            Class_*classname*_*currentDate.
|1309|    If the given path leads into a directory but with a filename, then this name is given to the class and if needed, a
|1310|    .md extension is attached.
|1311|
|1312|    Parameters
|1313|    ----------
|1314|    path :  str
|1315|        Directory or full path with filename. If it is a directory a generic name for the markdown text is given.
|1316|    md_text : str
|1317|        Description in markdown format
|1318|    fname : str
|1319|        Name of the module, class or function
|1320|
|1321|    Returns
|1322|    -------
|1323|    exitcode : str
|1324|        If all good empty string "" is returned, else a descriptive errormessage is returned.
|1325|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| path                           |                                |
| md_text                        |                                |
| fname                          |                                |

##### Returns

- Return 1:  exitcode+"\n"  &  path+"\n"



#### Function:     append\_to\_readme\_md

| General                      | Value|
| ---------------------------- | ---- |
| Start line (Start)           | 1355 |
| End line (End)               | 1385 |
| Lines of Code (LoC)          | 0029 |
| Lines of documentation (LoD) | 0017 |
| Empty lines (LoN)            | 0007 |

##### Documentation

|1356|    """ Append description to README.md file.
|1357|
|1358|    The longest possible path to a directiory is selected from the path. There the description of the file is attached
|1359|    to the README.md or a new one is created.
|1360|
|1361|    Parameters
|1362|    ----------
|1363|    path :  str
|1364|        Directory or full path with filename. If it is a directory a generic name for the markdown text is given.
|1365|    md_text : str
|1366|        Description in markdown format
|1367|
|1368|    Returns
|1369|    -------
|1370|    exitcode : str
|1371|        If all good empty string "" is returned, else a descriptive errormessage is returned.
|1372|    """


##### Arguments

| Arguments                      | Default                        |
| -------------------------------| ------------------------------ |
| path                           |                                |
| md_text                        |                                |

##### Returns

- Return 1:  exitcode+"\n"  &  path+"\n"






