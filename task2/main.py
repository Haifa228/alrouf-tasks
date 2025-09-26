from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os

# Mock LLM function (no real OpenAI needed)
def mock_llm_generate_email(summary: str, lang: str) -> str:
    if lang == "ar":
        return f"عزيزي {summary['client']},\n\nالسعر الإجمالي: {summary['grand_total']} {summary['currency']}.\nالشروط: {summary['delivery_terms']}.\n\nمع تحياتي،\nAlrouf"
    return f"Dear {summary['client']},\n\nGrand Total: {summary['grand_total']} {summary['currency']}.\nTerms: {summary['delivery_terms']}.\n\nRegards,\nAlrouf"

app = FastAPI()

class Item(BaseModel):
    sku: str
    qty: int
    unit_cost: float
    margin_pct: float

class QuoteInput(BaseModel):
    client: dict  # {"name": str, "contact": str, "lang": str}
    currency: str
    items: List[Item]
    delivery_terms: str
    notes: str

@app.post("/quote")
def create_quote(input: QuoteInput):
    line_totals = []
    grand_total = 0
    for item in input.items:
        price_per_line = item.unit_cost * (1 + item.margin_pct / 100) * item.qty
        line_totals.append({"sku": item.sku, "line_total": price_per_line})
        grand_total += price_per_line

    summary = {
        "client": input.client["name"],
        "grand_total": grand_total,
        "currency": input.currency,
        "delivery_terms": input.delivery_terms,
        "notes": input.notes
    }

    email_draft = mock_llm_generate_email(summary, input.client["lang"])

    return {
        "line_totals": line_totals,
        "grand_total": grand_total,
        "email_draft": email_draft
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
