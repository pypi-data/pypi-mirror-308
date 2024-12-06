from typing import Optional
import os
from galtea.connection.sdk_connection import SDKConnection
from galtea.datasets.dataset_manager import DatasetManager
from galtea.templates.concrete import ConcreteTemplateFactory
from galtea.users.user_manager import UserManager
from galtea.workspaces.workspace_manager import WorkspaceManager


class ArgillaAnnotationTask:

    def __init__(self, argilla_api_url: str = os.getenv("ARGILLA_API_URL"), argilla_api_key: str = os.getenv("ARGILLA_API_KEY")):
        """
        Initialize the ArgillaAnnotationTask class.
        Parameters:
            argilla_api_url (str): The URL of the Argilla API.
            argilla_api_key (str): The API key for the Argilla API.
        """ 
        self._sdk_connection = SDKConnection(argilla_api_url, argilla_api_key)
        self._workspace_manager = WorkspaceManager(self._sdk_connection.client)
        self._user_manager = UserManager(self._sdk_connection.client)
        self._dataset_manager = DatasetManager(self._sdk_connection.client)
        self._template_factory = ConcreteTemplateFactory()


    def create_annotation_task(self, name: str, template_type: str, dataset_path: str, min_submitted: Optional[int] = None, guidelines: Optional[str] = None, users_path_file: Optional[str] = "users.json", show_progress: bool = True, export_records: bool = True) :
        """Based on the template type, this function creates an Argilla annotation task loading the dataset (dataset_path) and creating the task with the given name.

        Parameters:
            name (str): The name of the annotation task.
            template_type (str): The type of the annotation template. (e.g. "ab_testing")
            dataset_path (str): The path to the dataset.
            min_submitted (int): The minimum number users that need to submit annotations to complete the task.
            guidelines (str): The guidelines for the annotation task. Defaults to None.
            users_path_file (str): The path to the users file. Defaults to "users.json".
            show_progress (bool): Whether to show the progress of the dataset. Defaults to True.
        """

        workspace = self._workspace_manager.create_workspace(name)

        self._user_manager.create_users(workspace, users_path_file=users_path_file)

        template = self._template_factory.get_template(name, template_type, min_submitted, guidelines)
        settings = template.build_settings()
        
        self._dataset_manager.create_dataset(name, workspace, settings)
        self._dataset_manager.load_records(template=template, dataset_path=dataset_path)

        progress = self._dataset_manager.get_progress()

        if show_progress:
            print(f"Dataset progress: {progress}")
        
        if progress['completed'] == progress['total'] and export_records:
            from time import strftime
            export_path = f"{self._dataset_manager.dataset.name}_{strftime('%Y-%m-%d_%H-%M-%S')}.json"
            self._dataset_manager.dataset.records.to_json(export_path)
            print(f"Exported dataset to {export_path}")

    
    def get_progress(self, dataset_name: str, workspace_name: str):
        """
        Given a dataset name and a workspace name, this function returns the progress of annotation of the dataset.
        Parameters:
            dataset_name (str): The name of the dataset.
            workspace_name (str): The name of the workspace.
        Returns:
            dict: The progress of the dataset.
            e.g. returns {'total': 10, 'completed': 0, 'pending': 10}
        """
        return self._dataset_manager.get_progress(dataset_name, workspace_name)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass