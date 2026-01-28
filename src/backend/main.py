"""
Quick Commerce - Cửa Hàng Tiện Lợi
FastAPI Backend Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from auth.router import router as auth_router
from users.router import router as users_router
from catalog.router import router as catalog_router
from inventory.router import router as inventory_router
from orders.router import router as orders_router
from contact.router import router as contact_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Quick Commerce API...")
    yield
    # Shutdown
    print("👋 Shutting down Quick Commerce API...")


app = FastAPI(
    title="Quick Commerce API",
    description="API Backend cho Cửa Hàng Tiện Lợi - Quick Commerce",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
app.include_router(users_router, prefix=settings.API_V1_PREFIX, tags=["Users"])
app.include_router(catalog_router, prefix=settings.API_V1_PREFIX, tags=["Catalog"])
app.include_router(inventory_router, prefix=settings.API_V1_PREFIX, tags=["Inventory"])
app.include_router(orders_router, prefix=settings.API_V1_PREFIX, tags=["Orders"])
app.include_router(contact_router, prefix=settings.API_V1_PREFIX, tags=["Contact"])


@app.get("/", tags=["Root"])
async def root():
    """API Root - Health Check"""
    return {
        "message": "🏪 Quick Commerce API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health Check Endpoint"""
    return {"status": "healthy"}

