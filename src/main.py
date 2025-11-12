from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.api.v1.auth import router as auth_router
from src.api.v1.admin import router as admin_router
from src.utils.dependencies import get_current_user
from src.db.session import engine, Base

app = FastAPI(title="User Platform", version="1.0.0")

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

# Static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Templates
templates = Jinja2Templates(directory="src/templates")

# HTML pages
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user=Depends(get_current_user)):
    try:
        template = "dashboard_admin.html" if user.role == "admin" else "dashboard_user.html"
        return templates.TemplateResponse(template, {"request": request, "user": user})
    except HTTPException:
        # Redirect to login if not authenticated
        return RedirectResponse(url="/login", status_code=303)

# Create tables on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)