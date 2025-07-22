from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr, ValidationError, BaseModel
from starlette.middleware.sessions import SessionMiddleware
from email_utils import enviar_email
from config import settings
from datetime import datetime
import json
import uvicorn
import locale


app = FastAPI()
app.add_middleware(SessionMiddleware, settings.SECRET_KEY)
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

locale.setlocale(locale.LC_TIME, 'es_AR.utf8')

with open("perfil.json", encoding="utf-8") as f:
    perfil_data = json.load(f)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    mensaje_estado = request.session.pop("mensaje_estado", None)
    fecha_actual = datetime.now().strftime("%B %Y")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "perfil": perfil_data,
            "mensaje_estado": mensaje_estado,
            "fecha_actual": fecha_actual
        }
    )


class ContactoForm(BaseModel):
    email: EmailStr

@app.post("/contacto")
async def contacto(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    mensaje: str = Form(...),
    telefono: str = Form(None)
):
    if telefono:
        request.session["mensaje_estado"] = ("danger", "Mensaje bloqueado por seguridad.")
        return RedirectResponse(url="/", status_code=303)

    try:
        validacion = ContactoForm(email=email)
        email_validado = validacion.email
    except ValidationError:
        request.session["mensaje_estado"] = ("danger", "El correo electrónico ingresado no es válido.")
        return RedirectResponse(url="/", status_code=303)

    asunto = f"Nuevo mensaje de {nombre} ({email_validado})"
    cuerpo = f"Nombre: {nombre}\nEmail: {email_validado}\nMensaje:\n{mensaje}"

    enviado = await enviar_email(asunto, cuerpo, reply_to=email_validado)

    if enviado:
        request.session["mensaje_estado"] = ("success", "¡Tu mensaje fue enviado correctamente!")
    else:
        request.session["mensaje_estado"] = ("danger", "Error al enviar el mensaje. Por favor, intentá más tarde.")

    return RedirectResponse(url="/", status_code=303)



if __name__ == "__main__":    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False
        )