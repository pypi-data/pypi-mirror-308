from typing import Optional
from pinecone_plugins.assistant.data.core.client.model.assistant_file_model import AssistantFileModel as OpenAIFileModel

class FileModel:
    def __init__(self, file_model: Optional[OpenAIFileModel] = None, data: dict[str, any] = None):
        if data:
            self.data_init(data)
        else:
            self.file_model_init(file_model)

    def data_init(self, data: dict[str, any]):
        self.data = data
        self.name = data.get("name")
        self.id = data.get("id")
        self.metadata = data.get("metadata")
        self.created_on = data.get("created_on")
        self.updated_on = data.get("updated_on")
        self.status = data.get("status")
        self.percent_done = data.get("percent_done")
        self.signed_url = data.get("signed_url")
    
    def file_model_init(self, file_model: OpenAIFileModel):
        self.data_init(
            {
                "name": file_model.name,
                "id": file_model.id,
                "metadata": file_model.metadata,
                "created_on": file_model.created_on,
                "updated_on": file_model.updated_on,
                "status": file_model.status,
                "percent_done": file_model.percent_done,
                "signed_url": file_model.signed_url
            }
        )

    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return repr(self.data)
