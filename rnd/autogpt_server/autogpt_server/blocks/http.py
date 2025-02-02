from enum import Enum

import requests

from autogpt_server.data.block import Block, BlockOutput, BlockSchema


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class HttpRequestBlock(Block):
    class Input(BlockSchema):
        url: str
        method: HttpMethod = HttpMethod.POST
        headers: dict[str, str] = {}
        body: object = {}

    class Output(BlockSchema):
        response: object
        client_error: object
        server_error: object

    def __init__(self):
        super().__init__(
            id="6595ae1f-b924-42cb-9a41-551a0611c4b4",
            input_schema=HttpRequestBlock.Input,
            output_schema=HttpRequestBlock.Output,
        )

    def run(self, input_data: Input) -> BlockOutput:
        response = requests.request(
            input_data.method.value,
            input_data.url,
            headers=input_data.headers,
            json=input_data.body,
        )
        if response.status_code // 100 == 2:
            yield "response", response.json()
        elif response.status_code // 100 == 4:
            yield "client_error", response.json()
        elif response.status_code // 100 == 5:
            yield "server_error", response.json()
        else:
            raise ValueError(f"Unexpected status code: {response.status_code}")
