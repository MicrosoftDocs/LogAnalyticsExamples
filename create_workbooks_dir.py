# Python program to explain os.mkdir() method 
  
# importing os module 
import os, shutil, glob

mode = 0o666

#for listedItem in os.listdir('.'):
#    if os.path.isdir(listedItem):
#        print('working on: ', listedItem)
#        wb_path = os.path.join(listedItem, "workbooks")
#        if os.path.isdir(wb_path):
#            print("Directory '%s' already exists" % wb_path)
#        else:
#            os.mkdir(wb_path, mode) 
#            print("Directory '%s' created" % wb_path)
#        
#        for filePath in glob.glob(listedItem + '\*'):
#            if filePath != "workbooks" and filePath!= wb_path:
#                print("moving: ", filePath, " to: ", wb_path)
#                shutil. move(filePath, wb_path)


for listedItem in os.listdir('.'):
    if os.path.isdir(listedItem):
        print('working on: ', listedItem)
        queriesPath = os.path.join(listedItem, "Queries")
        alertsPath = os.path.join(listedItem, "Alerts")
        if os.path.isdir(queriesPath):
            if not os.listdir(queriesPath):
                print("Directory '%s' exists and empty, writing readme file" % queriesPath)
                with open(os.path.join(queriesPath, "README"), "w") as file:
                    file.write("Put Log Analytics queries in this folder")
        else:
            os.mkdir(queriesPath, mode) 
            print("Directory '%s' created" % queriesPath)
        
        if os.path.isdir(alertsPath):
            if not os.listdir(alertsPath):
                print("Directory '%s' exists and empty, writing readme file" % alertsPath)
                with open(os.path.join(alertsPath, "README"), "w") as file:
                    file.write("Put alerts in this folder")
        else:
            os.mkdir(alertsPath, mode) 
            print("Directory '%s' created" % alertsPath)