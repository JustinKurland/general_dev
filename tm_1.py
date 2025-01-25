import json
import requests
import logging
import aiohttp
import asyncio
import pandas as pd
from aiocache import cached, SimpleMemoryCache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from google.cloud import bigquery
from dask import delayed, compute

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatMetrixDataExtraction:
    """Handles the extraction and analysis of ThreatMetrix data.

    This class connects to a BigQuery database and enriches the data 
    using external APIs like VirusTotal and Censys.
    
    Args:
        api_key (str): API key for accessing ThreatMetrix data.
    """
    
    def __init__(self, config_path="config.json"):
        """Initializes the ThreatMetrixDataExtraction class by loading
        API keys from a configuration file.

        Args:
            config_path (str): Path to the JSON configuration file.
        """
        self.client = bigquery.Client()

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        self.api_key = config["threat_metrix"]["api_key"]
        self.virustotal_api_key = config["virustotal"]["api_key"]
        self.censys_api_id = config["censys"]["api_id"]
        self.censys_api_secret = config["censys"]["api_secret"]

    def fetch_threat_metrix_data(self, start_time, end_time):
        """Fetches raw ThreatMetrix data from a BigQuery table based on 
           a given time range.

        This method constructs a SQL query to retrieve data from a 
        specified BigQuery table within the given time period. The data 
        consists of event bodies stored as JSON strings.

        Args:
            start_time (str): The start date and time for the query in 
                              'YYYY-MM-DD' format.
            end_time (str): The end date and time for the query in 
                            'YYYY-MM-DD' format.

        Returns:
            pandas.DataFrame: A DataFrame containing the queried 
            ThreatMetrix event data,with each row representing an event 
            body in JSON format.
        """
        query = f"""
            SELECT body
            FROM `your_dataset.your_source_table`
            WHERE event_time BETWEEN '{start_time}' AND '{end_time}'
        """
        return self.client.query(query).to_dataframe()

    async def analyze_with_threat_metrix(self, event_body):
        """Asynchronously analyzes and enriches a single ThreatMetrix event 
        with data from external APIs.

        This method takes the JSON representation of a ThreatMetrix event, 
        extracts relevant information (e.g., IP address), and enriches it 
        using VirusTotal and Censys APIs concurrently. The enriched data is 
        added to the event and returned as a dictionary.

        Args:
            event_body (str): The raw ThreatMetrix event data in JSON string 
            format.

        Returns:
            dict: A dictionary containing the enriched event data with 
            additional fields from VirusTotal and Censys (e.g., IP 
            reputation, device reputation), along with the original event 
            attributes (e.g., location, device information, etc.).
        """
        data = json.loads(event_body)
        ip_address = data.get('ip_address')

        async with aiohttp.ClientSession() as session:
            
            vt_data, censys_data = await asyncio.gather(
                self.enrich_with_virus_total(session, ip_address),
                self.enrich_with_censys(session, ip_address)
            )

        enriched_event = {
            'event_id': data.get('event_id'),
            'ip_address': ip_address,
            'user_agent': data.get('user_agent'),
            'device_id': data.get('device_id'),
            'location': data.get('location'),
            'event_time': data.get('event_time'),
            'risk_score': data.get('risk_score'),
            'account_id': data.get('account_id'),
            'login_attempt': data.get('login_attempt'),
            'session_id': data.get('session_id'),
            'transaction_id': data.get('transaction_id'),
            'device_os': data.get('device_os'),
            'device_model': data.get('device_model'),
            'device_type': data.get('device_type'),
            'country': data.get('country'),
            'region': data.get('region'),
            'city': data.get('city'),
            'zip_code': data.get('zip_code'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'confidence_score': data.get('confidence_score'),
            'fraud_type': data.get('fraud_type'),
            'identity_score': data.get('identity_score'),
            'email_domain': data.get('email_domain'),
            'phone_number': data.get('phone_number'),
            'payment_method': data.get('payment_method'),
            'proxy': data.get('proxy'),
            'vpn': data.get('vpn'),
            'tor': data.get('tor'),
            'bot': data.get('bot'),
            'malware': data.get('malware'),
            'phishevent': data.get('phishevent'),
            'account_creation': data.get('account_creation'),
            'account_takeover': data.get('account_takeover'),
            'account_funding': data.get('account_funding'),
            'device_change': data.get('device_change'),
            'password_reset': data.get('password_reset'),
            'profile_change': data.get('profile_change'),
            'withdrawal': data.get('withdrawal'),
            'deposit': data.get('deposit'),
            'purchase': data.get('purchase'),
            'transfer': data.get('transfer'),
            'refund': data.get('refund'),
            'login_success': data.get('login_success'),
            'login_failure': data.get('login_failure'),
            'multi_factor_auth': data.get('multi_factor_auth'),
            'sms_verification': data.get('sms_verification'),
            'email_verification': data.get('email_verification'),
            'phone_verification': data.get('phone_verification'),
            'ip_reputation': data.get('ip_reputation'),
            'blacklist_status': data.get('blacklist_status'),
            'device_reputation': data.get('device_reputation'),
            'behavioral_biometrics': data.get('behavioral_biometrics'),
            'network_attributes': data.get('network_attributes'),
            'geolocation': data.get('geolocation'),
            'risk_rules_triggered': data.get('risk_rules_triggered'),
            'custom_attributes': data.get('custom_attributes'),
            'screen_resolution': data.get('screen_resolution'),
            'charging_status': data.get('charging_status'),
            'virustotal': vt_data,
            'censys': censys_data
        }
        return enriched_event

    # This will cache the results in memory with a time-to-live (TTL) of 
    # 3600 seconds (1 hour), which is good for testing and development.
    # Later, we can adjust this to use a more robust cache backend, 
    # such as Redis.
    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def enrich_with_virus_total(self, session, ip_address, 
                                      retries=3, backoff_factor=1):
        """Fetches enrichment data from VirusTotal for a given IP 
           address asynchronously.

        This method sends an asynchronous API request to VirusTotal to 
        retrieve reputation and security-related information associated 
        with the provided IP address. It includes error handling with 
        retries for better fault tolerance in cases of rate-limiting or 
        transient server errors. 

        The method employs an exponential backoff strategy when retrying 
        failed requests due to specific HTTP status codes (e.g., 429, 
        500, 502, 503, 504).

        Args:
            session (aiohttp.ClientSession): The aiohttp session used to 
                perform the HTTP requests asynchronously.
            ip_address (str): The IP address for which to retrieve 
                enrichment data.
            retries (int, optional): The number of retry attempts in 
                case of failure (default is 3).
            backoff_factor (int or float, optional): The multiplier for 
                the exponential backoff between retry attempts (default 
                is 1).

        Returns:
            dict: A dictionary containing VirusTotal data for the given 
            IP address, such as reputation and associated threats, or an 
            empty dictionary if the request fails after all retries.
        """

        url = (
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
        )
        headers = {"x-apikey": self.virustotal_api_key}
        
        for attempt in range(retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        logger.info(
                            f"Successfully fetched data from VirusTotal for " 
                            f"IP: {ip_address}"
                        )
                        return await response.json()
                    elif response.status in [429, 500, 502, 503, 504]:
                        logger.warning(
                            f"Attempt {attempt+1}: Error {response.status}, "
                            f"retrying after backoff for IP: {ip_address}"
                        )
                        await asyncio.sleep(backoff_factor * (2 ** attempt))
                    else:
                        logger.error(
                            f"Error {response.status}: Failed to fetch data "
                            f"from VirusTotal for IP: {ip_address}"
                        )
                        return {}
            except aiohttp.ClientError as e:
                logger.error(
                    f"Error fetching VirusTotal data for IP: {ip_address}: {e}"
                    )
                await asyncio.sleep(backoff_factor * (2 ** attempt))  

        logger.error(
            f"Failed to fetch data from VirusTotal for IP: "
            f"{ip_address} after {retries} attempts."
            )
        return {}
    
    # This will cache the results in memory with a time-to-live (TTL) of 
    # 3600 seconds (1 hour), which is good for testing and development.
    # Later, we can adjust this to use a more robust cache backend, 
    # such as Redis.
    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def enrich_with_censys(self, session, ip_address, retries=3, 
                                 backoff_factor=1):
        """Fetches enrichment data from Censys for a given IP address 
            asynchronously.

        This method sends an asynchronous API request to Censys to 
        retrieve information related to the provided IP address. It 
        includes error handling with retries for better fault tolerance 
        in cases of rate-limiting or transient server errors.

        The method employs an exponential backoff strategy when retrying 
        failed requests due to specific HTTP status codes (e.g., 429, 
        500, 502, 503, 504).

        Args:
            session (aiohttp.ClientSession): The aiohttp session used to 
                perform the HTTP requests asynchronously.
            ip_address (str): The IP address for which to retrieve 
                enrichment data.
            retries (int, optional): The number of retry attempts in 
                case of failure (default is 3).
            backoff_factor (int or float, optional): The multiplier for 
                the exponential backoff between retry attempts (default 
                is 1).

        Returns:
            dict: A dictionary containing Censys data for the given IP 
                address, or an empty dictionary if the request fails 
                after all retries.
        """

        url = f"https://search.censys.io/api/v2/hosts/{ip_address}"
        headers = {
            "Authorization": f"Bearer {self.censys_api_key}"
        }

        for attempt in range(retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        logger.info(
                            f"Successfully fetched data from Censys for "
                            f"IP: {ip_address}"
                        )
                        return await response.json()
                    elif response.status in [429, 500, 502, 503, 504]:
                        logger.warning(
                            f"Attempt {attempt+1}: Error {response.status}, "
                            f"retrying after backoff for IP: {ip_address}"
                        )
                        await asyncio.sleep(backoff_factor * (2 ** attempt))
                    else:
                        logger.error(
                            f"Error {response.status}: Failed to fetch data "
                            f"from Censys for IP: {ip_address}"
                            )
                        return {}
            except aiohttp.ClientError as e:
                logger.error(
                    f"Error fetching Censys data for IP: {ip_address}: {e}"
                    )
                await asyncio.sleep(backoff_factor * (2 ** attempt))

        logger.error(
            f"Failed to fetch data from Censys for IP: {ip_address} after "
            f"{retries} attempts."
            )
        return {}

    import asyncio

    async def process_threat_metrix_data(self, threat_metrix_data):
        """Processes and enriches a batch of ThreatMetrix event data 
            asynchronously.

        This method iterates over a DataFrame of ThreatMetrix event 
        data, enriching each event using external APIs (VirusTotal,
        Censys). The result is a list of enriched event records fetched 
        concurrently.

        Args:
            threat_metrix_data (pandas.DataFrame): A DataFrame 
            containing the ThreatMetrix event data. Each row should 
            contain an event body in JSON format.

        Returns:
            list[dict]: A list of dictionaries where each dictionary 
            represents an enriched event, combining original event 
            attributes with additional information from external sources 
            (e.g., IP reputation, device reputation).
        """
        tasks = []
        for row in threat_metrix_data.to_dict(orient='records'):
            tasks.append(self.analyze_with_threat_metrix(row['body']))

        try:
            processed_results = await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error processing batch data: {e}")
            return []

        return processed_results
    
    def run_processing(self, threat_metrix_data):
        """Wrapper to run asynchronous processing in an event loop."""
        return asyncio.run(self.process_threat_metrix_data(threat_metrix_data))

