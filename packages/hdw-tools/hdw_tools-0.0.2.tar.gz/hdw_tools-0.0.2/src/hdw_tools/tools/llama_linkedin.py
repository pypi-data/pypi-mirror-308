from llama_index.core.tools.tool_spec.base import BaseToolSpec
from hdw_tools.core.base import APIClient
from hdw_tools.core.models import *


class LinkedInToolSpec(BaseToolSpec):
    spec_functions = [
        "linkedin_company",
        "linkedin_company_posts",
        "linkedin_group",
        "linkedin_post",
        "linkedin_post_comments",
        "linkedin_post_reactions",
        "linkedin_search_companies",
        "linkedin_search_educations",
        "linkedin_search_industries",
        "linkedin_search_locations",
        "linkedin_search_users",
        "linkedin_user",
        "linkedin_user_certificates",
        "linkedin_user_education",
        "linkedin_user_endorsers",
        "linkedin_user_experience",
        "linkedin_user_honors",
        "linkedin_user_languages",
        "linkedin_user_patents",
        "linkedin_user_posts",
        "linkedin_user_reactions",
        "linkedin_user_skills",
    ]

    def __init__(self) -> None:
        self.client = APIClient()

    def linkedin_company(
        self, request_payload: LinkedinCompanyPayload
    ) -> LinkedinCompany | list[LinkedinCompany] | dict:
        return self.client.get_data(
            endpoint="linkedin/company", request_payload=request_payload, response_model=LinkedinCompany
        )

    def linkedin_company_posts(
        self, request_payload: LinkedinCompanyPostsPayload
    ) -> LinkedinUserPost | list[LinkedinUserPost] | dict:
        return self.client.get_data(
            endpoint="linkedin/company/posts", request_payload=request_payload, response_model=LinkedinUserPost
        )

    def linkedin_group(self, request_payload: LinkedinGroupPayload) -> LinkedinGroup | list[LinkedinGroup] | dict:
        return self.client.get_data(
            endpoint="linkedin/group", request_payload=request_payload, response_model=LinkedinGroup
        )

    def linkedin_post(self, request_payload: LinkedinPostPayload) -> LinkedinUserPost | list[LinkedinUserPost] | dict:
        return self.client.get_data(
            endpoint="linkedin/post", request_payload=request_payload, response_model=LinkedinUserPost
        )

    def linkedin_post_comments(
        self, request_payload: LinkedinPostCommentsPayload
    ) -> LinkedinPostComment | list[LinkedinPostComment] | dict:
        return self.client.get_data(
            endpoint="linkedin/post/comments", request_payload=request_payload, response_model=LinkedinPostComment
        )

    def linkedin_post_reactions(
        self, request_payload: LinkedinPostReactionsPayload
    ) -> LinkedinPostReaction | list[LinkedinPostReaction] | dict:
        return self.client.get_data(
            endpoint="linkedin/post/reactions", request_payload=request_payload, response_model=LinkedinPostReaction
        )

    def linkedin_search_companies(
        self, request_payload: LinkedinSearchCompaniesPayload
    ) -> LinkedinSearchCompany | list[LinkedinSearchCompany] | dict:
        return self.client.get_data(
            endpoint="linkedin/search/companies", request_payload=request_payload, response_model=LinkedinSearchCompany
        )

    def linkedin_search_educations(
        self, request_payload: LinkedinSearchEducationsPayload
    ) -> LinkedinSearchEducation | list[LinkedinSearchEducation] | dict:
        return self.client.get_data(
            endpoint="linkedin/search/educations",
            request_payload=request_payload,
            response_model=LinkedinSearchEducation,
        )

    def linkedin_search_industries(
        self, request_payload: LinkedinSearchIndustriesPayload
    ) -> LinkedinSearchIndustry | list[LinkedinSearchIndustry] | dict:
        return self.client.get_data(
            endpoint="linkedin/search/industries",
            request_payload=request_payload,
            response_model=LinkedinSearchIndustry,
        )

    def linkedin_search_locations(
        self, request_payload: LinkedinSearchLocationsPayload
    ) -> LinkedinSearchLocation | list[LinkedinSearchLocation] | dict:
        return self.client.get_data(
            endpoint="linkedin/search/locations", request_payload=request_payload, response_model=LinkedinSearchLocation
        )

    def linkedin_search_users(
        self, request_payload: LinkedinSearchUsersPayload
    ) -> LinkedinSearchUser | list[LinkedinSearchUser] | dict:
        return self.client.get_data(
            endpoint="linkedin/search/users", request_payload=request_payload, response_model=LinkedinSearchUser
        )

    def linkedin_user(self, request_payload: LinkedinUserPayload) -> LinkedinUser | list[LinkedinUser] | dict:
        return self.client.get_data(
            endpoint="linkedin/user", request_payload=request_payload, response_model=LinkedinUser
        )

    def linkedin_user_certificates(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserCertificate | list[LinkedinUserCertificate] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/certificates",
            request_payload=request_payload,
            response_model=LinkedinUserCertificate,
        )

    def linkedin_user_education(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserEducation | list[LinkedinUserEducation] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/education", request_payload=request_payload, response_model=LinkedinUserEducation
        )

    def linkedin_user_endorsers(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserEndorser | list[LinkedinUserEndorser] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/endorsers", request_payload=request_payload, response_model=LinkedinUserEndorser
        )

    def linkedin_user_experience(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserExperience | list[LinkedinUserExperience] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/experience", request_payload=request_payload, response_model=LinkedinUserExperience
        )

    def linkedin_user_honors(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserHonor | list[LinkedinUserHonor] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/honors", request_payload=request_payload, response_model=LinkedinUserHonor
        )

    def linkedin_user_languages(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserLanguage | list[LinkedinUserLanguage] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/languages", request_payload=request_payload, response_model=LinkedinUserLanguage
        )

    def linkedin_user_patents(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserPatent | list[LinkedinUserPatent] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/patents", request_payload=request_payload, response_model=LinkedinUserPatent
        )

    def linkedin_user_posts(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserPost | list[LinkedinUserPost] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/posts", request_payload=request_payload, response_model=LinkedinUserPost
        )

    def linkedin_user_reactions(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserPost | list[LinkedinUserPost] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/reactions", request_payload=request_payload, response_model=LinkedinUserPost
        )

    def linkedin_user_skills(
        self, request_payload: LinkedinUserURNPayload
    ) -> LinkedinUserSkill | list[LinkedinUserSkill] | dict:
        return self.client.get_data(
            endpoint="linkedin/user/skills", request_payload=request_payload, response_model=LinkedinUserSkill
        )
