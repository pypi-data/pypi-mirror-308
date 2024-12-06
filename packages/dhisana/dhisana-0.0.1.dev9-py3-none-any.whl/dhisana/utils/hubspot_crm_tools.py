# Hubspot CRM Tools
import os
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool
from typing import Optional, List, Dict, Any

@assistant_tool
async def fetch_hubspot_object_info(
    object_type: str,
    object_id: Optional[str] = None,
    object_ids: Optional[List[str]] = None,
    associations: Optional[List[str]] = None,
    properties: Optional[List[str]] = None
):
    """
    Fetch information for any HubSpot object(s) (contacts, companies, deals, tickets, lists, etc.) using their ID(s) and type.
    Parameters:
    - **object_type** (*str*): Type of the object (e.g., "contacts", "companies", "deals", "tickets", "lists").
    - **object_id** (*str*, optional): Unique HubSpot object ID for fetching a single object.
    - **object_ids** (*List[str]*, optional): List of unique HubSpot object IDs for multiple.
    - **associations** (*List[str]*, optional): List of associated object types to include in the response.
    - **properties** (*List[str]*, optional): List of properties to include in the response.
    # Example below to get company information of contact.
    await fetch_hubspot_object_info(
        object_type="contacts",
        object_id="12345",  # Replace with the contact's ID
        associations=["companies"]
    )
    """

    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        return {'error': "HubSpot API key not found in environment variables"}

    if not object_id and not object_ids:
        return {'error': "HubSpot object ID(s) must be provided"}

    if not object_type:
        return {'error': "HubSpot object type must be provided"}

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    params = {}
    if properties:
        params['properties'] = ','.join(properties)
    if associations:
        params['associations'] = ','.join(associations)

    try:
        async with aiohttp.ClientSession() as session:
            if object_type.lower() == 'lists':
                # Handle lists endpoint
                if object_id:
                    url = f"https://api.hubapi.com/contacts/v1/lists/{object_id}"
                    async with session.get(url, headers=headers, params=params) as response:
                        result = await response.json()
                        if response.status != 200:
                            return {'error': result}
                        return result
                else:
                    return {'error': "For object_type 'lists', object_id must be provided"}
            else:
                if object_ids:
                    # Batch read
                    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}/batch/read"
                    payload = {
                        "inputs": [{"id": oid} for oid in object_ids]
                    }
                    if properties:
                        payload["properties"] = properties
                    if associations:
                        payload["associations"] = associations
                    async with session.post(url, headers=headers, json=payload) as response:
                        result = await response.json()
                        if response.status != 200:
                            return {'error': result}
                        return result
                else:
                    # Single object read
                    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}/{object_id}"
                    async with session.get(url, headers=headers, params=params) as response:
                        result = await response.json()
                        if response.status != 200:
                            return {'error': result}
                        return result
    except Exception as e:
        return {'error': str(e)}


@assistant_tool
async def search_hubspot_objects(
    object_type: str,
    filters: Optional[List[Dict[str, Any]]] = None,
    filter_groups: Optional[List[Dict[str, Any]]] = None,
    sorts: Optional[List[str]] = None,
    query: Optional[str] = None,
    properties: Optional[List[str]] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None
):
    """
    Search for HubSpot objects (contacts, companies, deals, tickets, etc.) using filters and filter groups.
    Parameters:
    - **object_type** (*str*): Type of the object (e.g., "contacts", "companies", "deals", "tickets").
    - **filters** (*List[Dict[str, Any]]*, optional): List of filters.
    - **filter_groups** (*List[Dict[str, Any]]*, optional): List of filter groups.
    - **sorts** (*List[str]*, optional): List of sort criteria.
    - **query** (*str*, optional): Search query string.
    - **properties** (*List[str]*, optional): List of properties to include in the response.
    - **limit** (*int*, optional): Maximum number of results to return.
    - **after** (*str*, optional): Pagination cursor.
    Returns:
    - **dict**: JSON response from the HubSpot API containing the search results.
    Examples:
    await search_hubspot_objects(
        object_type="contacts",
        filters=[
            {"propertyName": "firstname", "operator": "EQ", "value": "John"},
        ],
        properties=["firstname", "lastname", "email"]
    )
    """

    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        return {'error': "HubSpot API key not found in environment variables"}

    if not object_type:
        return {'error': "HubSpot object type must be provided"}

    if not any([filters, filter_groups, query]):
        return {'error': "At least one of filters, filter_groups, or query must be provided"}

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"https://api.hubapi.com/crm/v3/objects/{object_type}/search"

    payload: Dict[str, Any] = {}
    if filters:
        payload["filterGroups"] = [{"filters": filters}]
    if filter_groups:
        payload["filterGroups"] = filter_groups
    if sorts:
        payload["sorts"] = sorts
    if query:
        payload["query"] = query
    if properties:
        payload["properties"] = properties
    if limit:
        payload["limit"] = limit
    if after:
        payload["after"] = after

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                return result
    except Exception as e:
        return {'error': str(e)}


@assistant_tool
async def fetch_hubspot_lead_info(first_name: str = None, last_name: str = None, email: str = None, linkedin_url: str = None, phone_number: str = None, hubspot_id: str = None):
    """
    Fetch lead information from HubSpot based on provided parameters.

    This function sends an asynchronous GET request to the HubSpot Contacts API to retrieve the lead's information based on the available non-empty parameters.
    
    Parameters:
    first_name (str): Lead's first name.
    last_name (str): Lead's last name.
    email (str): Lead's email address.
    linkedin_url (str): Lead's LinkedIn URL.
    phone_number (str): Lead's phone number.
    hubspot_id (str): Lead's HubSpot contact ID.

    Returns:
    dict: JSON response from the HubSpot API containing lead information.

    Raises:
    ValueError: If the HubSpot API key is not found in the environment variables or if no search parameter is provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    # Construct the search parameters based on non-empty inputs
    search_params = {}
    if first_name:
        search_params["properties.firstname"] = first_name
    if last_name:
        search_params["properties.lastname"] = last_name
    if email:
        search_params["properties.email"] = email
    if linkedin_url:
        search_params["properties.linkedinurl"] = linkedin_url
    if phone_number:
        search_params["properties.phone"] = phone_number
    if hubspot_id:
        search_params["id"] = hubspot_id
    
    if not search_params:
        raise ValueError("At least one search parameter must be provided")
    
    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Building filters for search based on the available parameters
    filters = [{"propertyName": key, "operator": "EQ", "value": value} for key, value in search_params.items()]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json={"filters": filters}) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result


@assistant_tool
async def fetch_hubspot_contact_info(hubspot_id: str = None, email: str = None):
    """
    Fetch contact information from HubSpot using the contact's HubSpot ID or email.

    This function sends an asynchronous GET request to the HubSpot Contacts API to retrieve detailed contact information.
    
    Parameters:
    hubspot_id (str): Unique HubSpot contact ID.
    email (str): Contact's email address.

    Returns:
    dict: JSON response from the HubSpot API containing contact information.

    Raises:
    ValueError: If the HubSpot API key is not provided or if neither hubspot_id nor email is provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not hubspot_id and not email:
        raise ValueError("Either HubSpot contact ID or email must be provided")

    # Construct the URL based on the parameter provided
    if hubspot_id:
        url = f"https://api.hubapi.com/crm/v3/objects/contacts/{hubspot_id}"
    else:
        url = f"https://api.hubapi.com/crm/v3/objects/contacts/search"
    
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if hubspot_id:
            # Lookup by HubSpot ID
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                result = await response.json()
                return result
        else:
            # Lookup by email using search endpoint
            payload = {
                "filters": [
                    {
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email
                    }
                ]
            }
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                result = await response.json()
                return result

@assistant_tool
async def fetch_hubspot_list_records(list_id: str, max_entries_to_read: int = 2500) -> List[dict]:
    """
    Fetch records from a specific HubSpot list using the list's ID.

    This function sends asynchronous GET requests to the HubSpot Lists API to retrieve contact records associated with a given list, handling pagination as required.

    Parameters:
    - list_id (str): Unique HubSpot list ID.
    - max_entries_to_read (int, optional): Maximum number of entries to read. Defaults to 2500.

    Returns:
    - List[dict]: List of contacts from the HubSpot list.

    Raises:
    - ValueError: If the HubSpot API key, list ID, or max_entries_to_read is invalid.
    - Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")

    if not list_id:
        raise ValueError("HubSpot list ID must be provided")

    if not max_entries_to_read or max_entries_to_read <= 0:
        raise ValueError("max_entries_to_read must be a positive integer")

    # URL to fetch contacts within the specified list
    url = f"https://api.hubapi.com/contacts/v1/lists/{list_id}/contacts/all"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    contacts = []
    has_more = True
    vid_offset = None

    async with aiohttp.ClientSession() as session:
        while len(contacts) < max_entries_to_read and has_more:
            params = {
                'count': min(100, max_entries_to_read - len(contacts))
            }
            if vid_offset:
                params['vidOffset'] = vid_offset

            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                result = await response.json()

                contacts.extend(result.get('contacts', []))

                has_more = result.get('has-more', False)
                vid_offset = result.get('vid-offset', None)

    return contacts


@assistant_tool
async def update_hubspot_contact_properties(contact_id: str, properties: dict):
    """
    Update contact properties in HubSpot for a given contact ID.

    This function sends an asynchronous PATCH request to the HubSpot Contacts API to update specified contact properties.
    
    Parameters:
    contact_id (str): Unique HubSpot contact ID.
    properties (dict): Dictionary of properties to update, with property names as keys and new values as values.

    Returns:
    dict: JSON response from the HubSpot API containing the updated contact information.

    Raises:
    ValueError: If the HubSpot API key, contact ID, or properties are not provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not contact_id:
        raise ValueError("HubSpot contact ID must be provided")

    if not properties:
        raise ValueError("Properties dictionary must be provided")

    # URL to update contact properties for the specified contact ID
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Payload with properties to update
    payload = {
        "properties": properties
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result

@assistant_tool
async def update_hubspot_lead_properties(lead_id: str, properties: dict):
    """
    Update lead properties in HubSpot for a given lead ID.

    This function sends an asynchronous PATCH request to the HubSpot CRM API to update specified lead properties.
    
    Parameters:
    lead_id (str): Unique HubSpot lead ID.
    properties (dict): Dictionary of properties to update, with property names as keys and new values as values.

    Returns:
    dict: JSON response from the HubSpot API containing the updated lead information.

    Raises:
    ValueError: If the HubSpot API key, lead ID, or properties are not provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not lead_id:
        raise ValueError("HubSpot lead ID must be provided")

    if not properties:
        raise ValueError("Properties dictionary must be provided")

    # URL to update lead properties for the specified lead ID
    url = f"https://api.hubapi.com/crm/v3/objects/leads/{lead_id}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Payload with properties to update
    payload = {
        "properties": properties
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result

@assistant_tool
async def fetch_hubspot_company_info(company_id: str = None, name: str = None, domain: str = None):
    """
    Fetch company information from HubSpot using the company's HubSpot ID, name, or domain.

    This function sends an asynchronous request to the HubSpot Companies API to retrieve detailed company information.
    
    Parameters:
    company_id (str): Unique HubSpot company ID.
    name (str): Name of the company.
    domain (str): Domain of the company.

    Returns:
    dict: JSON response from the HubSpot API containing company information.

    Raises:
    ValueError: If the HubSpot API key is not provided or if none of the parameters are provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not (company_id or name or domain):
        raise ValueError("At least one of company_id, name, or domain must be provided")

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if company_id:
            # Direct lookup by company ID
            url = f"https://api.hubapi.com/crm/v3/objects/companies/{company_id}"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                result = await response.json()
                return result
        else:
            # Search lookup by name or domain
            url = "https://api.hubapi.com/crm/v3/objects/companies/search"
            filters = []
            if name:
                filters.append({"propertyName": "name", "operator": "EQ", "value": name})
            if domain:
                filters.append({"propertyName": "domain", "operator": "EQ", "value": domain})
            
            payload = {
                "filters": filters
            }
            
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Received status code {response.status}")
                result = await response.json()
                return result


@assistant_tool
async def fetch_hubspot_contact_associations(contact_id: str, to_object_type: str):
    """
    Fetch associations from a contact to other objects in HubSpot.

    This function sends an asynchronous GET request to the HubSpot Associations API to retrieve 
    associated records of a specified type for a contact.
    
    Parameters:
    contact_id (str): Unique HubSpot contact ID.
    to_object_type (str): The object type to retrieve associations for (e.g., 'companies', 'deals', 'tickets').
    
    Returns:
    dict: JSON response from the HubSpot API containing association information.

    Raises:
    ValueError: If the HubSpot API key or contact ID is not provided.
    Exception: If the response status code from the HubSpot API is not 200.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not contact_id:
        raise ValueError("HubSpot contact ID must be provided")
    
    if not to_object_type:
        raise ValueError("Target object type must be provided")
    
    # URL to fetch associations from the contact to the specified object type
    url = f"https://api.hubapi.com/crm/v4/objects/contacts/{contact_id}/associations/{to_object_type}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result





@assistant_tool
async def fetch_hubspot_list_by_name(list_name: str):
    """
    Fetch information for a specific HubSpot list using the list's name.

    This function sends an asynchronous GET request to the HubSpot Lists API to retrieve all lists,
    then filters to find a list that matches the specified name.
    
    Parameters:
    list_name (str): Name of the HubSpot list to find.

    Returns:
    dict: JSON response from the HubSpot API containing the list information if found.

    Raises:
    ValueError: If the HubSpot API key or list name is not provided.
    Exception: If the response status code from the HubSpot API is not 200 or if the list is not found.
    """
    HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not HUBSPOT_API_KEY:
        raise ValueError("HubSpot API key not found in environment variables")
    
    if not list_name:
        raise ValueError("HubSpot list name must be provided")

    # URL to fetch all lists
    url = "https://api.hubapi.com/contacts/v1/lists"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            lists = await response.json()

            # Search for the list with the specified name
            for hubspot_list in lists.get("lists", []):
                if hubspot_list.get("name") == list_name:
                    return hubspot_list

            # Raise an error if the list is not found
            raise Exception(f"List with name '{list_name}' not found")