class Client:
    def __init__(self,
                 client_id: str,
                 full_name: str):
        self.client_id = client_id
        self.full_name = full_name

    @staticmethod
    def deserialize(arr: list[str]) -> 'Client':
        if len(arr) != 2:
            raise ValueError("Invalid number of fields for Client")

        return Client(
            client_id=arr[0],
            full_name=arr[1]
        )

    def serialize(self) -> list[str]:
        return [
            self.client_id,
            self.full_name
        ]
