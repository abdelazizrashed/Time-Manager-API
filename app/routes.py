def register_routes(api, app, root = 'api'):

    from .auth import register_routes as attach_auth
    from .events import register_routes as attach_events
    from .reminders import  register_routes as attach_reminders
    from .shared import register_routes as attach_shared
    from .tasks import register_routes as attach_tasks


    attach_auth(api, app)
    attach_events(app, api)
    attach_reminders(app, api)
    attach_shared(app, api)
    attach_tasks(app, api)