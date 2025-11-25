from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieved_chunks
from app.rag.generator import get_response
from app.rag.prompt import get_prompt
from app.rag.memory import load_memory, save_memory

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask/{document_id}")
def ask(document_id: str, body: QuestionRequest):

    question = body.question

    # 1. Load past chat history for this document
    chat_history = load_memory(document_id)

    # 2. Retrieve relevant chunks
    chunks = retrieved_chunks(document_id, question, k=4)

    # 3. Build context text
    context_text = "\n\n".join(doc.page_content for doc in chunks)

    # 4. Build final prompt
    prompt_template = get_prompt()
    
    final_prompt = prompt_template.format(
        chat_history=chat_history,
        context=context_text,
        question=question
    )

    # 5. Generate answer
    answer = get_response(final_prompt)

    # 6. Save the new turn
    save_memory(document_id, question, answer)

    return {"answer": answer}
