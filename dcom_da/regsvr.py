from win32com.client import gencache
import win32com.client.makepy as makepy
import shutil
import os
import pickle
import sys
import win32timezone
from log.LOGS import LOGS

def regsvr():
    try:
        src = 'OPCDAAuto.dll'
        if os.path.exists(r'C:/Windows/SysWOW64'):
            LOGS('dcom_da/regsvr', 'Попытка записи OPCDAAuto.dll в SysWOW64', 'INFO')
            dist = r"C:/Windows/SysWOW64/"
            LOGS('dcom_da/regsvr', 'Успех: OPCDAAuto.dll записался в SysWOW64', 'INFO')
            print('Successfull write lib to: ', shutil.copy(src, dist))

        dist = r"C:/Windows/System32/"
        LOGS('dcom_da', 'Попытка записи OPCDAAuto.dll в System32', 'INFO')
        print('Successfull write lib to: ', shutil.copy(src, dist))
        os.system("regsvr32 /s OPCDAAuto.dll")
        LOGS('dcom_da/regsvr', 'Успех: OPCDAAuto.dll записался в System32', 'INFO')
        infos = makepy.GetTypeLibsForSpec(r'OPCDAAuto.dll')
        for (tlb, tlbSpec) in infos:
            desc = tlbSpec.desc
            if desc is None:
                if tlb is None:
                    desc = "<Could not load typelib %s>" % (tlbSpec.dll)
                else:
                    desc = tlb.GetDocumentation(-1)[0]
        if len(tlbSpec.clsid) != 0:

            with open('DLL_CLSID', 'wb') as file:
                pickle.dump(tlbSpec.clsid, file)

            LOGS('dcom_da/regsvr', 'Успех: Получилось зарегистрировать библиотеку', 'INFO')
            print('Successfull lib registration')
        else:
            print('Lib registration error')
            LOGS('dcom_da/regsvr', 'Ошибка: Не получилось зарегистрировать библиотеку', 'ERROR')

        return tlbSpec.clsid
    except Exception as err:
        print('Error: ', err)
        LOGS('dcom_da/regsvr', 'Ошибка: Проверьте права пользователя для регистрации', 'ERROR')
        return False

def get_clsid():
    if os.path.exists('DLL_CLSID') != True:
        LOGS('dcom_da/regsvr.get_clsid', 'Нет файла DLL_CLSID идет поиск решения', 'INFO')
        clsid=regsvr()

        if clsid!=False:
            LOGS('dcom_da/regsvr.get_clsid', 'Успех: Получилось создать и получить значения с DLL_CLSID', 'INFO')
            return clsid
        else:
            LOGS('dcom_da/regsvr.get_clsid', 'Ошибка: Не получилось создать DLL_CLSID', 'ERROR')
            raise Exception('Failed to register library ')

    else:
        with  open('DLL_CLSID', 'rb') as file:
            LOGS('dcom_da/regsvr.get_clsid', 'Успех: Получилось получить значения с DLL_CLSID', 'INFO')
            return pickle.load(file)

def get_serv_list():
    if os.path.exists('DLL_CLSID') != True:
        LOGS('dcom_da/regsvr.get_serv_list', 'Нет файла DLL_CLSID идет поиск решения', 'INFO')
        clsid=regsvr()
        if clsid == False:
            LOGS('dcom_da/regsvr.get_serv_list', 'Ошибка: не получилось создать DLL_CLSID', 'ERROR')
            raise Exception('Failed to register library ')
    else:
        with open('DLL_CLSID', 'rb') as file:
            clsid=pickle.load(file)
            LOGS('dcom_da/regsvr.get_serv_list', 'Успех:получилось получить значения с DLL_CLSID', 'INFO')

    dll = gencache.EnsureModule(clsid, 0, 1, 0)
    opcserver = dll.OPCServer()
    LOGS('dcom_da/regsvr.get_serv_list', 'Получение списка серверов', 'INFO')
    DAservers = opcserver.GetOPCServers()

    if len(DAservers) == 0:
        print('DA servers not found')
        LOGS('dcom_da/regsvr.get_serv_list', 'Список серверов пуст', 'INFO')
        sys.exit()

    i = 1
    for serv in DAservers:
        LOGS('dcom_da/regsvr.get_serv_list', 'Вывод списка серверов', 'INFO')
        print(str(i) + '. ' + serv)
        i += 1