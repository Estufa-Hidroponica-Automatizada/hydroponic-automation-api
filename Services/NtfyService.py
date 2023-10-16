import requests


class NtfyService():
    def __init__(self, url, topic):
        self.url = url
        self.topic = topic

    def send_notification(self, message, title, priority, tags):
            response = requests.post(f"{self.url}/{self.topic}",
                                     data=message.encode(encoding='utf-8'),
                                     headers={
                                        "Title": title,
                                        "Priority": priority,
                                        "Tags": tags
                                     })
        
ntfyService = NtfyService("http://192.168.15.10:8000", "estufa")