from Authentication import BasicAuthentication
from getinfoanaplan import GetInfoFromAnaplan
from Configurations_info import config
from log import log_information
from flask import Flask

app = Flask(__name__)

@app.route('/')
def mainWork():
        basic_auth = BasicAuthentication()
        get_info = GetInfoFromAnaplan()
        config_info = config()
        log_details = log_information()

        userName = config_info.get_username()
        password = config_info.get_password()
        filepath =config_info.filepath()
        log_info = log_details.log()

        authToken,expiresAt, bAuth_FLAG = basic_auth.bAuth(userName, password, log_info)
        #expiresAt, authToken, Validate_FLAG = basic_auth.refresh(expiresAt, authToken, log_info)

        if bAuth_FLAG:
                workspaceId = config_info.get_workspaceid()
                modelId = config_info.get_modelid()

                getworkspaces = get_info.getWorkspaces(authToken,log_info)
                validateworkspaces,workspace_Flag = get_info.validateWorkspaces(workspaceId, getworkspaces,log_info)

                if workspace_Flag:
                        getmodels = get_info.getModels(authToken,log_info)
                        validatemodel, model_Flag = get_info.validateModels( modelId, getmodels,log_info)

                        if model_Flag:
                                ExportProcess = config_info.getExportProcesses().split(',')
                                Process = get_info.GetProcess(authToken, workspaceId, modelId,log_info)
                                getProcess = get_info.FilterProcess(ExportProcess, Process, log_info)
                                for processID in getProcess:
                                        taskID = get_info.startProcess(authToken, processID, workspaceId, modelId, log_info)
                                        get_info.checkProcessStatus(authToken, workspaceId, modelId, processID, taskID, log_info)

                                downloadFiles = config_info.getDownloadFiles().split(',')

                                Files = get_info.getFilesFromAnaplan(authToken, workspaceId, modelId, log_info)

                                downloadFilesDetail = get_info.filterFiles(Files, downloadFiles, log_info)
                                #downloadLocation = config_info.getLocation()

                                uploadFiles = config_info.getUploadFiles().split(',')
                                uploadFilesDetail = get_info.filterFiles(Files, uploadFiles, log_info)

                                for file in downloadFilesDetail:
                                        chunk = get_info.getChuckCount(authToken, workspaceId, modelId, file['id'], log_info)
                                        df = get_info.downloadChunks(authToken, workspaceId, modelId, file['id'], file['name'], chunk, log_info)

                                for file in uploadFilesDetail:
                                        get_info.setChunkCount(authToken, workspaceId, modelId, file, log_info)
                                        get_info.uploadFile(authToken, workspaceId, modelId, file, df, log_info)

                                ImportProcess = config_info.getImportProcesses().split(',')
                                getProcess = get_info.FilterProcess(ImportProcess, Process, log_info)
                                for processID in getProcess:
                                        taskID = get_info.startProcess(authToken, processID, workspaceId, modelId,log_info)
                                        get_info.checkProcessStatus(authToken, workspaceId, modelId, processID, taskID,log_info)

        return "Integration Ran Successfully"

if __name__ == "__main__":
        #mainWork()
        app.run();
