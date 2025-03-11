from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch, AsyncMock, MagicMock
import logging
import pytest
from fastapi import FastAPI, HTTPException, status
from httpx import AsyncClient, ASGITransport

import second_dir.task.tasks
from second_dir.document_texts.schemas_doc_text import Documents_text_schema_add
from second_dir.documents.doc_models import Documents
from second_dir.document_texts.doc_text_models import Documents_text
from second_dir.documents.doc_router import router
from second_dir.document_texts.doc_text_router import router as router2
from second_dir.main import app
import requests
from second_dir.task.tasks import text_inside_image_celery


ENDPOINT = "http://localhost:8000/"

class Test_1():
    @pytest.fixture
    def test_app(self):
        app = FastAPI()
        app.include_router(router)
        return app

    @pytest.mark.asyncio
    async def test_get_doc_all(self, test_app):
        mock_data = [
            Documents(id=1, path="WWW Ленинград", date_create=datetime.utcnow()),
            Documents(id=2, path="т-т-т-точка-ру", date_create=datetime.utcnow()),

        ]
        with patch("second_dir.documents.doc_repository.DocumentsRepository.get_document_all",
                   new_callable=AsyncMock
                   ) as mock_get_document_all:
            mock_get_document_all.return_value = mock_data

            async with AsyncClient(transport=ASGITransport(app=app),
                                   base_url="http://test") as ac:
                response = await ac.get("/documents/get_all")
                print(response.json())
                logging.warning(f"Для отладки.  response.json(): {response.json()} ")
                assert response.status_code == status.HTTP_200_OK

                expected_data = [
                    {"id": doc.id, "path": doc.path, "date_create": doc.date_create.isoformat()}
                    for doc in mock_data
                ]
                assert response.json() == {"data": expected_data}

class Test_2():
    @pytest.fixture
    def test_app(self):
        app = FastAPI()
        app.include_router(router)
        return app

    @pytest.mark.asyncio
    async def test_text_doc_add(self, test_app):
        with patch("second_dir.document_texts.doc_text_repository.DocumentsTextRepository.add_document",
                   new_callable=AsyncMock
                   ) as mock_post_document_text:
            mock_post_document_text.return_value = 1

            async with AsyncClient(transport=ASGITransport(app=app),
                                   base_url="http://test") as ac:
                request_data = {"id_doc": 1, "text": "новый текст"}
                response = await ac.post("/documents_text/add_text", params=request_data)
                logging.warning(f"Для отладки.  response.json(): {response.json()} ")
                assert response.status_code == status.HTTP_200_OK

                assert response.json() == {"ok": True, "doc_text_id": 1}

    @pytest.mark.asyncio
    async def test_get_doc_text_all(self, test_app):
        mock_fake_data = [
            Documents_text(id=1, id_doc=1, text="текстанит"),
            Documents_text(id=2, id_doc=1, text="текстанитушкООО"),

        ]
        with patch("second_dir.document_texts.doc_text_repository.DocumentsTextRepository.get_document_all",
                   new_callable=AsyncMock
                   ) as mock_get_document_all:
            mock_get_document_all.return_value = mock_fake_data

            async with AsyncClient(transport=ASGITransport(app=app),
                                   base_url="http://test") as ac:
                response = await ac.get("/documents_text/get_all_text")
                logging.warning(f"Для отладки.  response.json(): {response.json()} ")
                assert response.status_code == status.HTTP_200_OK
                expected_data = [
                    {"id": doc_text.id, "id_doc": doc_text.id_doc, "text": doc_text.text}
                    for doc_text in mock_fake_data
                ]
                assert response.json() == {"data": expected_data}

    @pytest.mark.asyncio
    async def test_del_doc_text(self, test_app):
        mock_fake_data = [Documents_text(id=1, id_doc=1, text="текстанит")]
        with patch("second_dir.document_texts.doc_text_repository.DocumentsTextRepository.del_doc_text",
                   new_callable=AsyncMock
                   ) as mock_get_document_all:
            mock_get_document_all.return_value = mock_fake_data

            async with AsyncClient(transport=ASGITransport(app=app),
                                   base_url="http://test") as ac:
                del_id = 1
                response = await ac.delete(f"/documents_text/del_doc_text/{del_id}")
                logging.warning(f"Для отладки.  response.json(): {response.json()} ")
                assert response.status_code == status.HTTP_200_OK
                assert response.json() == {"ok": True, "massage": f"Текст Документа с id {del_id} - был удален"}

    @pytest.mark.asyncio
    async def test_can_skan_image_adn_add_text_in_db(self,test_app):
        with patch("second_dir.task.tasks.text_inside_image_celery.delay") as mock_celery_delay:
            with patch("second_dir.documents.doc_repository.DocumentsRepository.get_path_img_from_id",
                       new_callable=AsyncMock) as mock_get_path:
                with patch("second_dir.document_texts.doc_text_repository.DocumentsTextRepository.text_inside_img_create_in_db",
                           new_callable=AsyncMock) as mock_create_text_in_db:
                    mock_celery_delay.return_value = MagicMock(id="fake-task-id")
                    mock_get_path.return_value = "/fake/path/to/image.png"
                    async with AsyncClient(transport=ASGITransport(app=app),
                                           base_url="http://test") as ac:
                        response = await ac.post("documents_text/doc_analyse",params={"id": 1})
                        assert response.status_code == HTTPStatus.OK

                        assert response.json() == {
                            "status": HTTPStatus.ACCEPTED,
                            "message": "Успешно добавлена в очередь"
                        }

                        mock_celery_delay.assert_called_once_with(1, "/fake/path/to/image.png")




class Test_easy_breasy_api():
    def test_can_call_endpoint(self):
        response_false = requests.get(ENDPOINT)
        assert response_false.status_code == status.HTTP_404_NOT_FOUND

        response_true = requests.get(ENDPOINT+"documents/get_all")
        assert response_true.status_code == status.HTTP_200_OK
    def test_can_add_doc(self):
        fake_path = {"path": "У самурая есть только путь. Вечером снова в дорогу"}
        response = requests.post(ENDPOINT + "documents/add", params=fake_path)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"ok": True}

        fake_path2 = {"path": "Второй путь самурая"}
        response2 = requests.post(ENDPOINT + "documents/add", params=fake_path2)
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json() == {"ok": True}
    def test_can_get_all_doc(self):
        response = requests.get(ENDPOINT+"documents/get_all")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()

        assert len(result["data"]) == 2
        expected_paths = [
            "У самурая есть только путь. Вечером снова в дорогу",
            "Второй путь самурая"
        ]
        assert result["data"][0]["path"] in expected_paths
        assert result["data"][1]["path"] in expected_paths
    def test_can_upload_one_file(self):
        file_path = "second_dir/tests/UPLOAD_FILES/test_text_file.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Тестовое содержимое файла")

        with open(file_path, "rb") as f:
            files = {"upload_file": f}
            response = requests.post(ENDPOINT + "documents/upload_docs/one", files=files)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"ok": True}
    def test_can_del_one_doc(self):
        item_id = 2

        #Проверяем
        response_get_all = requests.get(ENDPOINT + "documents/get_all")
        assert response_get_all.status_code == status.HTTP_200_OK, "Не удалось получить список документов"
        documents = response_get_all.json().get("data", [])
        document_to_delete = next((doc for doc in documents if doc.get("id") == item_id), None)
        assert document_to_delete is not None, f"Документ с ID {item_id} не найден"
        logging.warning(f"Документ для удаления:  document_to_delete: {document_to_delete} ")

        #Удаляем
        response_delete = requests.delete(ENDPOINT + f"documents/del/{item_id}")
        assert response_delete.status_code == status.HTTP_200_OK, "Не удалось удалить документ"
        result = response_delete.json()
        logging.warning(f"Результат удаления: {result}")

        #Надо удостовериться
        response_get_all_after_delete = requests.get(ENDPOINT + "documents/get_all")
        assert response_get_all_after_delete.status_code == status.HTTP_200_OK, "Не удалось получить список документов после удаления"
        documents_after_delete = response_get_all_after_delete.json().get("data", [])
        assert item_id not in [doc.get("id") for doc in
                               documents_after_delete], f"Документ с ID {item_id} все еще существует"



