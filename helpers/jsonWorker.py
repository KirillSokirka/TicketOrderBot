import json


class JSONWorker:

    @staticmethod
    def get_list_of_parameter_values(json_filename, parameter):
        """
        return all values which is connected with this parametr
        :param json_filename: file to get json_data_from
        :param parameter: parameter which value in every object we intersted in
        :return: look upper
        """
        parameters = []
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for param in data:
                parameters.append(param[parameter])
        return parameters

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
    def get_event_by_param_value(json_filename, param, value):
        """
        will correctly works only with id and name
        :param json_file: file to get json_data_from
        :param param: name of parameter
        :return: event
        """
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for event in data:
                if event[param] == value:
                    return event
        return None

    @staticmethod
    def get_value_by_event_id(json_filename, name_of_param, id):
        """
        returns a value of param from event with id
        :param json_filename: file to get json_data_from
        :param name_of_param: name of param which value u need
        :param id: id of event
        :return: value of needed param
        """
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for event in data:
                if event['id'] == id:
                    return event[name_of_param]
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
        with open(json_filename, 'r') as file:
            data = json.loads(file.read())
            for obj in data:
                if obj[name_of_key_value] == obj_id_to_update:
                    obj[name_to_update] = new_value
                    break
        with open(json_filename, 'w') as file:
            file.seek(0)
            json.dump(data, file, indent=2)
        return True

    @staticmethod
    def save_to_json(filename, obj):
        with open(filename, "r+") as f:
            data = json.load(f)
            data.append(obj.__dict__())
            f.seek(0)
            json.dump(data, f, indent=2)
