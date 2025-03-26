from typing import Any, Optional, List, Dict
from fastapi.responses import JSONResponse
from math import ceil
from datetime import datetime

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

class ResponseSchema:
    def __init__(
        self,
        status: bool = True,
        message: str = "Success",
        data: Any = None,
        status_code: int = 200
    ):
        self.status = status
        self.message = message
        self.data = data
        self.status_code = status_code

    def dict(self) -> dict:
        return {
            "status": self.status,
            "message": self.message,
            "data": self._process_data(self.data),
            "status_code": self.status_code
        }
    
    def _process_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._process_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_data(item) for item in data]
        elif isinstance(data, datetime):
            return datetime_handler(data)
        return data

class PaginationSchema:
    def __init__(
        self,
        data: List[Any],
        total: int,
        page: int = 1,
        per_page: int = 10,
    ):
        self.data = data
        self.total = total
        self.page = page
        self.per_page = per_page
        self.total_pages = ceil(total / per_page)
        self.has_next = page < self.total_pages
        self.has_prev = page > 1

    def dict(self) -> dict:
        return {
            "data": self._process_data(self.data),
            "meta": {
                "page": self.page,
                "per_page": self.per_page,
                "total_items": self.total,
                "total_pages": self.total_pages,
                "has_next": self.has_next,
                "has_prev": self.has_prev
            }
        }
    
    def _process_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._process_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_data(item) for item in data]
        elif isinstance(data, datetime):
            return datetime_handler(data)
        return data

def create_response(
    status: bool = True,
    message: str = "Success",
    data: Any = None,
    status_code: int = 200
) -> JSONResponse:
    response = ResponseSchema(
        status=status,
        message=message,
        data=data,
        status_code=status_code
    )
    return JSONResponse(
        content=response.dict(),
        status_code=status_code
    )

def create_pagination_response(
    data: List[Any],
    total: int,
    page: int = 1,
    per_page: int = 10,
    message: str = "Success",
    status_code: int = 200
) -> JSONResponse:
    pagination = PaginationSchema(
        data=data,
        total=total,
        page=page,
        per_page=per_page
    )
    response = ResponseSchema(
        status=True,
        message=message,
        data=pagination.dict(),
        status_code=status_code
    )
    return JSONResponse(
        content=response.dict(),
        status_code=status_code
    ) 