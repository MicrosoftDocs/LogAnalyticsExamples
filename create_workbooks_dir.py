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
        WBAlertsPath = os.path.join(listedItem, "Workbooks", "Alerts")
        if os.path.isdir(WBAlertsPath):
            print("Directory '%s' exists, checking if empty..." %WBAlertsPath)
            if not os.listdir(WBAlertsPath):
                print("folder is empty, removing")
                os.removedirs(WBAlertsPath)
            else:
                print("folder not empty")   
        else:
            print("Directory %s doesn't exist" %WBAlertsPath)

for listedItem in os.listdir('.'):
    if os.path.isdir(listedItem):
        print('working on: ', listedItem)
        WBQueriesPath = os.path.join(listedItem, "Workbooks", "Queries")
        if os.path.isdir(WBQueriesPath):
            print("Directory '%s' exists, checking if empty..." %WBQueriesPath)
            if not os.listdir(WBQueriesPath):
                print("folder is empty, removing")
                os.removedirs(WBQueriesPath)
            else:
                print("folder not empty")   
        else:
            print("Directory %s doesn't exist" %WBQueriesPath)