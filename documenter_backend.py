#!/home/thomas/anaconda3/bin/python

"""
    # Author : Thomas Neuer (tneuer)
    # File Name : class_diagram_backend.py
    # Creation Date : Mit 10 Okt 2018 12:54:42 CEST
    # Last Modified : Son 21 Okt 2018 14:15:24 CEST
    # Description : Construct a file tree of connections between modules, classes and
                    functions. Information about every function and class is given. The output dictionary of the first
                    core functionality "parse_file(f)" has the following structure per file "f":
                    {"Classes":
                        { *Class1*:
                            { "Atrributes":
                                { *Attribute1*, *Attribute2*, ...,},
                              "Methods":
                                { *Method1*:
                                    { "Arguments":
                                        [ [Arg1, Default1], [Arg2, Default2], ...],
                                      "Doc" : *docstring*,
                                      "General":
                                        {"Start": *nr*, "End": *nr*, "LoC", *nr*, "LoD": *nr*, "LoN": *nr*},
                                      "Returns" :
                                        [Return1, Return2, ...]
                                    }
                                  *Method2*:
                                    {
                                    ...
                                    }
                                  }
                              "Doc" : *docstring*,
                              "General" :
                                {"Start": *nr*, "End": *nr*, "LoC", *nr*, "LoD": *nr*, "LoN": *nr*},
                              "Inheritance": [Inher1, Inher2, ...]
                            },
                          *Class2*:
                          {
                          ...
                          },
                     "Functions":
                        { *Function1*:
                            { "Arguments":
                                [ [Arg1, Default1], [Arg2, Default2], ...],
                              "Doc" : *docstring*,
                              "General":
                                {"Start": *nr*, "End": *nr*, "LoC", *nr*, "LoD": *nr*, "LoN": *nr*},
                              "Returns" :
                                [ [Return1], [Return2], ...]
                            }
                        },
                     "General":
                        {'LoC': *nr*, 'LoD': *nr*, 'LoN': *nr*, 'NoC': *nr*, 'NoF': *nr*},
                     "Imports":
                        [ [*pack1*, *as*, *ClassOrFunction*], [...], ... ],
                     "Doc": *docstring*,
                     "Modulename": *modulename*
                    }

        As one can see this result would be "convertible" to .json.

"""
#==============================================================================

import re

from pprint import pprint

class FileParser():
    """ Manages all file (module) information.

    The result is in json format.

    A lot of information is used from a file (module), e.g.:
        - Lines of code
        - (Number of) Classes
        - (Number of) Functions
        - Lines per class / function
        - Lines of documentation
        - Imported libraries
    """
    def __init__(self):
        self.moduleInfo = {}

    def parse_file(self, f):
        """ Get functions, classes, docstrings and imports from a module.

        Parses the code file content for methods, functions, attributes and classes. The python code is NOT checked for
        correct syntax. If weird syntax occurs, well behaved functionality is not guaranteed.

        Following information is colleceted:
            - General:
                - Lines of Code (LoC)
                - Lines of Documentation (LoD)
                - Empty Lines (LoN)
                - Number of classes
                - Number of functions
            - Classes:
                - Inheritance
                - Docstring
                - Methods
                - Attributes
                - Lines of code info
                - Number of methods
                - Number of attributes
            - Function:
                - Docstring
                - Arguments
                - Returns
                - Lines of code info
                - Number of arguments
            - Imports:
                - names
                - imported as
                - imported functions/classes

        Parameters
        ----------
        f : List
            Python file.

        Returns
        -------
        moduleInfo : str
            Containing all relevant information about the module. See above for structure.
        """

        lineCounter = 0 # Count lines of the total file
        docLineCounter = 0 # Count documentation lines of the total file
        emptyLineCounter = 0 # Count empty lines of the total file
        textBlockLineCounter = 0 # Count lines of a single block (class or function)
        isCurrentlyDoc = False
        isCurrentlyClass = False
        isCurrentlyMethod = False
        isCurrentlyFunction = False
        docString = "" # Saves Docstring of the file
        lineNRFormat = "|{}| " # Later shown in front of the documentation lines

        multiline_input = False # True if a function or class arguments are inserted over multiple lines

        with open(f, "r") as module:
            lines = module.readlines()

        filename = self.extract_file_name(f)

        # Store all the information about the module
        moduleInfo = {"Classes": {}, "Functions": {}, "Imports": [],
                "General": {}, "Doc": ""}

        # Iterate over all lines of the document
        for lnr, line in enumerate(lines):
            lnr = lnr + 1
            lineCounter += 1

            # Check if it a empty line
            if self.is_empty(line):
                emptyLineCounter += 1
                if isCurrentlyClass or isCurrentlyFunction:
                    textBlockEmptyLineCounter += 1
                    if isCurrentlyMethod:
                        methodEmptyLineCounter += 1

            # Record doctring
            if isCurrentlyDoc:
                docLineCounter += 1
                if isCurrentlyClass or isCurrentlyFunction:
                    textBlockDocLineCounter += 1
                    if isCurrentlyMethod:
                        methodDocString += lineNRFormat.format(lnr)
                        methodDocString += line.strip(" ")
                        methodDocLineCounter += 1
                    else:
                        textDocString += lineNRFormat.format(lnr)
                        textDocString += line.strip(" ")
                else:
                    docString += lineNRFormat.format(lnr)
                    docString += line.strip(" ")

                # Docsting call := """, if already inside documentation another call marks the end
                if self.contains_docstring_call(line):
                    isCurrentlyDoc = False

            # Initialize if docstring with call := """
            elif self.contains_docstring_call(line):
                isCurrentlyDoc = True
                docLineCounter += 1
                if isCurrentlyClass or isCurrentlyFunction:
                    textBlockDocLineCounter += 1
                    if isCurrentlyMethod:
                        methodDocLineCounter += 1
                        methodDocString += lineNRFormat.format(lnr)
                        methodDocString += line.strip(" ")
                    else:
                        textDocString += lineNRFormat.format(lnr)
                        textDocString += line.strip(" ")
                else:
                    docString += lineNRFormat.format(lnr)
                    docString += line.strip(" ")

            # Special care if arguments to a method, function or class are distributed over successive lines
            if multiline_input:
                if self.is_input_end(line):
                    arguments = self.extract_last_line_input(line) # End of input marked by ")"
                    multiline_input = False
                else:
                    arguments = self.extract_center_line_input(line)
                if arguments: # Only if arguments are on this line, might also be that there is only documentation
                    if isCurrentlyFunction:
                        moduleInfo["Functions"][f_name]["Arguments"].extend(arguments)
                    elif isCurrentlyMethod:
                        moduleInfo["Classes"][c_name]["Methods"][m_name]["Arguments"].extend(arguments)
                    elif isCurrentlyClass:
                        moduleInfo["Classes"][c_name]["Inheritance"].extend(arguments)

                continue # Do not proceed if it is still an input for the function

            if isCurrentlyMethod:
                methodLineCounter += 1

                # Method end is marked by "^    \w" (four whitespaces and then a letter) or just a letter at the beginning if end of class
                if self.is_method_block_end(line):
                    isCurrentlyMethod = False
                    methodLineCounter -= 1

                    # Method end: append all the collected information to this method
                    moduleInfo["Classes"][c_name]["Methods"][m_name]["General"] = {
                                "LoC": methodLineCounter,
                                "LoD": methodDocLineCounter,
                                "LoN": methodEmptyLineCounter,
                                "Start": moduleInfo["Classes"][c_name]["Methods"][m_name]["General"]["Start"],
                                "End": lnr
                                }
                    moduleInfo["Classes"][c_name]["Methods"][m_name]["Doc"] = methodDocString
                    methodLineCounter = 0

                # Check if the line contains a return value. Note: This does not necessarily mark the end of the method!!
                elif self.contains_returns(line):
                    ret = self.extract_return_values(line)
                    moduleInfo["Classes"][c_name]["Methods"][m_name]["Returns"].append(ret)

            if isCurrentlyClass:
                textBlockLineCounter += 1

                # Block end is marked by a character as the first entry of a line
                if self.is_block_end(line):
                    isCurrentlyClass = False
                    textBlockLineCounter -= 1

                    # Class end: append all the collected information to this class
                    moduleInfo["Classes"][c_name]["General"] = {
                                "LoC": textBlockLineCounter,
                                "LoD": textBlockDocLineCounter,
                                "LoN": textBlockEmptyLineCounter,
                                "Start": moduleInfo["Classes"][c_name]["General"]["Start"],
                                "End": lnr
                                }
                    moduleInfo["Classes"][c_name]["Doc"] = textDocString
                    textBlockLineCounter = 0

                    # if it is still a method, append information
                    if isCurrentlyMethod:
                        moduleInfo["Classes"][c_name]["Methods"][m_name]["General"] = {
                                "LoC": methodLineCounter,
                                "LoD": methodDocLineCounter,
                                "LoN": methodEmptyLineCounter,
                                "Start": moduleInfo["Classes"][c_name]["Methods"][m_name]["General"]["Start"],
                                "End": lnr
                                }
                        moduleInfo["Classes"][c_name]["Methods"][m_name]["Doc"] = methodDocString

                # extract attribute marked by "self." and not a open bracket at end (Then it is method)
                elif self.contains_attribute(line):
                    attribute = self.extract_attribute(line)
                    moduleInfo["Classes"][c_name]["Attributes"].add(attribute)

                # Check for method marked by "    def" (4 whitepsaces, then def)
                elif self.contains_method(line):
                    methodLineCounter = 0
                    methodDocLineCounter = 0
                    methodEmptyLineCounter = 0
                    methodDocString = ""
                    isCurrentlyMethod = True
                    m_name, arguments = self.extract_function_name_and_arguments(line)

                    # Multiline if no closing bracket is found on the line
                    if arguments == "multiline_input":
                        multiline_input = True
                        arguments = self.extract_first_line_input(line)

                    # Initilaize entry for this method
                    moduleInfo["Classes"][c_name]["Methods"][m_name] = {
                            "Arguments": arguments, "Returns": [], "General": {"Start": lnr},
                            "Doc": ""
                            }

            if isCurrentlyFunction:
                textBlockLineCounter += 1

                # Block end marked as for classes with letter at first position of the line
                if self.is_block_end(line):
                    isCurrentlyFunction = False
                    textBlockLineCounter -= 1

                    # Record infromation for this function
                    moduleInfo["Functions"][f_name]["General"] = {
                                "LoC": textBlockLineCounter,
                                "LoD": textBlockDocLineCounter,
                                "LoN": textBlockEmptyLineCounter,
                                "Start": moduleInfo["Functions"][f_name]["General"]["Start"],
                                "End": lnr
                                }
                    moduleInfo["Functions"][f_name]["Doc"] = textDocString
                    textBlockLineCounter = 0

                # Checks for returns. Note: This does not necessarily mean the end of the function!!
                elif self.contains_returns(line):
                    ret = self.extract_return_values(line)
                    moduleInfo["Functions"][f_name]["Returns"].append(ret)

            # Count comment lines marked by # as first nonemtpy symbol
            if not isCurrentlyDoc and self.is_comment(line):
                docLineCounter += 1
                if isCurrentlyClass or isCurrentlyFunction:
                    textBlockDocLineCounter += 1
                    if isCurrentlyMethod:
                        methodDocLineCounter += 1

            # contains import keyword
            elif not isCurrentlyDoc and self.is_import(line):
                importInfo = self.extract_import_info(line)
                moduleInfo["Imports"].append(importInfo)

            # Class header marked by class _name_(_parents_)
            elif not isCurrentlyDoc and self.contains_class_header(line):
                textBlockLineCounter = 0
                textBlockDocLineCounter = 0
                textBlockEmptyLineCounter = 0
                textDocString = ""
                isCurrentlyClass = True
                c_name = self.extract_class_name(line)
                inheritance = self.extract_between_brackets(line)
                if inheritance == "multiline_input":
                    multiline_input = True
                    inheritance = self.extract_first_line_input(line)
                else:
                    inheritance = inheritance.split(",")
                moduleInfo["Classes"][c_name] = {
                                "Methods": {}, "Attributes": set([]),
                                "General": {"Start": lnr}, "Doc": "",
                                "Inheritance": inheritance
                                }

            # Function header marked by def _name_(*args, **kwargs)
            elif not isCurrentlyDoc and self.contains_function_header(line):
                textBlockLineCounter = 0
                textBlockDocLineCounter = 0
                textBlockEmptyLineCounter = 0
                textDocString = ""
                isCurrentlyFunction = True
                f_name, arguments = self.extract_function_name_and_arguments(line)
                if arguments == "multiline_input":
                    multiline_input = True
                    arguments = self.extract_first_line_input(line)
                moduleInfo["Functions"][f_name] = {"Arguments": arguments, "Returns": [],
                        "General": {"Start": lnr}, "Doc": ""}

        # handles special case if class or function is defined at the end of the file
        if textBlockLineCounter != 0:
            if isCurrentlyClass:
                moduleInfo["Classes"][c_name]["General"] = {
                                "LoC": textBlockLineCounter,
                                "LoD": textBlockDocLineCounter,
                                "LoN": textBlockEmptyLineCounter,
                                "Start": moduleInfo["Classes"][c_name]["General"]["Start"],
                                "End": lnr
                                }
            elif isCurrentlyFunction:
                moduleInfo["Functions"][f_name]["General"] = {
                                "LoC": textBlockLineCounter,
                                "LoD": textBlockDocLineCounter,
                                "LoN": textBlockEmptyLineCounter,
                                "Start": moduleInfo["Functions"][f_name]["General"]["Start"],
                                "End": lnr
                                }

        # Append general information to the dictionary
        moduleInfo["General"]["LoC"] = lineCounter
        moduleInfo["General"]["LoD"] = docLineCounter
        moduleInfo["General"]["LoN"] = emptyLineCounter
        moduleInfo["General"]["NoC"] = len(moduleInfo["Classes"])
        moduleInfo["General"]["NoF"] = len(moduleInfo["Functions"])
        moduleInfo["Doc"] = docString
        moduleInfo["Modulename"] = filename

        self.moduleInfo[filename] = moduleInfo
        return moduleInfo

    def is_empty(self, line):
        """ Regexp: "^\s*$"
        """
        r = re.compile("^\s*$")
        if re.match(r, line):
            return True
        else:
            return False

    def is_comment(self, line):
        """ Regexp: "^\s*#"
        """
        r = re.compile("^\s*#")
        if re.match(r, line):
            return True
        else:
            return False

    def contains_docstring_call(self, line):
        ''' Regexp: '^\s*"""'
        '''
        r = re.compile('^\s*"""')
        if re.match(r, line):
            return True
        else:
            return False

    def is_import(self, line):
        """ Regexp: "(^\s*import\s)|(^\s*from\s)"
        """
        r = re.compile("(^\s*import\s)|(^\s*from\s)")
        if re.search(r, line):
            return True
        else:
            return False

    def contains_class_header(self, line):
        """ Regexp: "^class "
        """
        r = re.compile("^class ")
        if re.search(r, line):
            return True
        else:
            return False

    def contains_function_header(self, line):
        """ Regexp: "^def"
        """
        r = re.compile("^def")
        if re.search(r, line):
            return True
        else:
            return False

    def is_block_end(self, line):
        """ Regexp: "^\w+"
        """
        r = re.compile("^\w+")
        if re.search(r, line):
            return True
        else:
            return False

    def is_method_block_end(self, line):
        """ Regexp: "(^    \w+)|(^\w+)"
        """
        r = re.compile("(^    \w+)|(^\w+)")
        if re.search(r, line):
            return True
        else:
            return False

    def is_input_end(self, line):
        """ Regexp: "\)"
        """
        r = re.compile("\)")
        if re.search(r, line):
            return True
        else:
            return False

    def contains_attribute(self, line):
        """ Regexp: "self\.\w+\(?"
        """
        r = re.compile("self\.\w+\(?")
        attribute = re.search(r, line)
        if attribute and attribute.group(0)[-1]!="(":
            return True
        else:
            return False

    def contains_method(self, line):
        """ Regexp: "^    def "
        """
        r = re.compile("^    def ")
        if re.search(r, line):
            return True
        else:
            return False

    def contains_returns(self, line):
        """ Regexp: "^\s*return "
        """
        r = re.compile("^\s*return ")
        if re.search(r, line):
            return True
        else:
            return False

    def extract_file_name(self, f):
        """ Regexp: "\w*\.py"
        """
        r = re.compile("\w*\.py")
        m = re.search(r, f)
        filename = m.group(0)
        return filename

    def extract_class_name(self, line):
        """ Regexp: "(?<=class )\w+"
        """
        r = re.compile("(?<=class )\w+")
        m = re.search(r, line)
        classname = m.group(0)
        return classname

    def extract_import_info(self, line):
        """ Regexp: "((?<=^import )\w+)|((?<=^from )\w+)"; "(?<= as )\w+"; "(?<= import )\w+.*"
        """
        r = re.compile("((?<=^import )\w+)|((?<=^from )\w+)")
        m = re.search(r, line)
        import_name = m.group(0)
        r = re.compile("(?<= as )\w+")
        m = re.search(r, line)
        if m is not None:
            import_as = m.group(0)
        else:
            import_as = "-"
        r = re.compile("(?<= import )\w+.*")
        m = re.search(r, line)
        if m is not None:
            import_from = m.group(0)
        else:
            import_from = "-"
        return [import_name, import_as, import_from]

    def extract_function_name(self, line):
        """ Regexp: "(?<=def )\w+"
        """
        r = re.compile("(?<=def )\w+")
        m = re.search(r, line)
        functionname = m.group(0)
        return functionname

    def extract_between_brackets(self, line):
        """ Regexp: "\(.*\)"
        """
        r = re.compile("\(.*\)")
        m = re.search(r, line)
        try:
            return m.group(0)[1:-1]
        except AttributeError:
            return "multiline_input"

    def extract_arguments_keywords_and_defaults(self, line):
        """ Regexp: ",\s*"; "\s*=\s*"
        """
        r = re.compile(",\s*")
        arguments = re.split(r, line)
        r = re.compile("\s*=\s*")
        arguments = [re.split(r, argument.strip()) for argument in arguments if argument.strip() != ""]
        arguments = [[arg[0], ""] if len(arg)==1 else arg for arg in arguments]
        return arguments

    def extract_attribute(self, line):
        """ Regexp: "(?<=self\.)\w+"
        """
        r = re.compile("(?<=self\.)\w+")
        attribute = re.search(r, line).group(0)
        return attribute

    def extract_return_values(self, line):
        """ Regexp: "(?<=return ).*"
        """
        r = re.compile("(?<=return ).*")
        ret = re.search(r, line).group(0).split(",")
        return ret

    def extract_function_name_and_arguments(self, line):
        """ Wrapper around extract_function_name(), extract_between_brackets()
        and extract_arguments_keywords_and_defaults()
        """
        f_name = self.extract_function_name(line)
        arguments = self.extract_between_brackets(line)
        if arguments != "multiline_input":
            arguments = self.extract_arguments_keywords_and_defaults(arguments)
        return f_name, arguments

    def extract_first_line_input(self, line):
        """ Regexp: "(\(.*(?=#))|(\(.*)"
        """
        r = re.compile("(\(.*(?=#))|(\(.*)")
        m = re.search(r, line)
        try:
            arguments = self.extract_arguments_keywords_and_defaults(m.group(0)[1:])
            return arguments
        except AttributeError:
            return []

    def extract_center_line_input(self, line):
        """ Regexp: ".*(?=#)|(.*)"
        """
        r = re.compile(".*(?=#)|(.*)")
        m = re.search(r, line)
        try:
            arguments = self.extract_arguments_keywords_and_defaults(m.group(0))
            return arguments
        except AttributeError:
            return []


    def extract_last_line_input(self, line):
        """ Regexp: ".*\)"
        """
        r = re.compile(".*\)")
        m = re.search(r, line)
        try:
            arguments = self.extract_arguments_keywords_and_defaults(m.group(0)[:-1])
            return arguments
        except AttributeError:
            return []


class MarkdownConverter():
    """ Converts the non-human readable summary of the module into readable markdown format.
    """

    def __init__(self):
        pass

    def convert_to_md(self, parsed_file, mode="Module", name=None):
        """ Converts the input from the FileParser().parse_file(f) to a markdown string.

        Parameters
        ----------
        parsed_file : Output of the FileParser.parse_file(f) method
        mode : None, "Module", "Function" or "Class" [None]
            "Module" : The whole module/code file is converted to Markdown format. Argument "name" is ignored.
            "Classes": Only classes are converted into Markdown format. Argument "name" is ignored.
            "Functions": Only functions are converted into Markdown format. Argument "name" is ignored.
            "Class": Only a single class is converted to Markdown format. Argument "name" must be provided.
            "Function": Only a single function is converted to Markdown format. Argument "name" must be provided.
        name : str or None [None]
            Only used if "mode"=="Class" or "mode"=="Function". Constructs Markdown file of a single class or function
            indicated by the name of the class or function.

        Returns
        -------
        mdstring : str
            Markdown format string of the indicated code block.
        """
        self.module_name = parsed_file["Modulename"].replace("_", "\_")

        if mode == "Module":
            if name is not None:
                print("\n\tWarning: 'name' is not None, but ignored!\n")
            mdstring = self.convert_module_to_md(parsed_file)

        elif mode == "Classes":
            if name is not None:
                print("\n\tWarning: 'name' is not None, but ignored!\n")
            mdstring = self.convert_classes_to_md(parsed_file["Classes"], show_module=True)

        elif mode == "Functions":
            if name is not None:
                print("\n\tWarning: 'name' is not None, but ignored!\n")
            mdstring = self.convert_functions_to_md(parsed_file["Functions"], show_module=True)

        elif mode == "Class":
            if name is None:
                raise ValueError("If 'mode'=='Class', the name of the class has to be provided. Alternatively 'Classes'"
                                 "can be passed to convert all class information")
            mdstring = self.convert_class_to_md(parsed=parsed_file["Classes"][name], name=name, show_module=True)

        elif mode == "Function":
            if name is None:
                raise ValueError("If 'mode'=='Function', the name of the function has to be provided. Alternatively 'Functions'"
                             "can be passed to convert all function information")
            mdstring = self.convert_function_to_md(parsed=parsed_file["Functions"][name], name=name, show_module=True)

        return mdstring


    def convert_module_to_md(self, parsed):
        """ Convert a module to a .md file.

        Parameters
        ----------
        parsed : dict
            parsed information about the module

        Returns
        -------
        mdstring : str
            Module information as markdown file.
        """
        header = "# Module:     {}".format(self.module_name)
        tableOfContents = "\n\nThis module contains:\n- [{} Classes](#classes-of-{})\n- [{} Functions](#functions-of-{})\n\n".format(parsed["General"]["NoC"], self.module_name, parsed["General"]["NoF"], self.module_name)
        general_info_table = ("| General                      | Value|\n" \
                              "| ---------------------------- | ---- |\n" \
                              "| Lines of Code (LoC)          | {:04d} |\n".format(parsed["General"]["LoC"]) +
                              "| Lines of documentation (LoD) | {:04d} |\n".format(parsed["General"]["LoD"]) +
                              "| Empty lines (LoN)            | {:04d} |\n".format(parsed["General"]["LoN"]) +
                              "| Number of classes (NoC)      | {:04d} |\n".format(parsed["General"]["NoC"]) +
                              "| Number of functions (NoF)    | {:04d} |\n".format(parsed["General"]["NoF"])
                              )
        docstring = parsed["Doc"] if parsed["Doc"] != "" else "_No documentation available_"
        docstring = "\n## Documentation\n\n{}\n\n".format(docstring)

        imports = ("\n## Imports\n\nFollowing packages are imported:\n\n"
                   "| Package                          | Imported as      | Imported objects                    |\n" \
                   "| -------------------------------- | ---------------- | ----------------------------------- |\n" \
                    )
        importslist = "".join(["| {:<32} | {:<16} | {:<35} |\n".format(lib, AS, obj) for lib, AS, obj in parsed["Imports"]])
        imports += importslist

        classesdescription = "\n\n" + self.convert_classes_to_md(parsed["Classes"], show_module=False)
        functiondescription = "\n\n" + self.convert_functions_to_md(parsed["Functions"], show_module=False)

        mdstring = header + tableOfContents + general_info_table + docstring + imports + classesdescription + functiondescription
        return mdstring


    def convert_classes_to_md(self, parsed, show_module):
        """ Convert all classes of a module to a .md file.

        Parameters
        ----------
        parsed : dict
            parsed information about classes
        show_module : bool
            show_module name only for single plotted classes, not when this function is called from within
            a module.md creation function.

        Returns
        -------
        mdstring : str
            Classes information as markdown file.
        """
        header = "# Classes of {}".format(self.module_name)
        tableOfContents = "\nThis module contains following classes:\n"

        for i, Class in enumerate(parsed):
            tableOfContents += "- [{:<40} ({}, {})](#class:-{})\n".format(
                                                                   Class.replace("_", "\_"),
                                                                   parsed[Class]["General"]["LoC"],
                                                                   parsed[Class]["General"]["LoD"],
                                                                   Class.lower().replace("_", "\_"))

        classDescription = "\n\n\n\n"
        for Class in parsed:
            classDescription += self.convert_class_to_md(parsed[Class], name=Class.replace("_", "\_"), show_module=False) + "\n\n\n"

        mdstring = header + tableOfContents + classDescription
        return mdstring


    def convert_functions_to_md(self, parsed, show_module):
        """ Convert all functions of a module to a .md file.

        Parameters
        ----------
        parsed : dict
            parsed information about functions
        show_module : bool
            show_module name only for single plotted functions, not when this function is called from within
            a module.md creation function.

        Returns
        -------
        mdstring : str
            Functions information as markdown file.
        """
        header = "# Functions of {}".format(self.module_name)
        tableOfContents = "\nThis module contains following functions:\n"

        for i, function in enumerate(parsed):
            tableOfContents += "- [{:<40} ({}, {})](#function:-{})\n".format(
                                                                              function.replace("_", "\_"),
                                                                              parsed[function]["General"]["LoC"],
                                                                              parsed[function]["General"]["LoD"],
                                                                              function.lower().replace("_", "\_")
            )

        functionDescription = "\n\n\n\n"
        for function in parsed:
            functionDescription += self.convert_function_to_md(parsed[function], name=function.replace("_", "\_"), show_module=False) + "\n\n\n"

        mdstring = header + tableOfContents + functionDescription
        return mdstring


    def convert_class_to_md(self, parsed, name, show_module=True):
        """ Convert the information about a single class of a module to a md file.

        Parameters
        ----------
        parsed : dict
            parsed information about classes
        name : str
            name of the class to be converted
        show_module : bool
            show_module name only for single plotted classes, not when this function is called from within
            a classes.md creation function.

        Returns
        -------
        mdstring : str
            Class information as markdown file.
        """
        headerlevel = "#" if show_module else "####"
        header = "{} Class: {}\n\n".format(headerlevel, name)
        if show_module:
            from_module = "From module      __*{}*__\n\n".format(self.module_name)
        else:
            from_module = ""

        jumpTo = "Jump to:\n- [Methods](#methods-of-{})\n- [Attributes](#attributes-of-{})\n\n".format(name.lower(),                                                                                       name.lower())
        general_info_table = ("| General                      | Value|\n" \
                              "| ---------------------------- | ---- |\n" \
                              "| Start line (Start)           | {:04d} |\n".format(parsed["General"]["Start"]) +
                              "| End line (End)               | {:04d} |\n".format(parsed["General"]["End"]) +
                              "| Lines of Code (LoC)          | {:04d} |\n".format(parsed["General"]["LoC"]) +
                              "| Lines of documentation (LoD) | {:04d} |\n".format(parsed["General"]["LoD"]) +
                              "| Empty lines (LoN)            | {:04d} |\n".format(parsed["General"]["LoN"]) +
                              "| Number of methods            | {:04d} |\n".format(len(parsed["Methods"])) +
                              "| Number of Attributes         | {:04d} |\n".format(len(parsed["Attributes"])) +
                              "| Number of parents            | {:04d} |\n".format(len(parsed["Inheritance"]))
                              )
        docstring = parsed["Doc"] if parsed["Doc"] != "" else "_No documentation available_"
        docstring = "\n#{} Documentation\n\n{}\n\n".format(headerlevel, docstring)
        inheritance = "This class inherits from:\n"
        for inher in parsed["Inheritance"]:
            if inher != "":
                inheritance += "- {}\n".format(inher)
        inheritance = "\n#{} Inheritance\n\n{}\n\n".format(headerlevel, inheritance)
        tableOfContents = "\n#{} Methods of {}\n\n".format(headerlevel, name)
        tableOfContents += "This class contains following methods:\n\n"

        for i, function in enumerate(parsed["Methods"]):
            function = function.replace("_", "\_")
            tableOfContents += "{}. [{}](#method:-{})\n".format(i+1, function, function).lower()

        methods = ""
        for method in parsed["Methods"]:
            methods += self.convert_function_to_md(parsed["Methods"][method], name=method.replace("_", "\_"), show_module=False).replace("Function", "Method")

        attributes = "\n\n#{} Attributes of {}\n\nA list of the used attributes:\n\n".format(headerlevel, name)
        for i, attribute in enumerate(parsed["Attributes"]):
            attributes += "{} {}; ".format(i, attribute)
            if i % 5 == 0 and i != 0:
                attributes += "\n"
        attributes += "\n\n"

        mdstring = header + from_module + jumpTo + general_info_table + docstring + inheritance + tableOfContents + methods + attributes
        return mdstring


    def convert_function_to_md(self, parsed, name, show_module=True):
        """ Convert the information about a single function of a module to a md file.

        Parameters
        ----------
        parsed : dict
            parsed information about functions
        name : str
            name of the function to be converted
        show_module : bool
            show_module name only for single plotted functions, not when this function is called from within
            a functions.md creation function.

        Returns
        -------
        mdstring : str
            Function information as markdown file.
        """
        headerlevel = "#" if show_module else "####"
        header = "{} Function: {}\n\n".format(headerlevel, name)
        if show_module:
            from_module = "From module      __*{}*__\n\n".format(self.module_name)
        else:
            from_module = ""
        general_info_table = ("| General                      | Value|\n" \
                              "| ---------------------------- | ---- |\n" \
                              "| Start line (Start)           | {:04d} |\n".format(parsed["General"]["Start"]) +
                              "| End line (End)               | {:04d} |\n".format(parsed["General"]["End"]) +
                              "| Lines of Code (LoC)          | {:04d} |\n".format(parsed["General"]["LoC"]) +
                              "| Lines of documentation (LoD) | {:04d} |\n".format(parsed["General"]["LoD"]) +
                              "| Empty lines (LoN)            | {:04d} |\n".format(parsed["General"]["LoN"])
                              )
        docstring = parsed["Doc"] if parsed["Doc"] != "" else "_No documentation available_"
        docstring = "\n#{} Documentation\n\n{}\n\n##### Arguments\n\n".format(headerlevel, docstring)
        arguments = "| Arguments                      | Default                        |\n" \
                    "| -------------------------------| ------------------------------ |\n"
        argumentslist = "".join(["| {:<30} | {:<30} |\n".format(arg, default) for arg, default in parsed["Arguments"]])
        arguments += argumentslist
        returns = "\n##### Returns\n\n"
        returnlist = "".join(["- Return {}:  ".format(i+1) + "".join(ret).replace(" ", "  &  ") + "\n" for i, ret in enumerate(parsed["Returns"])])
        returns += returnlist

        mdstring = header + from_module + general_info_table + docstring + arguments + returns
        return mdstring


    def mash_markdown_files(self, misc_mds, names, md_types):
        """ Used to mash markdown texts from individual functions.

        Mainly called by the frontend to combine informations from different modules or to combine module with each other.
        This function mainly creates the header for these kind of things.

        Parameters
        ----------
        misc_mds : list
            List of miscellaneous markdown files.
        names : list
            Same length as misc_md. Corresponding names of the functions.
        md_types : list
            Same length as misc_md. Corresponding type of .md file ("Module", "Class", "Function").

        Returns
        -------
        mdstring : str
            Function information as markdown file.
        """
        assert len(misc_mds) == len(names), "Wrong length of names. Needed {}, but given {}.".format(len(misc_md), len(names))
        assert len(misc_mds) == len(md_types), "Wrong length of types. Needed {}, but given {}.".format(len(misc_md), len(md_types))

        header = "\n\n\n# OVERVIEW\n\n"
        intro = "Following descriptions are provided:\n"
        tableofcontents = ""
        for i, (name, md_type) in enumerate(zip(names, md_types)):
            tableofcontents += "{}. [{}: {}](#{}:-----{})\n".format(i+1, md_type, name.replace("_", "\_"), md_type.lower(), name.lower().replace("_", "\_"))

        content = "\n\n"
        for misc_md in misc_mds:
            content += misc_md

        mdstring = header + intro + tableofcontents + content
        return mdstring




if __name__=="__main__":
    parser = FileParser()
    Converter = MarkdownConverter()

    folder = "../NN"
    files = ["../NN/animate_training.py", "../NN/plot_nn.py", "../NN/scikit_neural_network.py"]

    file = "../ClassDiagram/class_diagram_backend.py"
    parsed_file = parser.parse_file(file)
    markdown = Converter.convert_to_md(parsed_file, mode="Classes", name="MarkdownConverter")

    # files = files[1]
    # parsed_file = parser.parse_file(files)
    # markdown = Converter.convert_to_md(parsed_file, mode="Functions", name="simulate_network")

    with open("./test.md", "w") as f:
        f.write(markdown)



