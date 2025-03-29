from pydantic import BaseModel

class TemplateOnly(BaseModel):
    template_name: str
