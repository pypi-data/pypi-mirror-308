import click
import requests
from rich.console import Console
from rich.pretty import Pretty
from rich.table import Table

console = Console()


def print_response(response):
    if isinstance(response, dict):
        console.print(Pretty(response))
    elif isinstance(response, list):
        table = Table(show_header=True, header_style="bold blue")
        if response:
            for key in response[0].keys():
                table.add_column(key)
            for item in response:
                table.add_row(*[str(item.get(k, "")) for k in response[0].keys()])
        console.print(table)
    else:
        console.print(response)


class CICDClient:
    def __init__(
        self,
        local_base_url="http://127.0.0.1:5000",
        remote_base_url="https://remote-server.com",
    ):
        # param local: Boolean flag to determine whether to use local or remote base URL.
        self.local_base_url = local_base_url
        self.remote_base_url = remote_base_url
        self.headers = {
            "Content-Type": "application/json",
            # Add authentication headers here if needed
        }

    # response = self.client.request('POST', endpoint, payload)
    def request(self, method, endpoint, data=None, local=False):
        base_url = self.local_base_url if local else self.remote_base_url
        url = f"{base_url}{endpoint}"
        # try:
        response = requests.request(
            method=method, url=url, headers=self.headers, json=data
        )
        return response  # Return the JSON response

    def handle_response(self, response=None):
        # print(response)
        if response is not None:
            # handle_response
            status_code = response.status_code
            message = response.json().get("message")

            if status_code == 200:
                # click.echo("Dry run completed successfully!")
                # click.echo(f"Response message: {message}")
                print_response(message)
                # Process the data_received as needed
            elif status_code == 400:
                # click.echo("Dry run failed.")
                click.echo(f"Error message: {message}")
                # Process the data_received as needed

            else:
                # click.echo("Dry run failed.")
                click.echo(f"Error message: {message}")
        else:
            click.echo("No data returned from the backend or the request failed")
