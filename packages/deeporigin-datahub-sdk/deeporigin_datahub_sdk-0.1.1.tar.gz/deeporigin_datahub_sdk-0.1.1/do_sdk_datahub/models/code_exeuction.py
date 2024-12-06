from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.code_exeuction_code_language import CodeExeuctionCodeLanguage
from ..models.code_exeuction_status import CodeExeuctionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CodeExeuction")


@_attrs_define
class CodeExeuction:
    """
    Attributes:
        id (str): Deep Origin system ID.
        status (CodeExeuctionStatus):
        start_date (Union[Unset, str]):
        finished_date (Union[Unset, str]):
        created_by_user_drn (Union[Unset, str]):
        code (Union[Unset, str]):
        code_language (Union[Unset, CodeExeuctionCodeLanguage]):
        result_uri (Union[Unset, str]):
        execution_error_message (Union[Unset, str]):
    """

    id: str
    status: CodeExeuctionStatus
    start_date: Union[Unset, str] = UNSET
    finished_date: Union[Unset, str] = UNSET
    created_by_user_drn: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    code_language: Union[Unset, CodeExeuctionCodeLanguage] = UNSET
    result_uri: Union[Unset, str] = UNSET
    execution_error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        status = self.status.value

        start_date = self.start_date

        finished_date = self.finished_date

        created_by_user_drn = self.created_by_user_drn

        code = self.code

        code_language: Union[Unset, str] = UNSET
        if not isinstance(self.code_language, Unset):
            code_language = self.code_language.value

        result_uri = self.result_uri

        execution_error_message = self.execution_error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
            }
        )
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if finished_date is not UNSET:
            field_dict["finishedDate"] = finished_date
        if created_by_user_drn is not UNSET:
            field_dict["createdByUserDrn"] = created_by_user_drn
        if code is not UNSET:
            field_dict["code"] = code
        if code_language is not UNSET:
            field_dict["codeLanguage"] = code_language
        if result_uri is not UNSET:
            field_dict["resultUri"] = result_uri
        if execution_error_message is not UNSET:
            field_dict["executionErrorMessage"] = execution_error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        status = CodeExeuctionStatus(d.pop("status"))

        start_date = d.pop("startDate", UNSET)

        finished_date = d.pop("finishedDate", UNSET)

        created_by_user_drn = d.pop("createdByUserDrn", UNSET)

        code = d.pop("code", UNSET)

        _code_language = d.pop("codeLanguage", UNSET)
        code_language: Union[Unset, CodeExeuctionCodeLanguage]
        if isinstance(_code_language, Unset):
            code_language = UNSET
        else:
            code_language = CodeExeuctionCodeLanguage(_code_language)

        result_uri = d.pop("resultUri", UNSET)

        execution_error_message = d.pop("executionErrorMessage", UNSET)

        code_exeuction = cls(
            id=id,
            status=status,
            start_date=start_date,
            finished_date=finished_date,
            created_by_user_drn=created_by_user_drn,
            code=code,
            code_language=code_language,
            result_uri=result_uri,
            execution_error_message=execution_error_message,
        )

        code_exeuction.additional_properties = d
        return code_exeuction

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
