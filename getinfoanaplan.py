import time
import requests
import json
import pandas as pd
from io import StringIO

class GetInfoFromAnaplan:
    def getWorkspaces(self, authToken,logging):
        try:
            logging.info("Workspace generation STARTED")
            auth_url = 'https://api.anaplan.com/2/0/workspaces/'
            auth_json = requests.get(
                url=auth_url,
                headers={
                    'Authorization': authToken
                }
            ).json()
            if auth_json['status']['message'] == 'Success':
                logging.info("Workspace generation COMPLETED")
                return [workspace['id'] for workspace in auth_json['workspaces']]
            else:
                logging.info("You DON'T have access to the workspace, try with other one")
        except Exception as K:
            logging.exception(K)

    def validateWorkspaces(self, workspaceId, workspaces,logging):
        try:
            logging.info("Workspace validation STARTED")
            if workspaceId in workspaces:
                logging.info("Workspace validation COMPLETED")
                return workspaceId,True
            else:
                logging.info("Workspace validation FAILED")
                return None,False;
        except Exception as K:
            logging.exception(K)

    def getModels(self, authToken,logging):
        try:
            logging.info("modelinfo generation STARTED")
            #authToken = authToken
            auth_url = 'https://api.anaplan.com/2/0/models'
            auth_json = requests.get(
                url=auth_url,
                headers={
                    'Authorization': authToken
                }
            ).json()
            if auth_json['status']['message'] == 'Success':
                logging.info("modelinfo generation COMPLETED")
                return [model['id'] for model in auth_json['models']]
        except Exception as K:
            logging.exception(K)

    def validateModels(self,modelId,models,logging):
        try:
            logging.info("model validation STARTED")
            if modelId in models:
                logging.info("Model validation COMPLETED")
                return modelId,True
            else:
                logging.info("Model validation FAILED")
                return None,False
        except Exception as K:
            logging.exception(K)

    def GetFiles(self, authToken,workspaceID,modelID,logging):
        try:
            logging.info("Generating Files, which are to be uploaded/downloaded info STARTED")
            auth_url = 'https://api.anaplan.com/2/0/workspaces/{0}/models/{1}/files'.format(workspaceID, modelID)
            auth_json = requests.get(
                url=auth_url,
                headers={
                    'Authorization': authToken
                }
            ).json()
            if auth_json['status']['message'] == 'Success':
                logging.info("Generating Files, which are to be uploaded/downloaded info COMPLETED")
                return auth_json['files']
            else:
                logging.info("Generating Files, which are to be uploaded/downloaded info FAILED")
        except Exception as K:
            logging.exception(K)

    def GetProcess(self, authToken,workspaceID,modelID,logging):
        try:
            logging.info("Process generation STARTED")
            auth_url = 'https://api.anaplan.com/2/0/workspaces/{0}/models/{1}/processes'.format(workspaceID, modelID)
            auth_json = requests.get(
                url=auth_url,
                headers={
                    'Authorization': authToken
                }
            ).json()

            if auth_json['status']['message'] == 'Success':
                logging.info("process generation COMPLETED")
                return auth_json['processes']
            else:
                logging.info("process generation FAILED")
        except Exception as K:
            logging.exception(K)

    def FilterProcess(self, configProcess, anaplanProcess, logging):
        try:
            logging.info("Filtering Process from config STARTED")
            result = []
            for confProcess in configProcess:
                for anaPro in anaplanProcess:
                    if confProcess == anaPro['name']:
                        result.append(anaPro['id'])
            logging.info("Filtering Process from config COMPLETED")
            return result
        except Exception as K:
            logging.exception(K)

    def startProcess(self, authToken, processID, workspaceID, modelID, logging):
        try:
            logging.info(f"Process ID {processID} STARTED")
            auth_url = f"https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/processes/{processID}/tasks"
            auth_json = requests.post(
                url=auth_url,
                headers={
                    'Authorization': authToken,
                    'Content-type': 'application/json'
                },
                data = json.dumps({'localeName': 'en_US'})
            ).json()

            if auth_json['status']['message'] == 'Success':
                logging.info(f"Process ID {processID} COMPLETED")
                return auth_json['task']['taskId']
            else:
                logging.info(auth_json)
                logging.info("process generation FAILED")
        except Exception as K:
            logging.exception(K)

    def checkProcessStatus(self, authToken, workspaceID, modelID, processID, taskID, logging):
        try:
            logging.info(f"Check the status of Process {processID} STARTED")
            auth_url = f"https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/processes/{processID}/tasks/{taskID}"
            auth_json = requests.get(
                url=auth_url,
                headers={
                    'Authorization': authToken,
                    'Content-type': 'application/json'
                }
            ).json()
            if auth_json['task']['currentStep'] == "Failed.":
                logging.info(auth_json)
            elif auth_json['task']['currentStep'] != "Complete.":
                logging.info(auth_json['task']['currentStep'])
                time.sleep(15.0)
                self.checkProcessStatus(authToken, workspaceID, modelID, processID, taskID, logging)
            else:
                logging.info(auth_json['task']['currentStep'])
                logging.info(f"Check the status of Process {processID} COMPLETED")
                return None;
        except Exception as K:
            logging.exception(K)

    def getFilesFromAnaplan(self, authToken, workspaceID, modelID, log):
        try:
            log.info("Extracting Files from Anaplan STARTED")
            url = f"https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/files/"
            getFileData = requests.get(
                url = url,
                headers = {
                    'Authorization': authToken
                }
            )
            getFileData_json = getFileData.json()
            #print(getFileData_json)

            if getFileData_json['status']['message'] == 'Success':
                file_info = getFileData_json['files'];
                log.info("Extracting Files from Anaplan COMPLETED")
            else:
                log.info("Extracting Files from Anaplan FAILED")
        except Exception as e:
            log.info(e)
        finally:
            return file_info

    def filterFiles(self, anaFiles, confFiles, log):
        filteredFile = []
        try:
            log.info("Filtering Files from config STARTED")
            for confFile in confFiles:
                for anaFile in anaFiles:
                    if confFile == anaFile['name']:
                        filteredFile.append(anaFile)
                        log.info("Filtering Files from config COMPLETED")
        except Exception as e:
            log.info(e)
        finally:
            return filteredFile;

    def getChuckCount(self, authToken, workspaceID, modelID, fileID, log):
        try:
            log.info(f"Getting the chunk count of {fileID} STARTED")
            url = f"https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/files/{fileID}/chunks/"
            getChunk = requests.get(
                url,
                headers = {
                    'Authorization': authToken,
                    "Content-Type": "application/json"
                }
            )
            getChunk = getChunk.json()
            if getChunk['status']['message'] == "Success":
                log.info(f"Getting the chunk count of {fileID} COMPLETED")
        except Exception as e:
            log.info(e)
        finally:
            return getChunk['chunks'];

    def downloadChunks(self, authToken, workspaceID, modelID, fileID, fileName, chunks, log):
        try:
            log.info(f"{fileName} download STARTED")
            for chunk in chunks:
                url = f"https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/files/{fileID}/chunks/{chunk['id']}"
                getChunk = requests.get(
                    url,
                    headers = {
                        'Authorization': authToken,
                        "Content-Type": "application/json"
                    }
                )
                df = pd.read_csv(StringIO(getChunk.text), sep=",", index_col=['Time'])
                df['Predict'] = 5
                log.info(f"{fileName} download COMPLETED")
            return df
        except Exception as e:
            log.info(e)

    def setChunkCount(self, authToken, workspaceID, modelID, file, log, chunkCount=-1):
        try:
            updatedFile = []
            log.info(f"Setting chunk count to -1 for {file['name']} STARTED")
            fileID = file['id']
            file['chunkCount'] = chunkCount
            fileData = file
            url = f'https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/files/{fileID}'
            getFileData = requests.post(
                url = url,
                headers = {
                    'Authorization': authToken,
                    'Content-Type': 'application/json'
                },
                json = fileData
            )
            getFileData = getFileData.json()

            if getFileData['status']['message'] == 'Success':
                log.info(f"Setting chunk count to -1 for {file['name']} COMPLETED")
                updatedFile.append(getFileData['file']);
            else:
                log.info(f"Getting files API Call for {file['name']} FAILED")
        except Exception as e:
            log.info(e)
        finally:
            return updatedFile;

    def uploadFile(self, authToken, workspaceId, modelId, file, df, log):
        try:
            csv = df.to_csv()
            tempFileName = file['name']
            log.info(f"Reading the Configuration file {tempFileName}")
            log.info(f"'{tempFileName}' Upload Started")
            fileID = file['id']

            url = f'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileID}/chunks/0'
            requests.put(
                url,
                headers = {
                    'Authorization': authToken,
                    'Content-Type': 'application/octet-stream'
                },
                data = csv
            )
            log.info(f"'{tempFileName}' Upload Completed")

            log.info(f"{tempFileName} started marking as complete")
            # Mark Upload as complete
            url = f'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileID}/complete'
            fileCompleteResponse = requests.post(
            url,
            headers = {
                'Authorization': authToken,
                'Content-Type': 'application/json'
            },
            json = file
            )
            fileCompleteResponse = fileCompleteResponse.json()

            if fileCompleteResponse['status']['message'] == "Success":
                log.info(f"{tempFileName} started MARKED as complete")
            else:
                log.info(f"Problem in updating the file {tempFileName}  as complete")
        except Exception as e:
            log.info(e)