import os
import requests

from ._enums import *

from typing import (
    List,
    Dict,
    Tuple,
    Any,
    Optional,
)

def trace(func):
    def wrapper(*args, **kwargs):
        print(f"Tracing {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class Interactor():
    def __init__(
        self,
        api_key: str = None,
    ) -> None:
        self._base_url = "http://localhost:8000"
        self._extension = "/interact/"

        if api_key:
            self._api_key = api_key
        else:
            _api_key = os.getenv("INTERACT_API_KEY")
            if _api_key:
                self._api_key = _api_key
            else:
                raise ValueError(
                    "No API key provided. Please pass an API key or set the INTERACT_API_KEY environment variable."
                )
        
        self._headers = {
            "x-api-key": self._api_key,
        }

    def label_request(
        self,
        task_name: str,
        task_type: TaskType,
        instructions: Dict[str, Any] | str,
        labels: List[str],
        priority: int,
        stake: int,
        expiration: int,
        image_type: str = "image/jpeg",
        image_urls: List[str] = [],
        image_data: List[bytes] = [],
    ) -> Dict[str, Any]:
        try:
            if len(image_urls) == 0 and len(image_data) == 0:
                raise ValueError("No image data provided.")
            
            response = requests.post(
                url = self._base_url + self._extension + "task-request/",
                headers = self._headers,
                json = {
                    "task_name": task_name,
                    "task_type": task_type,
                    "instructions": instructions,
                    "labels": labels,
                    "image_urls": image_urls,
                    "image_data": {
                        'extnesion': image_type,
                        'images': image_data,
                    },
                    "priority": priority,
                    "stake": stake,
                    "expiration": expiration,
                },
            )
            return response.json()
        except Exception as e:
            return {
                "error": str(e),
            }


    def design_request(
        self,
        task_name: str,
        task_type: TaskType,
        instructions: Dict[str, Any] | str,
        priority: int,
        stake: int,
        expiration: int,
    ) -> Dict[str, Any]:
        if task_type != TaskType.DESIGN:
            raise ValueError("Invalid task type for design request.")
        try:
            response = requests.post(
                url = self._base_url + self._extension + "task-request/",
                headers = self._headers,
                json = {
                    "task_name": task_name,
                    "task_type": task_type,
                    "instructions": instructions,
                    "priority": priority,
                    "stake": stake,
                    "expiration": expiration,
                },
            )
            return response.json()
        except Exception as e:
            return {
                "error": str(e),
            }


    def status(
        self,
        task_id: str,
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                url = self._base_url + self._extension + "poll-status/",
                headers = self._headers,
                json = {
                    "task_id": task_id,
                },
            )
            return response.json()
        except Exception as e:
            return {
                "error": str(e),
            }


    def results(
            self,
            task_id: str,
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                url = self._base_url + self._extension + "task-results/",
                json = {
                    "task_id": task_id,
                },
                headers = self._headers,
            )
            return response.json()
        except Exception as e:
            return {
                "error": str(e),
            }

