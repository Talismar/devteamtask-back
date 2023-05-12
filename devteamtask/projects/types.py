from typing import TypedDict

TagCreationDataType = TypedDict("TagCreationDataType", {
    "name": str,
    "project_id": int
})

StatusCreationDataType = TypedDict("StatusCreationDataType", {
    "name": str,
    "project_id": int
})
