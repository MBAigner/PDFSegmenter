import pickle


def save_object(obj, path, name):
    """

    :param obj:
    :param path:
    :param name:
    :return:
    """
    with open(path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_object(path, name):
    """

    :param path:
    :param name:
    :return:
    """
    with open(path + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def get_file_name(path):
    """

    :param path:
    :return:
    """
    parts = path.split("/")
    return parts[len(parts) - 1]


def replace_file_type(file_name, new_type):
    """

    :param file_name:
    :param new_type:
    :return:
    """
    file_name_parts = file_name.split(".")
    return file_name.replace(file_name_parts[len(file_name_parts)-1], new_type)


def cut_file_type(file_name):
    """

    :param file_name:
    :return:
    """
    file_name_parts = file_name.split(".")
    return file_name.replace("." + file_name_parts[len(file_name_parts)-1], "")
