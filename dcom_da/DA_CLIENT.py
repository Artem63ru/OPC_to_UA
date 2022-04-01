from win32com.client import gencache
# from .regsvr import get_clsid
# from regsvr import get_clsid
# from regsvr import get_serv_list
import os
import json
import xlrd
import xlwt
import pickle
import win32com

import dcom_da.regsvr

value_types=['str', 'int', 'bool', 'float']


class DA_CLIENT:
    def __init__(self, host='127.0.0.1', server_name='Matrikon.OPC.Simulation.1', mode='SERVER', file=None, sheet=None, MonitorHandler=None, UpdateRate=500):
        self._server=None
        self._browser=None
        self._opcGroupM=None
        self._opcGroupBuff=None
        self._monitorEventHandler=MonitorHandler
        self.monitorItemsID=[]
        self._serverHandles=[]


        self._isPingSuccess=False


        self.host=host
        self.server_name=server_name
        self.isConnected=False
        self.inputFile=file
        self.inputFileSheet=sheet
        self.UpdateRate=UpdateRate
        self.Tree=None
        self.Mode=mode




    def GetTree(self):
        if self.Tree is not None:
            return self.Tree

        try:
            if self.isConnected==False:
                return None

            if self._server is not None:
                self._browser=self._server.CreateBrowser()

                if self._browser is not None:
                    if self.Mode=='SERVER':
                        if os.path.exists('DA_TREE')==False:
                            self._browser.AccessRights = 0
                            self._opcGroupBuff=self._server.OPCGroups.Add('BufferGroup')
                            self.Tree=self._GetTreeItemByBranches()

                            with open('DA_TREE.json', 'w', encoding='utf-8') as f:
                                json.dump(obj=self.Tree, fp=f, indent=4, ensure_ascii=False, default=str)
                        else:
                             with open('DA_TREE.json', 'r') as file:
                                self.Tree=json.load(file)
                    else:
                        self.GetItemsFromFile()


        except Exception as err:
            print('GetTree Error::', err)

        return self.Tree

    def _GetTreeItemByBranches(self, branches=None, name=None):
        result=[]

        if branches is None:
            self._browser.MoveToRoot()
            self._browser.ShowBranches()
        else:
            self._browser.MoveTo(branches)
            self._browser.ShowBranches()

        brancheCount = self._browser.Count
        for i in range(brancheCount):
            i += 1
            if branches is None:
                self._browser.MoveToRoot()
                self._browser.ShowBranches()
                branches2 = [self._browser.Item(i)]
            else:
                self._browser.MoveTo(branches)
                self._browser.ShowBranches()
                branches2 = [None] * (len(branches) + 1)

                for j in range(len(branches)):
                    branches2[j] = branches[j]
                branches2[-1] = self._browser.Item(i)

            if name == None:
                name_buff = ''
            else:
                name_buff = name + self._browser.Item(i) + '.'

            new_branch={'Name':self._browser.Item(i),
                        'Type':'folder',
                        'BrancheArray':self._GetTreeItemByBranches(branches2, name_buff),
                        'LeafArray':[]}
            self._browser.MoveTo(branches2)
            self._browser.ShowLeafs()
            for j in range(self._browser.Count):
                j+=1
                new_leaf = {'Name': name_buff + self._browser.Item(j),
                            'Type': 'value'}
                try:
                    property_id = [1, 2]
                    property_id.insert(0, 0)

                    values, errors = self._server.GetItemProperties(name_buff + self._browser.Item(j), len(property_id) - 1,
                                                                    property_id)
                    if values[1].__class__.__name__ not in value_types:
                        continue
                    new_leaf['Value']=values[1]
                except:
                    continue

                self.monitorItemsID.append(name_buff + self._browser.Item(j))
                new_branch['LeafArray'].append(new_leaf)
            result.append(new_branch)
        return result


        #     result += "{\"Name\":\""
        #     if name == None:
        #         name_buff = ''
        #     else:
        #         name_buff = name + self._browser.Item(i) + '.'
        #     result += self._browser.Item(i)
        #     result += "\",\"Type\": \"folder"
        #     result += "\",\"BrancheArray\":"
        #     result += self._GetTreeItemByBranches(branches2, name_buff)
        #     result += ",\"LeafArray\":["
        #     self._browser.MoveTo(branches2)
        #     self._browser.ShowLeafs()
        #     for j in range(self._browser.Count):
        #         j += 1
        #         result += "{\"Name\":\""
        #         result += name_buff + self._browser.Item(j)
        #         result += "\",\"Type\": \"value"
        #
        #         property_id = [1, 2]
        #         property_id.insert(0, 0)
        #
        #         values, errors = self._server.GetItemProperties(name_buff + self._browser.Item(j), len(property_id) - 1,
        #                                                         property_id)
        #         print(values[1])
        #         result += "\",\"Value\": {}".format(str(values[1]))
        #
        #         self.monitorItemsID.append(name_buff + self._browser.Item(j))
        #
        #         result += "}"
        #         if j != self._browser.Count:
        #             result += ","
        #     result += "]}"
        #
        #
        # result = "["
        #
        # if branches is None:
        #     self._browser.MoveToRoot()
        #     self._browser.ShowBranches()
        # else:
        #     self._browser.MoveTo(branches)
        #     self._browser.ShowBranches()
        #
        # brancheCount = self._browser.Count
        # for i in range(brancheCount):
        #     i += 1
        #     if branches is None:
        #         self._browser.MoveToRoot()
        #         self._browser.ShowBranches()
        #         branches2 = [self._browser.Item(i)]
        #     else:
        #         self._browser.MoveTo(branches)
        #         self._browser.ShowBranches()
        #         branches2 = [None] * (len(branches) + 1)
        #
        #         for j in range(len(branches)):
        #             branches2[j] = branches[j]
        #         branches2[-1] = self._browser.Item(i)
        #
        #     result += "{\"Name\":\""
        #     if name == None:
        #         name_buff = ''
        #     else:
        #         name_buff = name + self._browser.Item(i) + '.'
        #     result += self._browser.Item(i)
        #     result += "\",\"Type\": \"folder"
        #     result += "\",\"BrancheArray\":"
        #     result += self._GetTreeItemByBranches(branches2, name_buff)
        #     result += ",\"LeafArray\":["
        #     self._browser.MoveTo(branches2)
        #     self._browser.ShowLeafs()
        #     for j in range(self._browser.Count):
        #         j += 1
        #         result += "{\"Name\":\""
        #         result += name_buff+ self._browser.Item(j)
        #         result += "\",\"Type\": \"value"
        #
        #         property_id = [1, 2]
        #         property_id.insert(0, 0)
        #
        #         values, errors = self._server.GetItemProperties(name_buff+self._browser.Item(j), len(property_id) - 1, property_id)
        #         print(values[1])
        #         result+="\",\"Value\": {}".format(str(values[1]))
        #
        #
        #         self.monitorItemsID.append(name_buff+self._browser.Item(j))
        #
        #         result += "}"
        #         if j != self._browser.Count:
        #             result += ","
        #     result += "]}"
        #     if i != brancheCount:
        #         result += ","
        # result += "]"
        # return result


    def FormMonitorItemList(self):
        tree=self.GetTree()

        def getLeafArray(tree):
            for branch in tree:
                if branch['Type']=='folder':
                    for leaf in branch['LeafArray']:
                        self.monitorItemsID.append(leaf['Name'])
                    getLeafArray(branch['BrancheArray'])
                else:
                    self.monitorItemsID.append(branch['Name'])

        getLeafArray(tree)

        # print(self.monitorItemsID)

    def SaveMonitorItemList(self):
        new_excel = xlwt.Workbook()
        ws = new_excel.add_sheet('output_sheet')
        ws.write(0, 0, 'instrumenttag')

        i = 1
        for tag in self.monitorItemsID:
            ws.write(i, 0, tag)
            i += 1

        new_excel.save('MonitorItemTags.xls')






    def AddItemId(self):
        try:
            if self._opcGroupM is not None:
                if self._opcGroupM.OPCItems.Count==0:
                    self._serverHandles=[None]*len(self.monitorItemsID)
                    for i in range(len(self.monitorItemsID)):
                        try:
                            self._serverHandles[i]=self._opcGroupM.OPCItems.AddItem(self.monitorItemsID[i], i).ServerHandle
                        except:
                            pass

                return True
        except Exception as err:
            print('AddItemId Error::', err)

        return False




    def GetItemsFromFile(self):

        def read_sheet(sheet):
            colidx = dict((sheet.cell(0, i).value, i) for i in range(sheet.ncols))
            tags = [sheet.cell(i, colidx["instrumenttag"]).value for i in range(1, sheet.nrows)]

            size=len(tags)

            for tag in tags:
                new_leaf = {'Name': tag,
                            'Type': 'value'}
                try:
                    property_id = [1, 2]
                    property_id.insert(0, 0)

                    values, errors = self._server.GetItemProperties(tag,
                                                                    len(property_id) - 1,
                                                                    property_id)
                    if values[1].__class__.__name__ not in value_types:
                        continue

                    new_leaf['Value'] = values[1]


                    # self.monitorItemsID.append(tag)
                except Exception as err:
                    print('Add item error::', err)
                    continue
                self.Tree.append(new_leaf)

        self.Tree = []

        wb = xlrd.open_workbook(self.inputFile)
        sheet = wb.sheet_by_name(self.inputFileSheet)
        read_sheet(sheet)



    def StartMonitor(self, handlerInit):
        try:
            self.isMonitor=True
            if self.isConnected==False:
                print('connected false')
                return

            if self._server is not None:
                if self._opcGroupM is not None:
                    handler = win32com.client.WithEvents(self._opcGroupM, self._monitorEventHandler)
                    handlerInit(handler)
                    if self.AddItemId():
                        self._opcGroupM.UpdateRate = self.UpdateRate
                        self._opcGroupM.IsActive = True
                        self._opcGroupM.IsSubscribed = True
                    else:
                        print('add item is false')
                else:
                    print('group is none')
            else:
                print('server is None')
        except Exception as err:
            print('Start monitor Error::', err)




    def PingHost(self):
        response = os.system("ping " + self.host)
        if response == 0:
            return True
        else:
            return False

    def CheckConnected(self) -> object:
        result=False
        try:
            ping=self.PingHost()
            if ping==True:
                self._isPingSuccess=True
                if self._server!=None:
                    serverState=int(self._server.ServerState)
                    if serverState==int(win32com.client.constants.OPCRunnig):
                        result=True
            else:
                self._isPingSuccess=False
                self._server=None
        except Exception as err:
            print('CheckConnected error::', err)
            self._isPingSuccess = False
            self._server = None

        return result

    def Connect(self):
        while True:
          try:
            self.CheckConnected()
            if (self._isPingSuccess and self.isConnected==False):
                dll = win32com.client.gencache.EnsureModule(dcom_da.regsvr.get_clsid(), 0, 1, 0)
                self._server=dll.OPCServer()
                self._server.Connect(self.server_name, self.host)
                print('Successfully connected to DA Server on the host {}'.format(self.host))

                self._opcGroupM = win32com.client.Dispatch(self._server.OPCGroups.Add('MonitorGroup'))

                self.isConnected=True

            break
          except Exception as err:
            self._server=None
            print('Failed connect to DA server. Check the settings (server name, host or access rights)\n',
                  err)

    def Disconnect(self):
        try:
            # self.CheckConnected()
            # if self._isPingSuccess and self.isConnected:
            #     if self._server is not None:
            #         self._server.OPCGroups.RemoveAll()
            #         self._server.Disconnect()
            #         print('Successfully disconnected')

            self._server=None
            self._browser=None
            self._opcGroupM=None
            self.isConnected=False
        except Exception as err:
            print('Failed disconnect:', err)




