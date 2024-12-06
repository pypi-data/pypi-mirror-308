import requests

class TextdripAPI:
    def __init__(self):
        self.base_url = 'https://api.textdrip.com'
    
    def login(self, email, password):
        url = f"{self.base_url}/api/login"
        headers = self.get_api_headers()
        payload = {"email": email, "password": password}
        response = self.get_response(api_url=url,headers=headers,data=payload)
        return response
       
    def get_profile(self, token):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        api_url = f"{self.base_url}/api/profile"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers)
        return response
          
    def get_campaign(self,token):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        api_url = f"{self.base_url}/api/get-campaign"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers)
        return response
    
    def create_contact(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=['name', 'phone', 'email', 'birthdate', 'address'], data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/create-contact"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def add_campaign(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=['contact_id', 'campaign_id'],data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/add-campaign"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def get_key_values(self, required_fields=[], data={}):
        for field in required_fields:
            if field not in data or not data[field]:
                return False
            if isinstance(data[field], list):
                for item in data[field]:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if not value: 
                                return False
                    elif not item:
                        return False
        return True

    def get_conversations(self,token):
        if not self.get_token:return {"success": False, "error": "Token Required"} 
        
        api_url = f"{self.base_url}/api/get-conversations"
        headers = self.get_api_headers(token=token)
        data = {
            "search": "",
            "page": "1"
        }
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
       
    def get_chats(self, token, phone_number, phone_token, page="1"):
        if not self.get_token(token):
            return {"success": False, "error": "Token Required"}

        api_url = f"{self.base_url}/api/get-chats"
        headers = self.get_api_headers(token=token, phone_token=phone_token)
        data = {
            "phone": phone_number,
            "page": page
        }
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def send_messgae(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/send-message"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def archive_chat(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/archive-chat"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def get_quick_response(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        api_url = f"{self.base_url}/api/get-quick-response"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def add_schedule(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/add-schedule"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def assigned_contact(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/assigned-contact"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def get_contact_details(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/get-contact-detail"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def get_all_tags(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        api_url = f"{self.base_url}/api/get-all-tags"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def get_drip_messages(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/get-drip-messages"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def create_contact_with_tag(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=['name'],data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/create-contact-with-tag"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def contact_update(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/contact-update"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def get_phone_list(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        api_url = f"{self.base_url}/api/get-phone-list"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers)
        return response
    

    def check_delivery_rate(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/check-delivery-rate"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def default_number_setup(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/default-number-setup"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def get_image(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/get-images"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def delete_image(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/delete-image"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def upload_image(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/upload-image"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    

    def get_pipeline(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        api_url = f"{self.base_url}/api/get-pipeline"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers)
        return response
    
    def contact_pipeline(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/contact-pipeline"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def bulk_create_contact(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/bulk-create-contact"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def bulk_create_contact_with_tag(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/bulk-create-contact"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response
    
    def remove_campaign(self,token,data={}):
        if not self.get_token(token):return {"success": False, "error": "Token Required"}
        if not self.get_key_values(required_fields=list(data.keys()),data=data):
            return {"success": False, "error": "Missing required fields"}
        api_url = f"{self.base_url}/api/remove-campaign"
        headers = self.get_api_headers(token=token)
        response = self.get_response(api_url=api_url,headers=headers,data=data)
        return response

    def get_token(self,token):
        return True if token else False 
    
    def get_api_headers(self, **kwargs):
        headers = {
            'Authorization': f"Bearer {kwargs.get('token', '')}" if kwargs.get('token', '') else '',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'phone-token': f"Bearer {kwargs.get('phone_token', '')}" if kwargs.get('phone_token', '') else '',
        }  
        return headers
    
    def get_response(self,**kwargs):
        try:
            response = requests.post(url=kwargs.get('api_url',''), headers=kwargs.get('headers',''),json=kwargs.get('data',''))
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}


    
    
    



    