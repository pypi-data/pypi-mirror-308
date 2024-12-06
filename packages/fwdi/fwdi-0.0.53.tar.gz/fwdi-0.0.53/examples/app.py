import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.path[0]).parent))

#======= Package library ============================
from fwdi.WebApp.web_application import WebApplication
from fwdi.WebApp.web_application_builder import WebApplicationBuilder
#----------------------------------------------------
from Application.dependency_injection import DependencyInjection as ApplicationDependencyInjection
from Presentation.dependency_injection import DependencyInjection as PresentationDependencyInjection
from Infrastructure.dependency_injection  import DependencyInjection as InfrastructureDependencyInjection
#----------------------------------------------------
def start_web_service():
    server_param = {
        'name':'Embedding service',
        'debug':'False'
    }
    builder:WebApplicationBuilder = WebApplication.create_builder(**server_param)
    #------------------------------------------------------------------------------------------
    ApplicationDependencyInjection.AddConfig(builder.services)
    InfrastructureDependencyInjection.AddInfrastructure(builder.services)
    ApplicationDependencyInjection.AddApplication(builder.services)
    #------------------------------------------------------------------------------------------
    PresentationDependencyInjection.AddScope(builder)
    app:WebApplication = builder.build()
    #------------------------------------------------------------------------------------------
    PresentationDependencyInjection.AddEndpoints(app)
    #------------------------------------------------------------------------------------------
    kwargs = {
            'host': "0.0.0.0",
            'port': 5002
        }
    app.run(**kwargs)

if __name__ == "__main__":
    start_web_service()