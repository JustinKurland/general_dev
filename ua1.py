import json
import user_agents
import aiohttp
import asyncio
import logging
from aiocache import cached, SimpleMemoryCache
from datetime import datetime
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserAgentAnalysis:
    """Analyzes user agents and enriches data with VirusTotal API.

    This class connects to a BigQuery database and performs user agent 
    parsing and enrichment using VirusTotal.

    Args:
        config_path (str): Path to the JSON configuration file.
    """
    
    def __init__(self, config_path="config.json"):
        self.client = bigquery.Client()
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.virustotal_api_key = config["virustotal"]["api_key"]

    def parse_user_agent(self, user_agent_string):
        """Parses a user agent string to extract browser, OS, and device 
           details.

        This function attempts to parse the provided user agent string 
        for information such as the browser, operating system, and 
        device family. It additionally determines the approximate age of 
        the user agent based on its major version. If the user agent is 
        unrecognized and returns generic values (e.g., 'Other' for 
        browser, OS, and device), it is marked as invalid.

        Args:
            user_agent_string (str): The user agent string to parse.

        Returns:
            dict: Parsed user agent details, including:
                - 'browser' (str): Browser family (e.g., "Chrome").
                - 'browser_version' (str): Browser version 
                (e.g., "58.0.3029").
                - 'os' (str): Operating system family (e.g., "Windows").
                - 'os_version' (str): OS version.
                - 'device' (str): Device family (e.g., "PC").
                - 'status' (str): 'valid' if parsed successfully, 
                'invalid' if the user agent is generic/unrecognized, and 
                'empty' if no user agent string is provided.
                - 'user_agent_age' (int or str): Approximate age of the 
                user agent in years, or 'current' if undetermined.
        """
        if not user_agent_string:
            return {'status': 'empty'}

        try:
            user_agent = user_agents.parse(user_agent_string)
            details = {
                'browser': user_agent.browser.family,
                'browser_version': ".".join(
                    map(str, user_agent.browser.version)
                ),
                'os': user_agent.os.family,
                'os_version': user_agent.os.version_string,
                'device': user_agent.device.family,
                'status': 'valid'
            }
            current_year = datetime.now().year
            major_version = (
                int(user_agent.browser.version[0])
                if user_agent.browser.version else 0
            )
            age = current_year - major_version
            details['user_agent_age'] = age if age > 0 else 'current'

            if (
                details['browser'] == 'Other'
                and details['os'] == 'Other'
                and details['device'] == 'Other'
            ):
                details['status'] = 'invalid'
            
            return details
        except Exception as e:
            print(f"Error parsing user agent: {e}")
            return {'status': 'invalid'}

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def enrich_with_virus_total(self, session, user_agent, retries=3, 
                                      backoff_factor=1):
        """Fetches enrichment data from VirusTotal for a given user 
           agent asynchronously.

        Args:
            session (aiohttp.ClientSession): aiohttp session for making 
            HTTP requests.
            user_agent (str): The user agent string to search on
            VirusTotal.
            retries (int, optional): Number of retry attempts on failure 
            (default is 3).
            backoff_factor (int, optional): Backoff multiplier between 
            retries (default is 1).

        Returns:
            dict: VirusTotal data for the user agent, or an empty dict 
            if request fails.
        """
        url = f"https://www.virustotal.com/api/v3/search?query={user_agent}"
        headers = {"x-apikey": self.virustotal_api_key}
        
        for attempt in range(retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        logger.info(
                            f"Successfully fetched VirusTotal data for user " 
                            f"agent: {user_agent}"
                            )
                        return await response.json()
                    elif response.status in [429, 500, 502, 503, 504]:
                        logger.warning(
                            f"Attempt {attempt+1}: Error {response.status}, "
                            f"retrying after backoff for user agent: "
                            f"{user_agent}"
                            )
                        await asyncio.sleep(backoff_factor * (2 ** attempt))
                    else:
                        logger.error(
                            f"Error {response.status}: Failed to fetch "
                            f"VirusTotal data for user agent: {user_agent}"
                            )
                        return {}
            except aiohttp.ClientError as e:
                logger.error(
                    f"Network error while fetching VirusTotal data for user "
                    f"agent: {user_agent}: {e}"
                    )
                await asyncio.sleep(backoff_factor * (2 ** attempt))

        logger.error(
            f"Failed to fetch VirusTotal data for user agent: {user_agent} "
            f"after {retries} attempts."
            )
        return {}

    async def process_user_agents(self, ua_list):
        """Asynchronously processes a list of user agents and enriches 
           them with VirusTotal data.

        Args:
            ua_list (list): List of user agent strings.

        Returns:
            list[dict]: List of dictionaries containing parsed user 
            agent details and enrichment data from VirusTotal.
        """
        tasks = []
        async with aiohttp.ClientSession() as session:
            for ua in ua_list:
                parsed_ua = self.parse_user_agent(ua)
                tasks.append(self.enrich_with_virus_total(session, ua))
            
            virus_total_data = await asyncio.gather(*tasks)
        
        # Define parsed_user_agents separately to align with the zip operation in the return
        parsed_user_agents = [self.parse_user_agent(ua) for ua in ua_list]
        
        return [
            {**parsed_ua, 'virustotal': vt_data}
            for parsed_ua, vt_data in zip(parsed_user_agents, virus_total_data)
        ]
        
    def run_processing(self, ua_list):
        """Runs asynchronous processing of user agents in an event 
           loop.
        """
        return asyncio.run(self.process_user_agents(ua_list))
