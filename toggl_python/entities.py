from datetime import datetime, timezone
from typing import Callable, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_serializer


class BaseEntity(BaseModel):
    id: Optional[int] = None
    at: Optional[datetime] = None

    def __eq__(self, value: object, /) -> bool:
        return super().__eq__(value)

    @field_serializer("at")
    def _serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        else:
            return dt.astimezone().replace(microsecond=0).isoformat()


class Client(BaseEntity):
    name: str
    wid: int
    notes: Optional[str] = None


class Group(BaseEntity):
    name: str
    wid: int = Field(alias="workspace_id")


class Project(BaseEntity):
    name: str
    wid: int
    cid: Optional[int] = None
    active: bool = True
    is_private: bool = True
    template: Optional[bool] = None
    template_id: Optional[int] = None
    billable: Optional[bool] = True
    auto_estimates: Optional[bool] = False
    estimated_hours: Optional[int] = None
    color: Union[str, int] = 0
    rate: Optional[float] = None
    created_at: Optional[datetime] = None

    @field_serializer("created_at")
    def _serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        else:
            return dt.astimezone().replace(microsecond=0).isoformat()


class ProjectUser(BaseEntity):
    pid: int
    uid: int
    wid: int
    notes: Optional[str] = None
    manage: Optional[bool] = False
    rate: Optional[float] = None
    full_name: Optional[float] = None


class Tag(BaseEntity):
    name: str
    wid: int = Field(alias="workspace_id")


class Task(BaseEntity):
    name: str
    pid: int = Field(alias="project_id")
    wid: int = Field(alias="workspace_id")
    uid: Optional[int] = Field(alias="user_id", default=None)
    estimated_seconds: Optional[int] = None
    tracked_seconds: Optional[int] = None
    active: Optional[bool] = True


class TimeEntry(BaseEntity):
    wid: int
    pid: Optional[int] = None
    tid: Optional[int] = None
    description: Optional[str] = None
    billable: Optional[bool] = False
    start: Union[datetime, Callable[[], datetime]] = datetime.now(timezone.utc)
    stop: Optional[Union[datetime, Callable[[], datetime]]] = None
    duration: int
    created_with: Optional[str] = None
    tags: List[str] = []
    duronly: Optional[bool] = None

    @field_serializer("start", "stop")
    def _serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        else:
            return dt.astimezone().replace(microsecond=0).isoformat()
    
    def __hash__(self):
        return hash((self.wid,self.duration,self.id,self.pid,self.description))



class ReportTimeEntry(BaseEntity):
    wid: Optional[int] = None
    pid: Optional[int] = None
    tid: Optional[int] = None
    uid: Optional[int] = None
    description: Optional[str] = None
    billable: Optional[int] = False
    is_billable: Optional[bool] = False
    cur: Optional[Union[str, bool]] = False
    start: Union[datetime, Callable[[], datetime]] = datetime.now(timezone.utc)
    end: Optional[Union[datetime, Callable[[], datetime]]] = None
    dur: int
    tags: List[str] = []

    @field_serializer("start", "end")
    def _serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        else:
            return dt.astimezone().replace(microsecond=0).isoformat()


class Workspace(BaseEntity):
    name: str
    premium: bool
    admin: bool
    default_hourly_rate: Optional[float] = None
    default_currency: str
    only_admins_may_create_projects: bool
    only_admins_see_billable_rates: bool
    rounding: int
    rounding_minutes: int
    logo_url: Optional[HttpUrl] = None


class User(BaseEntity):
    api_token: Optional[str] = None
    default_wid: Optional[int] = Field(alias="default_workspace_id", default=None)
    email: EmailStr
    fullname: str
    beginning_of_week: int = 0
    image_url: Optional[HttpUrl] = None
    openid_enabled: Optional[bool] = None
    timezone: Optional[str] = None
    country_id: Optional[int] = None
    projects: Optional[Project] = None
    tags: Optional[Tag] = None
    tasks: Optional[Task] = None
    time_entries: Optional[TimeEntry] = None
    updated_at: str
    workspaces: Optional[Workspace] = None


class WorkspaceUser(BaseEntity):
    uid: int
    wid: int
    admin: bool
    active: bool
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    invite_url: Optional[HttpUrl] = None


class Activity(BaseEntity):
    user_id: int
    project_id: int
    duration: int
    description: str
    stop: datetime
    tid: int


class MostActiveUser(BaseEntity):
    user_id: int
    duration: int


class Dashboard(BaseEntity):
    most_active_user: List[MostActiveUser] = []
    activity: List[Activity]
