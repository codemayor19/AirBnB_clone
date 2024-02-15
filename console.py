#!/usr/bin/python3
"""
dcs
"""
import cmd
import re
import ast
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City

class HBNBCommand(cmd.Cmd):
    """
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity", "Place",
                      "Review", "State", "City"]

    def emptyline(self):
        """
        do nothing when an empty line is started
        """
        pass

    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

    def help_out(self, arg):
        """
        """
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        """_summary_

        Args:
            arg (_type_): _description_
        """
        print()
        return True

    def do_create(self, arg):
        """create a new instance of BaseModel and use it in the JSOn file.
        Usage: create <class_name>
        """
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{commands[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del object[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific id.
        Usage: all [class_name]
        """
        objects = storage.all()
        commands = shlex.split(arg)
        # print(f"{commands = }")

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))

    def default(self, arg):
        """
        Define a default behavior for cmd module for invalid syntax
        """
        arg_list = arg.split('.')
        incoming_class_name = arg_list[0]
        command = arg_list[1].split('(')
        incoming_method = command[0]
        incoming_extra_arg = command[1].split(")")[0]

    method_dict = {
            'all': self.do_all,
            'show': self.do_show,
            'destroy': self.do_destroy,
            'update': self.do_update,
            'count': self.do_count
        }

        if incoming_method in method_dict.keys():
            if incoming_method != "update":
                return method_dict[incoming_method]("{} {}".format(incoming_class_name, incoming_extra_arg))
            else:
                obj_id, arg_dict = self.split_curly_braces(incoming_extra_arg)
                try:
                    if isinstance(arg_dict, str):
                        attributes = arg_dict
                        return method_dict[incoming_method]("{} {} {}".format(incoming_class_name,
                                                                                obj_id,
                                                                                attributes))
                    elif isinstance(arg_dict, dict):
                        dict_attributes = arg_dict
                        return method_dict[incoming_method]("{} {} {}".format(incoming_class_name,
                                                                                obj_id,
                                                                                dict_attributes))
                except Exception:
                    print("** argument missing **")
        print("** Unknown syntax: {} **".format(arg))
        return False

    def split_curly_braces(incoming_extra_arg):
        """
        split the curly braces for the update method
        """
        curly_braces = re.search(r"\{(.*?)\}")

        if curly_braces:
            id_with_coma = shlex.split(incoming_extra_arg[:curly_braces.span()[0]])
            id = [i.strip(",") for i in id_with_coma][0]
            str_data = curly_braces.group(1)
            try:
                arg_dict = ast.literal_eval("{" + str_data + "}")
            except Exception:
                print("** invalid dictionary format **")
                return
            return id, arg_dict
        else:
            commands = incoming_extra_arg.split(',')
            try:
                id = commands[0]
                attr_name = commands[1]
                attr_value = commands[2]
                return f"{id}", f"{attr_name} {attr_value}"
            except Exception:
                print("** argument missing **")

    def do_count(self, arg):
        """
        Counts and retrieve the number of instances of a class
        Usage: <class name>.count()
        """
        objects = storage.all()
        commands = shlex.split(arg)
        if arg:
            incoming_class_name = commands[0]
        count = 0

        if commands:
            if incoming_class_name in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == incoming_class_name:
                        count += 1
                print(count)
            else:
                print("** check what you are to print **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "attribute_value"
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                curly_braces = re.search(r"\{(.*?)\}", arg)
                if curly_braces:
                    str_data = curly_braces.group(1)

                    arg_dict = ast.literal_eval("{" + str_data + "}")
                    attribute_names = list(arg_dict.keys())
                    attribute_values = list(arg_dict.values())

                    attr_name1 = attribute_names[0]
                    attr_value1 = attribute_values[0]
                    attr_name2 = attribute_names[1]
                    attr_value2 = attribute_values[1]

                    setattr(obj, attr_name1, attr_value1)
                    setattr(obj, attr_name2, attr_value2)
                else:
                    attr_name = commands[2]
                    attr_value = commands[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()
