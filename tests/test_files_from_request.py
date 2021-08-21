from app import app

test_client = app.test_client()


# def test_file_files_if_lists_all():
#     assert 'GET' in (test_client.options('/files').headers['Allow'])