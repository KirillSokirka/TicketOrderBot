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