import configparser

class config:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read('configurations.ini')

    def get_username(self):
        return self.parser['Anaplan_auth']['username']

    def get_password(self):
        return self.parser['Anaplan_auth']['password']

    def get_workspaceid(self):
        return self.parser['Anaplan_Workspaceinfo']['workspaceid']

    def get_modelid(self):
        return self.parser['Anaplan_Workspaceinfo']['modelid']

    def filepath(self):
        return self.parser['Logger']['logfilepath']

    def getExportProcesses(self):
        return self.parser['ExportProcesses']['Process']

    def getImportProcesses(self):
        return self.parser['ImportProcesses']['Process']

    def getDownloadFiles(self):
        return self.parser['DownloadFile']['downloadFile']

    def getUploadFiles(self):
        return self.parser['UploadFile']['uploadFile']

    def getLocation(self):
        return self.parser['FileLocation']['location']
