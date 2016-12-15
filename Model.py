class Document:
    def __str__(self):

        string_obj = ""
        for k,v in self.__dict__.items():
            string_obj += " {0}: {1} ".format(k,v)

        return string_obj


class User:
    pass
