from pathlib import Path
from werkzeug.datastructures import FileStorage

resources = Path(__file__).parent.parent / "resources"

def test_upload(client):

    with open(resources / "testmd.md", "rb") as file:
        file_storage = FileStorage(stream=file, filename="testmd.md", content_type="text/markdown")

        response = client.post(
            "/flashcards/upload",
            data={
                "setName": "test",
                "setDescription": "A test set description",
                "file": file_storage  # Simulating file upload
            },
        )

    print(response.json)
    assert response.status_code == 200

    #TODO test that the set is successfully uploaded into the db
    
