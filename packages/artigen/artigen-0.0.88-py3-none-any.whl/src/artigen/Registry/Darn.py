from .BaseRegistry import BaseRegistry
from collections import defaultdict
import httpx
import json
import os


class Darn(BaseRegistry):
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
        }

    async def _sdk_request(self, service_name, endpoint, method, data=None, headers=None):
        """
        Prepares and forwards the request to the RequestHandler.
        :param service_name: The target service name.
        :param endpoint: The endpoint on the service to be called.
        :param data: Data payload for POST/PUT requests.
        :param headers: Headers including API key for authorization.
        """
        headers = headers or self.headers

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=f"http://gpu.attentions.ai:30060/request-handler-svc/proxy/{service_name}/{endpoint}",
                    headers=headers,
                    content=json.dumps(data) if data else None,
                )
                if response.status_code == 401:
                    return {"status": "error", "message": "Invalid API key"}
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"status": "error", "message": f"HTTP error occurred: {str(e)}"}
            except httpx.RequestError as e:
                return {"status": "error", "message": f"Request error occurred: {str(e)}"}

    async def _create_connection(self, name, connection_type, token=None, projectName=None, fileId=None):
        """
        Creates a connection for the specified type.
        :param name: The name of the connection.
        :param connection_type: The type of the connection (e.g., 'huggingface').
        :param token: Optional token for authentication (e.g., Hugging Face token).
        :return: JSON response from the connection service.
        """
        headers = {**self.headers, "Content-Type": "application/json"}
        data = {
            "name": name,
            "type": connection_type,
        }
        if token:
            data["hfToken"] = token
        if projectName:
            data["projectName"] = projectName
        if fileId:
            data["fileId"] = fileId

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url="http://gpu.attentions.ai:30060/connection",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                return {"status": "error", "message": "Failed to fetch metadata"}
            except Exception as e:
                return {"status": "error", "message": f"Unexpected error occurred: {str(e)}"}

    async def _upload_file(self, file_path, file_type):
        """
        Uploads a file to the server.
        :param file_path: The path to the file to be uploaded.
        :param file_type: The type of the file (default is 'darn').
        :return: JSON response from the file upload service.
        """
        if not os.path.isfile(file_path):
            return {"status": "error", "message": f"Path is not a file: {file_path}"}

        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}

        async with httpx.AsyncClient() as client:
            try:
                with open(file_path, 'rb') as file:
                    response = await client.post(
                        url="http://gpu.attentions.ai:30060/file",
                        headers=self.headers,
                        files={"file": (os.path.basename(file_path), file)},
                        data={"type": file_type}
                    )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"status": "error", "message": f"Unexpected error occurred: {str(e)}"}

    async def create_darn(self, name, description=None, tags=None, dataset=None, darn_type=None, token=None,
                          projectName=None, credentialFile=None):
        if not name:
            return {"status": "error", "message": "Name is required"}

        if not dataset:
            return {"status": "error", "message": "dataset is required"}

        if not darn_type:
            return {"status": "error", "message": "darn_type is required"}

        try:
            # Check if a DARN with the same name already exists
            existing_darns_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            if existing_darns_response.get("status") == "error" and existing_darns_response.get(
                    "message") == "Invalid API key":
                return existing_darns_response

            if existing_darns_response.get("status") == "error":
                return existing_darns_response

            existing_darns = existing_darns_response.get('data', {}).get('darn', [])
            for darn in existing_darns:
                if darn.get('name') == name:
                    return {"status": "error", "message": "DARN name already exists"}

            # Logic for Hugging Face DARN
            if darn_type == "huggingface":
                if not token:
                    return {"status": "error", "message": "token is required"}

                # Check the list of connections
                connection_response = await self._create_connection(
                    name=name,
                    connection_type="huggingface",
                    token=token
                )
                connection_id = connection_response.get('id') or connection_response.get('value', {}).get('id')
                if not connection_id:
                    return {"status": "error", "message": "Connection ID not found in response"}

                async with httpx.AsyncClient() as client:
                    validate_response = await client.post(
                        url=f"http://gpu.attentions.ai:30060/connection/hugging-face/validate-repo-name",
                        headers={**self.headers, "Content-Type": "application/json"},
                        json={
                            "type": "huggingface",
                            "id": connection_id,
                            "resourceName": dataset,
                            "resourceType": "dataset"
                        }
                    )

                if validate_response.status_code != 200:
                    return {"status": "error", "message": "Repository name validation failed"}

                # Generate a parent pin
                parent_pin_response = await self._sdk_request(
                    service_name="pin-service",
                    endpoint="generate-pin",
                    method="POST",
                    data={
                        "type": "darn",
                        "sub_type": "test"
                    }
                )

                if parent_pin_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to generate parent pin"}

                parent_pin = parent_pin_response.get("data", {}).get("pin")
                if not parent_pin:
                    return {"status": "error", "message": "Parent pin not found in response"}
                # Create the DARN with the parent pin
                darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": name,
                        "description": description,
                        "pin_no": [parent_pin],
                        "tags": tags,
                        "metadata": {},
                        "children_metadata": []
                    }
                )

                if darn_response.get("status") != "success":
                    return {"status": "error", "message": darn_response.get("message", "Failed to create DARN")}

                darn_id = darn_response.get("data", {}).get("darn", {}).get("id")
                if not darn_id:
                    return {"status": "error", "message": "DARN ID not found in response"}
                # Process DARN with Hugging Face details
                darn_call = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": "",
                        "parent": darn_id,
                        "pin_no": [parent_pin],
                        "metadata": {
                            "type": "huggingface",
                            "connection_id": connection_id,
                            "details": {
                                "details": [
                                    {
                                        "dataset": dataset,
                                        "type": "dataset"
                                    }
                                ]
                            }
                        }
                    }
                )

                if darn_call.get("status") != "success":
                    return {"status": "error", "message": darn_call.get("message", "Failed to create DARN")}

            elif darn_type == "local":
                # Generate a parent pin
                parent_pin_response = await self._sdk_request(
                    service_name="pin-service",
                    endpoint="generate-pin",
                    method="POST",
                    data={
                        "type": "darn",
                        "sub_type": "test"
                    }
                )

                if parent_pin_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to generate parent pin"}

                parent_pin = parent_pin_response.get("data", {}).get("pin")
                if not parent_pin:
                    return {"status": "error", "message": "Parent pin not found in response"}

                # Create the DARN with the parent pin
                darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": name,
                        "description": description,
                        "pin_no": [parent_pin],
                        "tags": tags,
                        "metadata": {},
                        "children_metadata": []
                    }
                )

                if darn_response.get("status") != "success":
                    return {"status": "error", "message": darn_response.get("message", "Failed to create DARN")}

                darn_id = darn_response.get("data", {}).get("darn", {}).get("id")
                if not darn_id:
                    return {"status": "error", "message": "DARN ID not found in response"}

                children_metadata = []
                for value in dataset:
                    file_upload_response = await self._upload_file(value, file_type="darn")

                    # Generate a child pin for each file
                    child_pin_response = await self._sdk_request(
                        service_name="pin-service",
                        endpoint="generate-pin",
                        method="POST",
                        data={
                            "type": "darn",
                            "sub_type": "test",
                            "parent": parent_pin
                        }
                    )

                    if child_pin_response.get("status") != "success":
                        return {"status": "error", "message": "Failed to generate child pin"}

                    child_pin = child_pin_response.get("data", {}).get("pin")

                    if not child_pin:
                        return {"status": "error", "message": "Child pin not found in response"}

                    # Create a child DARN with the file metadata
                    child_darn_response = await self._sdk_request(
                        service_name="darn-service",
                        endpoint="process-darn",
                        method="POST",
                        data={
                            "name": str(file_upload_response.get("fileName")),
                            "parent": darn_id,
                            "pin_no": [child_pin],
                            "tags": tags,
                            "metadata": {
                                "details": {
                                    "duration": file_upload_response.get("duration"),
                                    "fileName": file_upload_response.get("fileName"),
                                    "extension": file_upload_response.get("extension"),
                                    "fileSize": file_upload_response.get("fileSize"),
                                    "downloadUrl": file_upload_response.get("downloadUrl"),
                                    "publicUrl": None,
                                    "id": file_upload_response.get("id"),
                                    "type": "darn"
                                },
                                "type": "local",
                                "created_by": None
                            },
                            "children_metadata": []
                        }
                    )

                    if child_darn_response.get("status") != "success":
                        return {"status": "error", "message": "Failed to create child DARN"}

                    # Add to children metadata
                    children_metadata.append({
                        "pin_no": child_darn_response.get("data", {}).get("darn", {}).get("pin_no", []),
                        "type": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("type", ""),
                        "connection_id": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                            "details", {}).get("id", ""),
                        "details": {
                            "details": [
                                {
                                    "name": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                                        "details", {}).get("fileName"),
                                    "size": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                                        "details", {}).get("fileSize"),
                                    "file_type": child_darn_response.get("data", {}).get("darn", {}).get("metadata",
                                                                                                         {}).get(
                                        "details",
                                        {}).get(
                                        "extension"),
                                    "downloadUrl": child_darn_response.get("data", {}).get("darn", {}).get("metadata",
                                                                                                           {}).get(
                                        "details", {}).get("downloadUrl"),
                                    "duration": child_darn_response.get("data", {}).get("darn", {}).get("metadata",
                                                                                                        {}).get(
                                        "details", {}).get("duration")
                                }
                            ]
                        }
                    })

                update_child_metadata = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="update-darn",
                    method="PUT",
                    data={
                        "id": darn_id,
                        "children_metadata": [
                            {
                                "pin_no": parent_pin,
                                "type": "local",
                                "details": {}
                            }
                        ]
                    }
                )
                if update_child_metadata.get("status") != "success":
                    return {"status": "error", "message": "Failed to update DARN with children metadata"}

                # Update DARN with children metadata
                update_child_metadata = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="update-darn",
                    method="PUT",
                    data={
                        "id": darn_id,
                        "pin_no": parent_pin,
                    }
                )
                if update_child_metadata.get("status") != "success":
                    return {"status": "error", "message": "Failed to update DARN with children metadata"}

            elif darn_type == "bigquery":
                if not projectName:
                    return {"status": "error", "message": "projectName is required"}

                upload_response = await self._upload_file(file_path=credentialFile, file_type="credentials")

                credentials_id = upload_response.get("id")
                if not credentials_id:
                    return {"status": "error", "message": "Credentials ID not found in response"}

                connection_response = await self._create_connection(
                    name="validConnection",
                    connection_type="bigquery",
                    projectName=projectName,
                    fileId=credentials_id
                )
                if connection_response.status_code != 200:
                    return {"status": "error", "message": "Failed to upload credentials"}
                connection_id = connection_response.get("id")

                async with httpx.AsyncClient() as client:
                    connection_response = await client.get(
                        url=f"http://gpu.attentions.ai:30060/connection/{connection_id}",
                        headers=self.headers
                    )

                if connection_response.status_code != 200:
                    return {"status": "error", "message": "Failed to make connection with credentials"}

                database_tables = defaultdict(list)
                for item in dataset:
                    database, table = item.split(".")
                    database_tables[database].append(table)

                json_body = [
                    {"database_name": db, "tables": [{"name": table} for table in tables]}
                    for db, tables in database_tables.items()
                ]
                selected_database = len(json_body)
                selected_table = sum(len(entry["tables"]) for entry in json_body)

                async with httpx.AsyncClient() as client:
                    metadata_response = await client.get(
                        url=f"http://gpu.attentions.ai:30060/connection/metadata/{connection_id}",
                        headers=self.headers
                    )

                if metadata_response.status_code != 200:
                    return {"status": "error", "message": "Failed to fetch metadata"}

                metadata = metadata_response.json()
                total_databases = len(metadata)
                total_tables = sum(len(entry['tables']) for entry in metadata)
                # Verify json_body against fetched metadata
                for db_entry in json_body:
                    db_name = db_entry["database_name"]
                    tables = db_entry["tables"]
                    table_names = [table["name"] for table in tables]

                    # Find the corresponding database in the metadata
                    metadata_db = next((item for item in metadata if item["database"] == db_name), None)
                    if not metadata_db:
                        return {"status": "error", "message": f"Database not found: {db_name}"}

                    # Check if all tables exist in the metadata
                    for table in table_names:
                        if table not in metadata_db["tables"]:
                            return {"status": "error", "message": f"Table not found: {table} in database {db_name}"}

                # Step 3: Generate a parent pin
                parent_pin_response = await self._sdk_request(
                    service_name="pin-service",
                    endpoint="generate-pin",
                    method="POST",
                    data={
                        "type": "darn",
                        "sub_type": "asset-registration"
                    }
                )

                if parent_pin_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to generate parent pin"}

                parent_pin = parent_pin_response.get("data", {}).get("pin")
                if not parent_pin:
                    return {"status": "error", "message": "Parent pin not found in response"}

                # Step 2: Create the DARN with the parent pin
                darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": name,
                        "description": description,
                        "pin_no": [parent_pin],
                        "tags": tags,
                        "metadata": {},
                        "children_metadata": []
                    }
                )

                if darn_response.get("status") != "success":
                    return {"status": "error", "message": darn_response.get("message", "Failed to create DARN")}

                darn_id = darn_response.get("data", {}).get("darn", {}).get("id")
                if not darn_id:
                    return {"status": "error", "message": "DARN ID not found in response"}

                darn_call = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": "",
                        "parent": darn_id,
                        "pin_no": [parent_pin],
                        "metadata": {
                            "type": "bigquery",
                            "connection_id": connection_id,
                            "details": {
                                "total_db": total_databases,
                                "selected_db": selected_database,
                                "total_table": total_tables,
                                "selected_table": selected_table,
                                "details": json_body
                            }
                        }
                    }
                )

                if darn_call.get("status") != "success":
                    return {"status": "error", "message": darn_response.get("message", "Failed to create DARN")}

            else:
                return {"status": "error", "message": f"Unsupported darn_type: {darn_type}"}

            return {
                "status": "success",
                "message": "DARN created successfully",
            }

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def update_darn(self, name, tags=None, file_paths=None):
        if not file_paths:
            return {"status": "error", "message": "file_paths is required"}

        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            if response.get("status") == "error":
                return response

            darn_list = response.get('data', {}).get('darn', [])
            darn_id = None

            # Iterate over the list to find the DARN with the specified name
            for darn in darn_list:
                if darn.get('name') == name:
                    darn_id = darn.get('id')
                    break

            if not darn_id:
                return {"status": "error", "message": f"No DARN found with name: {name}"}

            # Step 1: Generate a parent pin
            parent_pin_response = await self._sdk_request(
                service_name="pin-service",
                endpoint="generate-pin",
                method="POST",
                data={
                    "type": "darn",
                    "sub_type": "test"
                }
            )

            if parent_pin_response.get("status") != "success":
                return {"status": "error", "message": "Failed to generate parent pin"}

            parent_pin = parent_pin_response.get("data", {}).get("pin")
            if not parent_pin:
                return {"status": "error", "message": "Parent pin not found in response"}

            #  Step 2: Update the DARN with the parent pin
            darn_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "children_metadata": [{
                        "pin_no": " ",
                        "type": "local",
                        "connection_id": "",
                        "details": {
                            "details": {

                            }
                        }
                    }
                    ]
                }
            )

            if darn_response.get("status") != "success":
                return {"status": "error", "message": "Failed to create DARN"}

            darn_id = darn_response.get("data", {}).get("darn", {}).get("id")
            if not darn_id:
                return {"status": "error", "message": "DARN ID not found in response"}

            # Step 3: Process each file
            children_metadata = []
            for file_path in file_paths:
                if not os.path.isfile(file_path):
                    return {"status": "error", "message": f"Path is not a file: {file_path}"}

                if not os.path.exists(file_path):
                    return {"status": "error", "message": f"File not found: {file_path}"}

                # Generate a child pin for each file
                child_pin_response = await self._sdk_request(
                    service_name="pin-service",
                    endpoint="generate-pin",
                    method="POST",
                    data={
                        "type": "darn",
                        "sub_type": "test",
                        "parent": parent_pin
                    }
                )

                if child_pin_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to generate child pin"}

                child_pin = child_pin_response.get("data", {}).get("pin")

                if not child_pin:
                    return {"status": "error", "message": "Child pin not found in response"}

                async with httpx.AsyncClient() as client:
                    with open(file_path, 'rb') as file:
                        file_upload_response = await client.post(
                            url="http://gpu.attentions.ai:30060/file",
                            headers=self.headers,
                            files={"file": (os.path.basename(file_path), file)},
                            data={"type": "darn"}
                        )

                if file_upload_response.status_code != 200:
                    return {"status": "error", "message": "Failed to upload file"}

                file_metadata = file_upload_response.json()

                # Create a child DARN with the file metadata
                child_darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": str(file_metadata.get("fileName")),
                        "parent": darn_id,
                        "pin_no": [child_pin],
                        "tags": tags,
                        "metadata": {
                            "details": {
                                "duration": file_metadata.get("duration"),
                                "fileName": file_metadata.get("fileName"),
                                "extension": file_metadata.get("extension"),
                                "fileSize": file_metadata.get("fileSize"),
                                "downloadUrl": file_metadata.get("downloadUrl"),
                                "publicUrl": None,
                                "id": file_metadata.get("id"),
                                "type": "darn"
                            },
                            "type": "local",
                            "created_by": None
                        },
                        "children_metadata": []
                    }
                )

                if child_darn_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to create child DARN"}

                children_metadata.append({
                    "pin_no": child_darn_response.get("data", {}).get("darn", {}).get("pin_no", []),
                    "type": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("type", ""),
                    "connection_id": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                        "details", {}).get("id", ""),
                    "details": {
                        "details": [
                            {
                                "name": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                                    "details", {}).get("fileName"),
                                "size": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                                    "details", {}).get("fileSize"),
                                "file_type": child_darn_response.get("data", {}).get("darn", {}).get("metadata",
                                                                                                     {}).get("details",
                                                                                                             {}).get(
                                    "extension"),
                                "downloadUrl": child_darn_response.get("data", {}).get("darn", {}).get("metadata",
                                                                                                       {}).get(
                                    "details", {}).get("downloadUrl"),
                                "duration": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                                    "details", {}).get("duration")
                            }
                        ]
                    }
                })

            update_child_metadata = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "children_metadata": [
                        {
                            "pin_no": "",
                            "type": "local",
                            "details": {}
                        }
                    ]
                }
            )
            if update_child_metadata.get("status") != "success":
                return {"status": "error", "message": "Failed to update DARN with children metadata"}

            update_darn_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "pin_no": parent_pin,
                }
            )

            if update_darn_response.get("status") != "success":
                return {"status": "error", "message": "Failed to update DARN with children metadata"}

            return {
                "status": "success",
                "message": "DARN updated successfully",
            }

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def list_darn(self):
        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            # Check if the response indicates an invalid API key
            if response.get("status") == "error" and response.get("message") == "Invalid API key":
                return response

            darn_list = response.get('data', {}).get('darn', [])

            table_data = [
                {
                    "Darn Name": darn.get('name'),
                    "Description": darn.get('description'),
                    "Tags": darn.get('tags'),
                    "Status": darn.get('status')
                }
                for darn in darn_list
            ]

            formatted_output = "\n".join(str(entry) for entry in table_data)

            return formatted_output
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    async def delete_darn(self, name):
        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            # Check if the response indicates an invalid API key
            if response.get("status") == "error" and response.get("message") == "Invalid API key":
                return response

            darn_list = response.get('data', {}).get('darn', [])

            # Find the ID of the DARN to delete
            id_to_delete = None
            for darn in darn_list:
                if darn.get('name') == name:
                    id_to_delete = darn.get('id')
                    break

            if not id_to_delete:
                return {"status": "error", "message": f"No DARN found with name: {name}"}

            delete_response = await self._sdk_request(
                service_name="darn-service",
                endpoint=f"delete-darn?id={id_to_delete}",
                method="DELETE",
            )
            return delete_response

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
