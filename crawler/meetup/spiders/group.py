import scrapy
from meetup.items import GroupItem
import json


class GroupSpider(scrapy.Spider):
    name = "meetup"
    allowed_domains = ["api.meetup.com"]

    MEETUP_API_KEY = ""

    start_urls = [
        "https://api.meetup.com/2/groups?sign=true&key=" + MEETUP_API_KEY + "&only=category.name,id,name&group_id=11521392"
    ]
    # AngularJS-BH is the seed group
    base_profile_url = "https://api.meetup.com/2/profiles?sign=true&key=" + MEETUP_API_KEY + "&only=group.id&member_id="
    base_group_members_url = "https://api.meetup.com/2/profiles?sign=true&key=" + MEETUP_API_KEY + "&only=member_id&group_id="
    base_group_info_url = "https://api.meetup.com/2/groups?sign=true&key=" + MEETUP_API_KEY + "&category.name,id,name&group_id="

    DEBUG_MODE = True

    def parse(self, response):
        """
        Seed crawl, only called when spiders starts. Yields a request for
        detailed info about the seed group
        """
        self.print_api_usage_rates(response)

        # Yields a request for detailed info for the seed group
        group_request = scrapy.Request(response.url, callback=self.parse_group_info_url)

        return group_request

    def parse_group_info_url(self, response):
        """
        Gets info about a group, yielding a request for its members
        """
        self.print_api_usage_rates(response)

        response_data = json.loads(response.body_as_unicode())

        group_id = response_data["results"][0]["id"]
        group_members_request = scrapy.Request(self.base_group_members_url + str(group_id), callback=self.parse_group_members_url)

        # Starts the group item
        group_item = GroupItem()
        group_item["groupId"] = response_data["results"][0]["id"]
        group_item["groupName"] = response_data["results"][0]["name"]
        group_item["categoryName"] = response_data["results"][0]["category"]["name"]
        group_item["membersId"] = []

        # Save the item to be populated with members ids
        group_members_request.meta["groupItem"] = group_item

        return group_members_request

    def parse_group_members_url(self, response):
        """
        Gets all group members
        """
        self.print_api_usage_rates(response)

        response_data = json.loads(response.body_as_unicode())

        item = response.meta["groupItem"]

        # Yielding requests to get groups for every member in this group
        for member in response_data["results"]:
            member_id = member["member_id"]
            item["membersId"].append(member_id)
            profile_request = scrapy.Request(self.base_profile_url + str(member_id), callback=self.parse_user_profile_url)
            profile_request.meta["memberId"] = member_id
            yield profile_request

        # Follows next link to continue reading the members
        if "next" in response_data["meta"] and len(response_data["meta"]["next"]) > 0:
            # Follows the next link to get all pages of data
            group_request = scrapy.Request(response_data["meta"]["next"], callback=self.parse_group_members_url)
            group_request.meta["groupItem"] = item
            yield group_request
        else:
            # If there is no next link, saves the item
            yield item

    def parse_user_profile_url(self, response):
        """
        Yields requests to crawl all groups for a user
        """
        self.print_api_usage_rates(response)

        response_data = json.loads(response.body_as_unicode())

        # Yields a requests for every group this user belongs to
        for result in response_data["results"]:
            group_id = result["group"]["id"]
            group_request = scrapy.Request(self.base_group_info_url + str(group_id), callback=self.parse_group_info_url)
            yield group_request

        if "next" and response_data["meta"] and len(response_data["meta"]["next"]) > 0:
            # Follows the next link to get all pages of data
            profile_request = scrapy.Request(response_data["meta"]["next"], callback=self.parse_user_profile_url)
            profile_request.meta["memberId"] = response.meta["memberId"]
            yield profile_request

    def print_api_usage_rates(self, response):
        if self.DEBUG_MODE:
            print "X-RateLimit-Limit: " + response.headers["X-RateLimit-Limit"] + " requests can be made in a window of time"
            print "X-RateLimit-Reset: " + response.headers["X-RateLimit-Reset"] + " seconds until the current rate limit window resets"
            print "X-RateLimit-Remaining: " + response.headers["X-RateLimit-Remaining"] + " requests remaining in the current rate limit window"
