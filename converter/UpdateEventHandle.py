from opcua import ua


def get_ua_type(value):
    if value.__class__.__name__ == 'int':
        return ua.uatypes.VariantType.Int32
    elif value.__class__.__name__ == 'float':
        return ua.uatypes.VariantType.Float
    elif value.__class__.__name__ == 'bool':
        return ua.uatypes.VariantType.Boolean
    elif value.__class__.__name__ == 'str':
        return ua.uatypes.VariantType.String
    else:
        return None


def get_variant_type(datatype):
    if datatype == 'bool':
        variant = ua.VariantType.Boolean
    elif datatype == 'int':
        variant = ua.VariantType.Int32
    elif datatype == 'float':
        variant = ua.VariantType.Float
    elif datatype == 'str':
        variant = ua.VariantType.String
    else:
        raise ValueError('"%s" datatype not implemented' % datatype)

    return variant


class UpdateEventHandler:

    def set_lists(self, ualist, dalist):
        self.ualist = ualist
        self.dalist = dalist

    def OnDataChange(self, TransactionID, NumItems, ClientHandles, ItemValues, Qualities, TimeStamps):
        i = 0
        # print(TransactionID, NumItems, ClientHandles, ItemValues, Qualities, TimeStamps)
        while (i < NumItems):
            handle = ClientHandles[i]
            value = ItemValues[i]
            quality = Qualities[i]
            time = TimeStamps[i]

            self.ualist[self.dalist[handle]].set_value(value, get_ua_type(value))
            # print('is worked...')
            i = i + 1
