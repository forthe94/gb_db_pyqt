import dis


def get_methods_and_attrs(clsdict):
    methods = set()
    attrs = set()
    for elem in clsdict:
        try:
            instructions = dis.get_instructions(clsdict[elem])
        except TypeError:
            print(f'Cant disassembler {clsdict[elem]}')
        else:
            for inst in instructions:
                # print(inst)
                if inst.opname == 'LOAD_GLOBAL':
                    # Global method used in class
                    methods.add(inst.argval)
                if inst.opname == 'LOAD_ATTR':
                    # Attr used in class
                    attrs.add(inst.argval)
    return methods, attrs


class ServerMaker(type):
    def __init__(self, clsname, bases, clsdict):
        methods, attrs = get_methods_and_attrs(clsdict)
        if 'connect' in methods:
            raise TypeError('Connect method shouldnt be used in server class')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Wrong socket initialization')
        super().__init__(clsname, bases, clsdict)


class ClientMaker(type):
    def __init__(self, clsname, bases, clsdict):
        methods, _ = get_methods_and_attrs(clsdict)
        if methods.intersection({'accept', 'listen', 'socket'}):
            raise TypeError('Usage of forbidden method in client class')
        if methods.intersection({'get_message', 'send_message'}) != {'get_message', 'send_message'}:
            TypeError('Message processing functions not found in client class')

        super().__init__(clsname, bases, clsdict)