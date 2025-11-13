# Events feature (scaffold)

This directory contains skeleton files for the `backend-events` feature.

Files:
- `events_models.py` - Event and EventRegistration models
- `events_serializers.py` - DRF serializers
- `events_views.py` - ViewSets and registration action
- `events_service.py` - helpers like `is_event_live` and registration helper
- `events_signals.py` - signal hooks (e.g., notify organizer)
- `events_tests.py` - basic tests

Next steps:
- Add migrations for event models
- Add API routes in `engagement/events_urls.py` and include from project `urls.py`
- Expand notifications and access control
