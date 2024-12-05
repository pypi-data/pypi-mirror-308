from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt


class UserRole(Enum):
    member = "member"
    admin = "admin"


class EmployeeCount(Enum):
    field_1_10 = "1-10"
    field_11_50 = "11-50"
    field_51_200 = "51-200"
    field_201_500 = "201-500"
    field_501_1000 = "501-1000"
    field_1001_5000 = "1001-5000"
    field_5001_10000 = "5001-10000"
    field_10001_ = "10001+"


class LinkedinCompanyPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    company: str = Field(..., description="Company Alias or URL", examples=["openai"], title="Company")


class LinkedinGroupMemberRole(Enum):
    owner = "owner"
    manager = "manager"
    non_member = "non_member"


class LinkedinGroupPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    group: str = Field(..., description="Group URN or URL", examples=["3990648"], title="Group")


class LinkedinOfficeLocation(BaseModel):
    field_type: Optional[str] = Field("LinkedinOfficeLocation", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    is_headquarter: Optional[bool] = Field(False, title="Is Headquarter")
    location: Optional[str] = Field(None, title="Location")
    description: Optional[str] = Field(None, title="Description")
    latitude: Optional[float] = Field(None, title="Latitude")
    longitude: Optional[float] = Field(None, title="Longitude")


class LinkedinPostCommentsSort(Enum):
    relevance = "relevance"
    recent = "recent"


class LinkedinProfileStatus(Enum):
    open_to_work = "open_to_work"
    hiring = "hiring"


class LinkedinReactionType(Enum):
    like = "like"
    interest = "interest"
    empathy = "empathy"
    praise = "praise"
    appreciation = "appreciation"
    entertainment = "entertainment"


class LinkedinSearchEducationsPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    name: str = Field(..., description="Education name", examples=["Harward"], title="Name")
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinSearchIndustriesPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    name: str = Field(..., description="Industry name", examples=["IT"], title="Name")
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinSearchLocationsPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    name: str = Field(..., description="Location name", examples=["Tokyo"], title="Name")
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinURNPrefix(Enum):
    fsd_company = "fsd_company"
    fsd_group = "fsd_group"
    fsd_profile = "fsd_profile"
    fsd_skill = "fsd_skill"
    activity = "activity"
    comment = "comment"
    company = "company"
    group = "group"
    geo = "geo"
    member = "member"
    industry = "industry"
    ugcPost = "ugcPost"


class TypeActivity(Enum):
    activity = "activity"


class LinkedinURNLiteralActivity(BaseModel):
    type: Literal["activity"] = Field(..., title="Type")
    value: str = Field(..., title="Value")


class Type1(Enum):
    company = "company"


class LinkedinURNLiteralCompany(BaseModel):
    type: Literal["company"] = Field(..., title="Type")
    value: str = Field(..., title="Value")


class Type2(Enum):
    fsd_company = "fsd_company"
    company = "company"


class LinkedinURNLiteralFsdCompanyCompany(BaseModel):
    type: Type2 = Field(..., title="Type")
    value: str = Field(..., title="Value")


class Type3(Enum):
    fsd_profile = "fsd_profile"


class LinkedinURNLiteralFsdProfile(BaseModel):
    type: Literal["fsd_profile"] = Field(..., title="Type")
    value: str = Field(..., title="Value")


class LinkedinUserBirthDate(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserBirthDate", alias="@type", title="Entity Type")
    day: int = Field(..., title="Day")
    month: int = Field(..., title="Month")


class LinkedinUserCertificateCompany(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserCertificateCompany", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    urn: Optional[LinkedinURNLiteralFsdCompanyCompany] = None
    url: Optional[str] = Field(None, title="Url")


class LinkedinUserExperienceEmployment(Enum):
    full_time = "full-time"
    part_time = "part-time"
    permanent = "permanent"
    self_employment = "self-employment"
    freelance = "freelance"
    contract = "contract"
    internship = "internship"
    apprenticeship = "apprenticeship"
    indirect_contract = "indirect contract"


class LinkedinUserExperienceWorkType(Enum):
    on_site = "on-site"
    hybrid = "hybrid"
    remote = "remote"


class LinkedinUserHonor(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserHonor", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    issued_by: Optional[str] = Field(None, title="Issued By")
    issued_at: Optional[str] = Field(None, title="Issued At")
    text: Optional[str] = Field(None, title="Text")


class LinkedinUserLanguage(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserLanguage", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    level: Optional[str] = Field(None, title="Level")


class LinkedinUserPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    user: Union[str, LinkedinURNLiteralFsdProfile] = Field(
        ...,
        description="User Alias or URL or fsd_profile URN",
        examples=["google"],
        title="User",
    )


class LinkedinUserPostEvent(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserPostEvent", alias="@type", title="Entity Type")
    url: str = Field(..., title="Url")
    image: Optional[str] = Field(None, title="Image")
    title: Optional[str] = Field(None, title="Title")
    date: Optional[str] = Field(None, title="Date")
    participant_count: Optional[int] = Field(None, title="Participant Count")


class LinkedinUserWebsite(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserWebsite", alias="@type", title="Entity Type")
    url: str = Field(..., title="Url")
    category: str = Field(..., title="Category")
    label: Optional[str] = Field(None, title="Label")


class User(BaseModel):
    id: UUID = Field(..., title="Id")
    front_id: str = Field(..., title="Front Id")
    login: str = Field(..., title="Login")
    role: UserRole
    email: str = Field(..., title="Email")
    name: str = Field(..., title="Name")
    created_at: datetime = Field(..., title="Created At")
    modified_at: datetime = Field(..., title="Modified At")
    last_login_at: Optional[datetime] = Field(..., title="Last Login At")


class LinkedinCompanyPostsPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    urn: LinkedinURNLiteralCompany = Field(
        ...,
        description="Company URN, only company urn type is allowed",
        examples=["company:11130470"],
    )
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinPostPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    urn: LinkedinURNLiteralActivity = Field(
        ...,
        description="Post URN, only activity urn type is allowed",
        examples=["urn:li:activity:7234173400267538433"],
    )


class LinkedinReaction(BaseModel):
    field_type: Optional[str] = Field("LinkedinReaction", alias="@type", title="Entity Type")
    type: LinkedinReactionType
    count: int = Field(..., title="Count")


class LinkedinURN(BaseModel):
    type: LinkedinURNPrefix
    value: str = Field(..., title="Value")


class LinkedinUserCertificate(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserCertificate", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    company: Optional[LinkedinUserCertificateCompany] = None
    created_at: Optional[str] = Field(None, title="Created At")
    label: Optional[str] = Field(None, title="Label")
    url: Optional[str] = Field(None, title="Url")


class LinkedinUserEducationCompany(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserEducationCompany", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    urn: Optional[LinkedinURN] = None
    url: Optional[str] = Field(None, title="Url")


class LinkedinUserEndorser(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserEndorser", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    photo: Optional[str] = Field(None, title="Photo")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    headline: Optional[str] = Field(None, title="Headline")


class LinkedinUserExperienceCompany(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserExperienceCompany", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    urn: Optional[LinkedinURN] = None
    url: Optional[str] = Field(None, title="Url")


class LinkedinUserPatentInventorUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserPatentInventorUser", alias="@type", title="Entity Type")
    urn: LinkedinURN


class LinkedinUserPostUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserPostUser", alias="@type", title="Entity Type")
    internal_id: LinkedinURN
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    headline: Optional[str] = Field(None, title="Headline")
    image: Optional[str] = Field(None, title="Image")


class LinkedinUserURNPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    urn: LinkedinURN = Field(
        ...,
        description="User URN, only fsd_profile urn type is allowed",
        examples=["urn:li:fsd_profile:ACoAACmguogBIdbijM6YpcIganWLJ67yKyV5kd4"],
    )
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinUserSkill(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserSkill", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    urn: Optional[LinkedinURN] = None


class LinkedinCompany(BaseModel):
    field_type: Optional[str] = Field("LinkedinCompany", alias="@type", title="Entity Type")
    urn: LinkedinURN
    url: str = Field(..., title="Url")
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    website: Optional[str] = Field(None, title="Website")
    locations: Optional[List[LinkedinOfficeLocation]] = Field(None, title="Locations")
    short_description: Optional[str] = Field(None, title="Short Description")
    description: Optional[str] = Field(None, title="Description")
    employee_count: Optional[int] = Field(None, title="Employee Count")
    founded_on: Optional[int] = Field(None, title="Founded On")
    phone: Optional[str] = Field(None, title="Phone")
    logo_url: Optional[str] = Field(None, title="Logo Url")
    organizational_urn: Optional[LinkedinURN] = None
    page_verification_status: Optional[bool] = Field(None, title="Page Verification Status")
    last_modified_at: Optional[int] = Field(None, title="Last Modified At")
    headquarter_status: Optional[bool] = Field(None, title="Headquarter Status")
    headquarter_location: Optional[str] = Field(None, title="Headquarter Location")
    industry: Optional[LinkedinURN] = None
    specialities: Optional[List[str]] = Field(None, title="Specialities")
    is_active: Optional[bool] = Field(None, title="Is Active")
    employee_count_range: Optional[str] = Field(None, title="Employee Count Range")
    similar_organizations: Optional[List[LinkedinURN]] = Field(None, title="Similar Organizations")
    hashtags: Optional[List[str]] = Field(None, title="Hashtags")
    crunchbase_link: Optional[str] = Field(None, title="Crunchbase Link")


class LinkedinCompanyPostCompany(BaseModel):
    field_type: Optional[str] = Field("LinkedinCompanyPostCompany", alias="@type", title="Entity Type")
    internal_id: LinkedinURN
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    headline: Optional[str] = Field(None, title="Headline")
    image: Optional[str] = Field(None, title="Image")


class LinkedinGroupUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinGroupUser", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    headline: Optional[str] = Field(None, title="Headline")


class LinkedinPostCommentUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinPostCommentUser", alias="@type", title="Entity Type")
    internal_id: LinkedinURN
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    headline: Optional[str] = Field(None, title="Headline")


class LinkedinPostCommentsPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    urn: LinkedinURN = Field(
        ...,
        description="Post URN, only activity urn type is allowed",
        examples=["urn:li:activity:7235504557777174528"],
    )
    sort: Optional[LinkedinPostCommentsSort] = Field("relevance", description="Sort type")
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinPostReactionUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinPostReactionUser", alias="@type", title="Entity Type")
    internal_id: LinkedinURN
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    url: str = Field(..., title="Url")
    headline: Optional[str] = Field(None, title="Headline")


class LinkedinPostReactionsPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    urn: LinkedinURN = Field(
        ...,
        description="Post URN, only activity urn type is allowed",
        examples=["google"],
    )
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinSearchCompaniesPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    keywords: Optional[str] = Field(
        "",
        description="Any keyword for searching in the company page",
        examples=["microsoft"],
        title="Keywords",
    )
    location: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Location URN, can be obtained in /linkedin/search/locations, only geo urn type is allowed",
        examples=['["urn:li:geo:103689695"]'],
        title="Location",
    )
    industry: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Industry URN, can be obtained in /linkedin/search/industries, only industry urn type is allowed",
        examples=['["urn:li:industry:96"]'],
        title="Industry",
    )
    employee_count: Optional[List[EmployeeCount]] = Field(
        None,
        description="Employee count",
        examples=['{"urn:li:industry:96"}'],
        title="Employee Count",
    )
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinSearchCompany(BaseModel):
    field_type: Optional[str] = Field("LinkedinSearchCompany", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    url: str = Field(..., title="Url")
    alias: str = Field(..., title="Alias")
    image: Optional[str] = Field(None, title="Image")
    industry: Optional[str] = Field(None, title="Industry")


class LinkedinSearchEducation(BaseModel):
    field_type: Optional[str] = Field("LinkedinSearchEducation", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    headline: Optional[str] = Field(None, title="Headline")
    image: Optional[str] = Field(None, title="Image")


class LinkedinSearchIndustry(BaseModel):
    field_type: Optional[str] = Field("LinkedinSearchIndustry", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")


class LinkedinSearchLocation(BaseModel):
    field_type: Optional[str] = Field("LinkedinSearchLocation", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")


class LinkedinSearchUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinSearchUser", alias="@type", title="Entity Type")
    internal_id: LinkedinURN
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    image: Optional[str] = Field(None, title="Image")
    headline: Optional[str] = Field(None, title="Headline")
    location: Optional[str] = Field(None, title="Location")


class LinkedinSearchUsersPayload(BaseModel):
    timeout: Optional[int] = Field(300.0, title="Timeout")
    keywords: Optional[str] = Field(
        "",
        description="Any keyword for searching in the user page.With the params result count will be small.Use other params to obtain a lot of results",
        examples=["Director"],
        title="Keywords",
    )
    first_name: Optional[str] = Field(
        "",
        description="Search for exact first name",
        examples=["Bill"],
        title="First Name",
    )
    last_name: Optional[str] = Field(
        "",
        description="Search for exact last name",
        examples=["Gates"],
        title="Last Name",
    )
    title: Optional[str] = Field(
        "",
        description="Search for exact word in the title",
        examples=["Director"],
        title="Title",
    )
    company_keywords: Optional[str] = Field(
        "",
        description="Search for exact word in the company name",
        examples=["Microsoft"],
        title="Company Keywords",
    )
    school_keywords: Optional[str] = Field(
        "",
        description="Search for exact word in the school name",
        examples=["Harvard"],
        title="School Keywords",
    )
    current_company: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Current company URN, only company urn type is allowed",
        examples=['["urn:li:company:1441"]'],
        title="Current Company",
    )
    past_company: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Past company URN, only company urn type is allowed",
        examples=['["urn:li:company:1441"]'],
        title="Past Company",
    )
    location: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Location URN, can be obtained in /linkedin/search/locations, only geo urn type is allowed",
        examples=['["urn:li:geo:103689695"]'],
        title="Location",
    )
    industry: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Industry URN, can be obtained in /linkedin/search/industries, only industry urn type is allowed",
        examples=['["urn:li:industry:96"]'],
        title="Industry",
    )
    education: Optional[Union[List[LinkedinURN], str]] = Field(
        None,
        description="Industry URN, can be obtained in /linkedin/search/educations, only fsd_company urn type is allowed",
        examples=['["urn:li:fsd_company:96"]'],
        title="Education",
    )
    count: PositiveInt = Field(..., description="Max result count", title="Count")


class LinkedinUserEducation(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserEducation", alias="@type", title="Entity Type")
    company: LinkedinUserEducationCompany
    major: Optional[str] = Field(None, title="Major")
    interval: Optional[str] = Field(None, title="Interval")


class LinkedinUserExperience(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserExperience", alias="@type", title="Entity Type")
    company: LinkedinUserExperienceCompany
    position: Optional[str] = Field(None, title="Position")
    work_type: Optional[LinkedinUserExperienceWorkType] = None
    employment: Optional[LinkedinUserExperienceEmployment] = None
    interval: Optional[str] = Field(None, title="Interval")
    period: Optional[str] = Field(None, title="Period")
    location: Optional[str] = Field(None, title="Location")
    description: Optional[str] = Field(None, title="Description")


class LinkedinUserPatent(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserPatent", alias="@type", title="Entity Type")
    name: str = Field(..., title="Name")
    id: Optional[str] = Field(None, title="Id")
    issued_at: Optional[str] = Field(None, title="Issued At")
    text: Optional[str] = Field(None, title="Text")
    url: Optional[str] = Field(None, title="Url")
    inventors: Optional[List[LinkedinUserPatentInventorUser]] = Field(None, title="Inventors")
    inventor_count: Optional[int] = Field(None, title="Inventor Count")


class LinkedinUserPost(BaseModel):
    field_type: Optional[str] = Field("LinkedinUserPost", alias="@type", title="Entity Type")
    urn: LinkedinURN
    url: str = Field(..., title="Url")
    author: Optional[Union[LinkedinUserPostUser, LinkedinCompanyPostCompany]] = Field(None, title="Author")
    created_at: Optional[int] = Field(None, title="Created At")
    share_urn: Optional[LinkedinURN] = None
    is_empty_repost: Optional[bool] = Field(None, title="Is Empty Repost")
    repost: Optional[LinkedinUserPost] = None
    images: Optional[List[str]] = Field(None, title="Images")
    text: Optional[str] = Field(None, title="Text")
    comment_count: Optional[int] = Field(None, title="Comment Count")
    share_count: Optional[int] = Field(None, title="Share Count")
    reactions: Optional[List[LinkedinReaction]] = Field(None, title="Reactions")
    event: Optional[LinkedinUserPostEvent] = None


class LinkedinGroupMember(BaseModel):
    field_type: Optional[str] = Field("LinkedinGroupMember", alias="@type", title="Entity Type")
    user: LinkedinGroupUser
    role: Union[LinkedinGroupMemberRole, str] = Field(..., title="Role")
    joined_at: Optional[int] = Field(None, title="Joined At")


class LinkedinPostComment(BaseModel):
    field_type: Optional[str] = Field("LinkedinPostComment", alias="@type", title="Entity Type")
    urn: LinkedinURN
    url: str = Field(..., title="Url")
    text: str = Field(..., title="Text")
    author: LinkedinPostCommentUser
    created_at: int = Field(..., title="Created At")
    is_commenter_post_author: bool = Field(..., title="Is Commenter Post Author")
    comment_count: Optional[int] = Field(None, title="Comment Count")
    reactions: Optional[List[LinkedinReaction]] = Field(None, title="Reactions")
    parent: Optional[LinkedinURN] = None


class LinkedinPostReaction(BaseModel):
    field_type: Optional[str] = Field("LinkedinPostReaction", alias="@type", title="Entity Type")
    type: LinkedinReactionType
    user: LinkedinPostReactionUser


class LinkedinUser(BaseModel):
    field_type: Optional[str] = Field("LinkedinUser", alias="@type", title="Entity Type")
    internal_id: LinkedinURN
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    alias: str = Field(..., title="Alias")
    url: str = Field(..., title="Url")
    email: Optional[str] = Field(None, title="Email")
    birth_date: Optional[LinkedinUserBirthDate] = None
    websites: Optional[List[LinkedinUserWebsite]] = Field(None, title="Websites")
    headline: Optional[str] = Field(None, title="Headline")
    follower_count: Optional[int] = Field(None, title="Follower Count")
    image: Optional[str] = Field(None, title="Image")
    connection_count: Optional[int] = Field(None, title="Connection Count")
    description: Optional[str] = Field(None, title="Description")
    top_skills: Optional[List[str]] = Field(None, title="Top Skills")
    frame: Optional[LinkedinProfileStatus] = None
    location: Optional[str] = Field(None, title="Location")
    pronouns: Optional[str] = Field(None, title="Pronouns")
    custom_pronouns: Optional[str] = Field(None, title="Custom Pronouns")
    experience: Optional[List[LinkedinUserExperience]] = Field(None, title="Experience")
    education: Optional[List[LinkedinUserEducation]] = Field(None, title="Education")
    languages: Optional[List[LinkedinUserLanguage]] = Field(None, title="Languages")
    certificates: Optional[List[LinkedinUserCertificate]] = Field(None, title="Certificates")
    honors: Optional[List[LinkedinUserHonor]] = Field(None, title="Honors")
    patents: Optional[List[LinkedinUserPatent]] = Field(None, title="Patents")
    verified: Optional[bool] = Field(False, title="Verified")


class LinkedinGroup(BaseModel):
    field_type: Optional[str] = Field("LinkedinGroup", alias="@type", title="Entity Type")
    urn: LinkedinURN
    name: str = Field(..., title="Name")
    url: str = Field(..., title="Url")
    image: Optional[str] = Field(None, title="Image")
    created_at: Optional[int] = Field(None, title="Created At")
    member_count: int = Field(..., title="Member Count")
    description: Optional[str] = Field(None, title="Description")
    rules: Optional[str] = Field(None, title="Rules")
    geo: Optional[LinkedinURN] = None
    industries: Optional[List[LinkedinURN]] = Field(None, title="Industries")
    members: Optional[List[LinkedinGroupMember]] = Field(None, title="Members")


LinkedinUserPost.model_rebuild()
