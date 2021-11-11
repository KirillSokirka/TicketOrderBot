import json
from helpers.s3manager import S3Manager
from config import EVENTS_KEY, TICKETS_KEY


class JSONWorker:

    @staticmethod
    def get_values_by_parameter_name(json_filename, parameter):
        """
        return all values which is connected with this parameter
        :param json_filename: file to get json_data_from
        :param parameter: parameter which value in every object we interested in
        :return: look upper
        """
        parameters = []
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for param in data:
                parameters.append(param[parameter])
        return parameters

    @staticmethod
    def get_all_objects(json_filename):
        """
        Func to get all objects in specified json
        :param json_filename: name of json_file
        :return: list of objects in dict form
        """
        objs = []
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for obj in data:
                objs.append(obj)
        return objs

    @staticmethod
    def get_list_of_object_by_key(json_filename, parameter_name, key):
        """
        func to get list oj objects by param name:
        :param json_filename: name of json file
        :param parameter_name: name of parametr which u will use to get list_of_objects
        :param key: key value
        :return:
        """
        objs = []
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for obj in data:
                if obj[parameter_name] == key:
                    objs.append(obj)
        return objs

    @staticmethod
    def get_object_by_key(json_filename, param, value):
        """
        returns a object by one of it parameter value
        :param json_file: file to get json_data_from
        :param param: name of parameter
        :return: object
        """
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for d in data:
                if d[param] == value:
                    return d
        return None

    @staticmethod
    def get_object_value(json_filename, name_of_param, id):
        """
        returns a value of param from event with id
        :param json_filename: file to get json_data_from
        :param name_of_param: name of param which value u need
        :param id: id of object
        :return: value of needed param
        """
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for d in data:
                if d['id'] == id:
                    return d[name_of_param]
        return None

    @staticmethod
    def check_if_unique(json_filename, name_of_param, value):
        """
        checks a value for uniqueness
        :param json_filename: file to get json_data_from
        :param name_of_param: name of parameter wnich value uniqueness will be checked
        :param value: value to check uniquness
        :return: false or true, it depends
        """
        temp = ''
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for event in data:
                if event[name_of_param] == value:
                    return False
        return True

    @staticmethod
    def update_value(json_filename, name_of_key_value ,obj_id_to_update, name_to_update, new_value):
        """
        update a specific value in object to a new value
        :param json_filename: json which should be updated
        :param name_of_key_value: name of specific value
        :param obj_id_to_update: object which value we should update
        :param name_to_update: name of pdram which ll be updated
        :param new_value: new value
        :return: True if everything correct
        """
        temp = ''
        if json_filename == 'json_files/tickets.json':
            temp = TICKETS_KEY
        else:
            temp = EVENTS_KEY
        S3Manager.download_object(json_filename, temp)
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for obj in data:
                if obj[name_of_key_value] == obj_id_to_update:
                    obj[name_to_update] = new_value
                    break
        with open(json_filename, 'w') as file:
            file.seek(0)
            json.dump(data, file, indent=2)
        S3Manager.upload_object(json_filename, temp)
        return True

    @staticmethod
    def save_to_json(filename, obj):
        temp = ''
        if filename == 'json_files/tickets.json':
            temp = TICKETS_KEY
        else:
            temp = EVENTS_KEY
        S3Manager.download_object(filename, temp)
        with open(filename, "r+") as f:
            data = json.load(f)
            data.append(obj.__dict__())
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
        S3Manager.upload_object(filename, temp)

