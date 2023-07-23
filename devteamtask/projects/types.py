from typing import TypedDict, Union
from uuid import UUID

TagCreationDataType = TypedDict("TagCreationDataType", {"name": str, "project_id": str})

StatusCreationDataType = TypedDict("StatusCreationDataType", {"name": str, "project_id": Union[UUID, str]})
