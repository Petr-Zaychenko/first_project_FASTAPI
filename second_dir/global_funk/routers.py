from second_dir.documents.doc_router import router as router_doc
from second_dir.document_texts.doc_text_router import router as router_doc_text


all_routers = [router_doc, router_doc_text]

__all__ = ["router_doc", "router_doc_text"]