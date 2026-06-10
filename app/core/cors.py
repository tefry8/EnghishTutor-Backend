from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Cambia esto por los dominios permitidos en producción
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
