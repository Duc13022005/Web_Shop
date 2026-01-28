from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import logging

# Configure Logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

# --- Pydantic Models ---
class ContactCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    message: str = Field(..., min_length=10, max_length=1000)

# --- Service/Logic (Simulated) ---
def process_contact_requests(data: ContactCreate):
    """
    Simulate processing: sending email, saving to DB, etc.
    """
    logger.info(f"📧 Sending email notification for: {data.email}")
    # Here you would integrate with an email service (e.g., SES, SMTP)
    # or save to a database.
    logger.info(f"✅ Contact request from {data.first_name} processed successfully.")

# --- Endpoints ---
@router.post("/", status_code=200)
async def submit_contact_form(contact_data: ContactCreate, background_tasks: BackgroundTasks):
    """
    Submit contact form data.
    """
    try:
        logger.info(f"📝 Received contact form submission from: {contact_data.email}")
        
        # Use background task to "send" the email so we don't block the response
        background_tasks.add_task(process_contact_requests, contact_data)
        
        return {
            "success": True,
            "message": "Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể."
        }
    except Exception as e:
        logger.error(f"❌ Error processing contact form: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
