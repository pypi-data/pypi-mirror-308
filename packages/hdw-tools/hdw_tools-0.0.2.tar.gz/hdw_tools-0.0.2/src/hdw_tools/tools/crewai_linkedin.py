from crewai_tools import BaseTool  # type: ignore
from hdw_tools.core.base import APIClient
from hdw_tools.core.models import *
from typing import Type
from pydantic import BaseModel


class GetLinkedInCompany(BaseTool):
    name: str = "Get LinkedIn company"
    description: str = "Get LinkedIn company"
    args_schema: Type[BaseModel] = LinkedinCompanyPayload

    def _run(self, **kwargs: dict) -> LinkedinCompany | list[LinkedinCompany] | dict:
        client = APIClient()
        return client.get_data(endpoint="linkedin/company", request_payload=kwargs, response_model=LinkedinCompany)


class GetLinkedInCompanyPosts(BaseTool):
    name: str = "Get LinkedIn company posts"
    description: str = "Get LinkedIn company posts"
    args_schema: Type[BaseModel] = LinkedinCompanyPostsPayload

    def _run(self, **kwargs: dict) -> LinkedinUserPost | list[LinkedinUserPost] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/company/posts", request_payload=kwargs, response_model=LinkedinUserPost
        )


class GetLinkedInGroup(BaseTool):
    name: str = "Get LinkedIn group"
    description: str = "Get LinkedIn group"
    args_schema: Type[BaseModel] = LinkedinGroupPayload

    def _run(self, **kwargs: dict) -> LinkedinGroup | list[LinkedinGroup] | dict:
        client = APIClient()
        return client.get_data(endpoint="linkedin/group", request_payload=kwargs, response_model=LinkedinGroup)


class GetLinkedInPost(BaseTool, APIClient):
    name: str = "Get LinkedIn post"
    description: str = "Get LinkedIn post"
    args_schema: Type[BaseModel] = LinkedinPostPayload

    def _run(self, **kwargs: dict) -> LinkedinUserPost | list[LinkedinUserPost] | dict:
        client = APIClient()
        return client.get_data(endpoint="linkedin/post", request_payload=kwargs, response_model=LinkedinUserPost)


class GetLinkedInPostComments(BaseTool, APIClient):
    name: str = "Get LinkedIn post comments"
    description: str = "Get LinkedIn post comments"
    args_schema: Type[BaseModel] = LinkedinPostCommentsPayload

    def _run(self, **kwargs: dict) -> LinkedinPostComment | list[LinkedinPostComment] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/post/comments", request_payload=kwargs, response_model=LinkedinPostComment
        )


class GetLinkedInPostReactions(BaseTool, APIClient):
    name: str = "Get LinkedIn post reactions"
    description: str = "Get LinkedIn post reactions"
    args_schema: Type[BaseModel] = LinkedinPostReactionsPayload

    def _run(self, **kwargs: dict) -> LinkedinPostReaction | list[LinkedinPostReaction] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/post/reactions", request_payload=kwargs, response_model=LinkedinPostReaction
        )


class SearchLinkedInCompanies(BaseTool, APIClient):
    name: str = "Search LinkedIn companies"
    description: str = "Search LinkedIn companies"
    args_schema: Type[BaseModel] = LinkedinSearchCompaniesPayload

    def _run(self, **kwargs: dict) -> LinkedinSearchCompany | list[LinkedinSearchCompany] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/search/companies", request_payload=kwargs, response_model=LinkedinSearchCompany
        )


class SearchLinkedInEducations(BaseTool, APIClient):
    name: str = "Search LinkedIn educations"
    description: str = "Search LinkedIn educations"
    args_schema: Type[BaseModel] = LinkedinSearchEducationsPayload

    def _run(self, **kwargs: dict) -> LinkedinSearchEducation | list[LinkedinSearchEducation] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/search/educations",
            request_payload=kwargs,
            response_model=LinkedinSearchEducation,
        )


class SearchLinkedinIndustries(BaseTool, APIClient):
    name: str = "Search LinkedIn industries"
    description: str = "Search LinkedIn industries"
    args_schema: Type[BaseModel] = LinkedinSearchIndustriesPayload

    def _run(self, **kwargs: dict) -> LinkedinSearchIndustry | list[LinkedinSearchIndustry] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/search/industries",
            request_payload=kwargs,
            response_model=LinkedinSearchIndustry,
        )


class SearchLinkedInLocations(BaseTool, APIClient):
    name: str = "Search LinkedIn locations"
    description: str = "Search LinkedIn locations"
    args_schema: Type[BaseModel] = LinkedinSearchLocationsPayload

    def _run(self, **kwargs: dict) -> LinkedinSearchLocation | list[LinkedinSearchLocation] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/search/locations", request_payload=kwargs, response_model=LinkedinSearchLocation
        )


class SearchLinkedInUsers(BaseTool, APIClient):
    name: str = "Search LinkedIn users"
    description: str = "Search LinkedIn users"
    args_schema: Type[BaseModel] = LinkedinSearchUsersPayload

    def _run(self, **kwargs: dict) -> LinkedinSearchUser | list[LinkedinSearchUser] | dict:
        client = APIClient()
        return client.get_data(
            endpoint="linkedin/search/users", request_payload=kwargs, response_model=LinkedinSearchUser
        )


class GetLinkedInUser(BaseTool):
    name: str = "Get LinkedIn user"
    description: str = "Get LinkedIn user"
    args_schema: Type[BaseModel] = LinkedinUserPayload

    def _run(self, **kwargs: dict) -> LinkedinUser | list[LinkedinUser] | dict:
        client = APIClient()
        return client.get_data(endpoint="linkedin/user", request_payload=kwargs, response_model=LinkedinUser)
