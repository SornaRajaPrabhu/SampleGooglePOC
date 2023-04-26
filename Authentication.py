import requests
import time

class BasicAuthentication:

    def bAuth(self, userName, password, log_info):
        try:
            log_info.info("Token generation STARTED")
            auth_url = 'https://auth.anaplan.com/token/authenticate'
            auth_json = requests.post(
                url=auth_url,
                auth=(userName, password)
            ).json()
            if auth_json['status'] == 'SUCCESS':
                tokenValue = auth_json['tokenInfo']['tokenValue']
                log_info.info("Token generation COMPLETED")
                return self.validate('AnaplanAuthToken ' + tokenValue, log_info)
            else:
                return None,None, False
        except Exception as K:
            log_info.exception(K)

    def validate(self, authToken, log_info):
        try:
            log_info.info("Token validation STARTED")
            auth_url = 'https://auth.anaplan.com/token/validate'
            auth_json = requests.get(
                url=auth_url,
                headers={
                    'Authorization': authToken
                }
            ).json()
            if auth_json['status'] == 'SUCCESS':
                expiresAt = auth_json['tokenInfo']['expiresAt']
                log_info.info("Token validation COMPLETED")
                return authToken,expiresAt, True
            else:
                return None,None, False
        except Exception as K:
            log_info.exception(K)

    def refresh(self,expiresAt,authToken,log_info):
        try:
            current_time = time.time()

            if expiresAt > current_time:
                return expiresAt,authToken,True
            else:
               log_info.info("Token Refreshing STARTED")
               auth_url = 'https://auth.anaplan.com/token/refresh'
               auth_json = requests.post(
                   url=auth_url,
                   headers={
                       'Authorization': authToken
                   }
               ).json()
               log_info.info(auth_json['statusMessage'])
               if auth_json['status'] == 'SUCCESS':
                   tokenValue = auth_json['tokenInfo']['tokenValue']
                   log_info.info("Token Refreshing COMPLETED")
                   return self.validate('AnaplanAuthToken ' + tokenValue, log_info)
               else:
                   return None,None,False

        except Exception:
            log_info.exception(Exception)
