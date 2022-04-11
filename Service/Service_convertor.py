# import time
# import sys
# import win32serviceutil
# import win32service
# import servicemanager
#
#
# class MyService:
#     def stop(self):
#         self.running = False
#
#     def run(self):
#         self.running = True
#         while self.running:
#             time.sleep(8)
#             servicemanager.LogInfoMsg("Service running...")
#
#
# class ServiceConvertor(win32serviceutil.ServiceFramework):
#     _svc_name_ = 'Convertor_Service'
#     _svc_display_name_ = 'This service of convertor'
#
#     def SvcStop(self):
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         self.service_impl.stop()
#         self.ReportServiceStatus(win32service.SERVICE_STOPPED)
#
#     def SvcDoRun(self):
#         self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
#         self.service_impl = MyService()
#         self.ReportServiceStatus(win32service.SERVICE_RUNNING)
#         self.service_impl.run()
#
