from .config import BYTERAT_URL
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
from typing import Optional, List
import asyncio
import json


class ByteratData:
    def __init__(self, data: List[str], continuation_token: Optional[str]) -> None:
        self.data = pd.DataFrame([json.loads(entry) for entry in data])
        self.continuation_token = continuation_token


class ByteratClientAsync:
    def __init__(self, token: str) -> None:
        self.token = token
        self.transport = AIOHTTPTransport(BYTERAT_URL, headers={"Authorization": token})
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def get_observation_metrics(
        self, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
        query($continuation_token: String) {
            get_observation_data(continuation_token: $continuation_token) {
                data
                continuation_token
            }
        }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query, variable_values={"continuation_token": continuation_token}
            )

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_observation_metrics_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
        query($dataset_key: String!, $continuation_token: String) {
            get_observation_data(dataset_key: $dataset_key, continuation_token: $continuation_token) {
                data
                continuation_token
            }
        }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "continuation_token": continuation_token,
                },
            )

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_observation_metrics_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
        query($dataset_key: String!, $dataset_cycle: Int!, $continuation_token: String) {
            get_observation_data(dataset_key: $dataset_key, dataset_cycle: $dataset_cycle, continuation_token: $continuation_token) {
                data
                continuation_token
            }
        }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query, variable_values={"dataset_key": dataset_key, "dataset_cycle": dataset_cycle}
            )

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_observation_metrics_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
        query($file_name: String!, $continuation_token: String) {
            get_observation_data(file_name: $file_name, continuation_token: $continuation_token) {
                data
                continuation_token
            }
        }
        """
        )

        async with self.client as session:
            response = await session.execute(query, variable_values={"file_name": file_name})

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_metadata(self, continuation_token: Optional[str] = None) -> ByteratData:
        query = gql(
            """
            query($continuation_token: String) {
                get_metadata(continuation_token: $continuation_token) {
                    data,
                    continuation_token
                }
        }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query, variable_values={"continuation_token": continuation_token}
            )

        data = response["get_metadata"]["data"]
        continuation_token = response["get_metadata"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_metadata_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
            query($dataset_key: String!, $continuation_token: String) {
                get_metadata(dataset_key: $dataset_key, continuation_token: $continuation_token) {
                    data,
                    continuation_token
               }
        }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_metadata"]["data"]
        continuation_token = response["get_metadata"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data(self, continuation_token: Optional[str] = None) -> ByteratData:
        query = gql(
            """
                query($continuation_token: String) {
                    get_dataset_cycle_data(continuation_token: $continuation_token) {
                        data,
                        continuation_token
                    }
                }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
                query($dataset_key: String!, $continuation_token: String) {
                    get_dataset_cycle_data(dataset_key: $dataset_key, continuation_token: $continuation_token) {
                        data,
                        continuation_token
                    }
                }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
                query($dataset_key: String!, $dataset_cycle: Int!, $continuation_token: String) {
                    get_dataset_cycle_data(dataset_key: $dataset_key, dataset_cycle: $dataset_cycle, continuation_token: $continuation_token) {
                        data,
                        continuation_token
                    }
                }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "dataset_cycle": dataset_cycle,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(
            """
                query($file_name: String!, $continuation_token: String) {
                    get_dataset_cycle_data(file_name: $file_name, continuation_token: $continuation_token) {
                        data,
                        continuation_token
                    }
                }
        """
        )

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "file_name": file_name,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

class ByteratClientSync:
    def __init__(self, token: str) -> None:
        self.client = ByteratClientAsync(token)

    def get_observation_metrics(self, continuation_token: Optional[str] = None) -> ByteratData:
        return asyncio.run(self.client.get_observation_metrics(continuation_token))

    def get_observation_metrics_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(
            self.client.get_observation_metrics_by_dataset_key(dataset_key, continuation_token)
        )

    def get_observation_metrics_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(
            self.client.get_observation_metrics_by_dataset_key_and_dataset_cycle(
                dataset_key, dataset_cycle, continuation_token
            )
        )

    def get_observation_metrics_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(
            self.client.get_observation_metrics_by_filename(file_name, continuation_token)
        )

    def get_dataset_cycle_data(self, continuation_token: Optional[str] = None) -> ByteratData:
        return asyncio.run(self.client.get_dataset_cycle_data(continuation_token))

    def get_dataset_cycle_data_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(
            self.client.get_dataset_cycle_data_by_dataset_key(dataset_key, continuation_token)
        )

    def get_dataset_cycle_data_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(
            self.client.get_dataset_cycle_data_by_dataset_key_and_dataset_cycle(
                dataset_key, dataset_cycle, continuation_token
            )
        )

    def get_dataset_cycle_data_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(
            self.client.get_dataset_cycle_data_by_filename(file_name, continuation_token)
        )

    def get_metadata(self, continuation_token: Optional[str] = None) -> ByteratData:
        return asyncio.run(self.client.get_metadata(continuation_token))

    def get_metadata_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return asyncio.run(self.client.get_metadata_by_dataset_key(dataset_key, continuation_token))
