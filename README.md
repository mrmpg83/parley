# Parley

> Real-time chat rooms built with Django Channels and WebSocket. File sharing is next.

![Status](https://img.shields.io/badge/status-early%20development-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Django](https://img.shields.io/badge/Django-Channels-092E20)

> **Heads up:** this project is in early development and is **not production-ready yet**. APIs and structure will change. Feedback and contributions are very welcome.

## About

An open-source web application built on **Django** and **Django Channels**, using **WebSocket** for real-time communication. The goal is a solid, reusable foundation for real-time features (chat first, file sharing next) that anyone can run, study and extend.

## Features

Available now:

- Real-time messaging over WebSocket (ASGI, served by Daphne)
- Chat rooms: join any room by name at `/chat/<room_name>/`
- Messages are stored in the database; the last 10 messages load when you join a room
- Auto-reconnecting WebSocket client
- Simple username-only login for development (no password)
- Django admin at `/admin/`

Planned: see the [Roadmap](#roadmap).

## Getting started

### Prerequisites

- Python 3.12 or newer
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mrmpg83/parley.git
cd parley

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database tables
python manage.py migrate

# 5. (Optional) Create an admin user for /admin/
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Open <http://127.0.0.1:8000>. You will be redirected to a login page: enter any username, then pick a room name. Open a second browser window (or a private window) with a different username and the same room to see messages arrive in real time.

## Project structure

```text
.
├── manage.py
├── requirements.txt
├── djangoChannels/            # Project package: settings, ASGI entry point, root URLs
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Chat/                      # The chat app
│   ├── consumers.py           # WebSocket consumer (ChatConsumer)
│   ├── routing.py             # WebSocket URL routing
│   ├── models.py              # Message model
│   ├── serialalizers.py       # Django REST Framework serializer
│   ├── views.py, urls.py      # HTTP views: login, logout, room list, chat room
│   ├── migrations/
│   ├── static/                # reconnecting-websocket.js
│   └── tests.py
└── templates/chat/            # Login, room selection and chat room pages
```

## How it works

| What | Where |
|------|-------|
| Login page | `/chat/login/` |
| Room list | `/chat/` |
| Chat room | `/chat/<room_name>/` |
| WebSocket endpoint | `ws://<host>/ws/chat/<room_name>/` |

Room names may contain letters, digits and underscores. Each room is a Channels group, so messages are broadcast to everyone connected to the same room.

### WebSocket protocol

The client sends JSON commands:

```json
{"command": "fetch_message"}
{"command": "new_message", "message": "Hello!", "username": "alice"}
```

`fetch_message` returns the last messages of the room to the requesting client. `new_message` saves the message and broadcasts it to the room. Messages are delivered as:

```json
{"message": [{"author": "alice", "content": "Hello!", "timestamp": "2026-10-29T08:15:30.123456Z"}]}
```

## Configuration

Settings live in `djangoChannels/settings.py` and are currently tuned for local development. Before any real deployment, review at least:

- `SECRET_KEY`: generate your own and keep it out of version control
- `DEBUG`: set to `False`
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`: set to your own domains
- `CHANNEL_LAYERS`: the default in-memory layer only works inside a single process. Use a Redis-backed layer (`channels_redis`) when running more than one worker

## Tests

The Selenium tests in `Chat/tests.py` need Google Chrome and a matching `chromedriver` on your `PATH`, plus `pip install selenium`:

```bash
python manage.py test
```

They were written before the login step was added and likely need updating (see the Roadmap).

## Roadmap

- [ ] File sharing in rooms (upload, download, size and type limits)
- [ ] Real authentication; use the authenticated user for every WebSocket message
- [ ] Read settings from environment variables
- [ ] Redis channel layer for multi-process deployments
- [ ] Private and group rooms, message history with pagination
- [ ] Update the automated tests and add CI
- [ ] Docker setup

Have an idea? [Open an issue](../../issues).

## Contributing

Contributions are welcome, from bug reports to new features.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request

For bugs and feature requests, please use the [issue tracker](../../issues).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

Built with [Django](https://www.djangoproject.com/), [Django Channels](https://channels.readthedocs.io/), [Daphne](https://github.com/django/daphne) and [Django REST Framework](https://www.django-rest-framework.org/). The browser client uses [reconnecting-websocket](https://github.com/joewalnes/reconnecting-websocket) by Joe Walnes (MIT).
