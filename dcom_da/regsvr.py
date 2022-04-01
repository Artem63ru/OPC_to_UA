from win32com.client import gencache
import win32com.client.makepy as makepy
import shutil
import os
import pickle
import sys
import win32timezone


def regsvr():
    try:
        src = 'OPCDAAuto.dll'
        if os.path.exists(r'C:/Windows/SysWOW64'):
            dist = r"C:/Windows/SysWOW64/"
            print('Successfull write lib to: ', shutil.copy(src, dist))

        dist = r"C:/Windows/System32/"
        print('Successfull write lib to: ', shutil.copy(src, dist))

        os.system("regsvr32 /s OPCDAAuto.dll")

        reg_clsid = makepy.ShowInfo(r'OPCDAAuto.dll')
        if len(reg_clsid) != 0:

            with open('DLL_CLSID', 'wb') as file:
                pickle.dump(reg_clsid[0], file)

            print('Successfull lib registration')
        else:
            print('Lib registration error')

        return reg_clsid[0]
    except Exception as err:
        print('Error: ', err)
        return False

def get_clsid():
    if os.path.exists('DLL_CLSID') != True:
        clsid=regsvr()

        if clsid!=False:
            return clsid
        else:
            raise Exception('Failed to register library ')

    else:
        with  open('DLL_CLSID', 'rb') as file:
            return pickle.load(file)

def get_serv_list():
    if os.path.exists('DLL_CLSID') != True:
        clsid=regsvr()
        if clsid == False:
            raise Exception('Failed to register library ')
    else:
        with open('DLL_CLSID', 'rb') as file:
            clsid=pickle.load(file)

    dll = gencache.EnsureModule(clsid, 0, 1, 0)
    opcserver = dll.OPCServer()

    DAservers = opcserver.GetOPCServers()

    if len(DAservers) == 0:
        print('DA servers not found')
        sys.exit()

    i = 1
    for serv in DAservers:
        print(str(i) + '. ' + serv)
        i += 1