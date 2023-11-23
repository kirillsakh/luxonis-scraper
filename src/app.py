import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from sqlalchemy.orm import Session

from config_manager import Config, ConfigManager
from database.adapter import create_database_session
from database.models import Ad
from logging_config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)

cfg: Config = ConfigManager.initialize_from_env().config

def get_config() -> Config:
    """
    Get the configuration object.

    Returns:
        Config: The configuration object.
    """
    return cfg

def get_db_session() -> Session:
    """
    Get a SQLAlchemy database session.

    Returns:
        Session: SQLAlchemy database session.
    """
    psql_kwargs = dict(
        user=cfg.psql_user,
        password=cfg.psql_password,
        host=cfg.psql_host,
        port=cfg.psql_port,
        database=cfg.psql_database
    )
    with create_database_session(**psql_kwargs) as session:
        return session

def setup_jinja_environment() -> Environment:
    """
    Set up the Jinja2 environment.

    Returns:
        Environment: Jinja2 environment.
    """
    # Resolve the templates directory path based on the current script location and configuration.
    templates_dir = Path(__file__).resolve().parent / cfg.static_config['jinja']['dir']
    return Environment(loader=FileSystemLoader(templates_dir))


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(
    session: Session = Depends(get_db_session),
    jinja_env: Environment = Depends(setup_jinja_environment),
    config: Config = Depends(get_config)
):
    """
    Read the root endpoint and render HTML content.

    Args:
        session (Session): SQLAlchemy database session.
        jinja_env (Environment): Jinja2 environment.
        config (Config): Configuration object.

    Returns:
        HTMLResponse: HTML response containing the rendered content.
    """
    try:
        flat_ads = session.query(Ad).all()
        template_name = config.static_config['jinja']['ads_template']
        template = jinja_env.get_template(template_name)
        html_content = template.render(flat_ads=flat_ads)

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(cfg.app_port))
