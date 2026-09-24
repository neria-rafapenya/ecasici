"""Fuente de datos aislada para sustituir mocks por conectores reales."""

from pathlib import Path

from app.services.event_store import EventStore

EVENT_TAXONOMY = {
    'motion_detected': {'label': 'Movimiento detectado', 'category': 'motion'},
    'person_detected': {'label': 'Persona detectada', 'category': 'object'},
    'animal_detected': {'label': 'Animal detectado', 'category': 'object'},
    'vehicle_detected': {'label': 'Vehículo detectado', 'category': 'object'},
    'zone_entry': {'label': 'Entrada en zona', 'category': 'rule'},
    'zone_exit': {'label': 'Salida de zona', 'category': 'rule'},
    'line_crossing': {'label': 'Cruce de línea', 'category': 'rule'},
    'loitering': {'label': 'Permanencia prolongada', 'category': 'rule'},
    'camera_offline': {'label': 'Cámara desconectada', 'category': 'system'},
}

OBJECT_TAXONOMY = {
    'person': 'persona',
    'dog': 'perro',
    'cat': 'gato',
    'bird': 'pájaro',
    'car': 'coche',
    'van': 'furgoneta',
    'truck': 'camión',
    'bus': 'autobús',
    'motorcycle': 'moto',
    'bicycle': 'bicicleta',
    'unknown': 'objeto no identificado',
}

class MockDataProvider:
    def __init__(self):
        self._dashboard = {
            'summary': {'installations': 4, 'cameras': 32, 'openEvents': 3, 'availability': 98.7},
            'installations': [
                {'id': 'eca-001', 'name': 'Centro Logístico Norte', 'city': 'Barcelona', 'status': 'online', 'cameras': 8, 'events': 2, 'health': 99.4},
                {'id': 'eca-002', 'name': 'Almacén Frío Levante', 'city': 'Valencia', 'status': 'online', 'cameras': 12, 'events': 1, 'health': 98.2},
                {'id': 'eca-003', 'name': 'Oficinas ECA SICI', 'city': 'Madrid', 'status': 'attention', 'cameras': 6, 'events': 0, 'health': 96.8},
                {'id': 'eca-004', 'name': 'Parking Cliente Premium', 'city': 'Girona', 'status': 'online', 'cameras': 6, 'events': 0, 'health': 99.9},
            ],
            'events': [
                {'id': 'evt-1042', 'type': 'Actividad detectada', 'location': 'Centro Logístico Norte · Cámara 03', 'time': 'Hace 2 min', 'severity': 'high', 'confidence': 94, 'detail': 'Movimiento en zona restringida fuera de horario'},
                {'id': 'evt-1041', 'type': 'Cámara desconectada', 'location': 'Almacén Frío Levante · Cámara 08', 'time': 'Hace 18 min', 'severity': 'medium', 'confidence': None, 'detail': 'Sin señal recibida durante más de 90 segundos'},
                {'id': 'evt-1040', 'type': 'Vehículo detectado', 'location': 'Centro Logístico Norte · Cámara 07', 'time': 'Hoy, 08:43', 'severity': 'low', 'confidence': 91, 'detail': 'Entrada registrada en zona de carga'},
            ],
        }
        self._cameras = [
            {
                'id': 'cam-01',
                'name': 'Cámara local',
                'type': 'local',
                'status': 'ready',
                'location': 'Centro Logístico Norte',
                'detail': 'Emisión en directo a través de la cámara local',
            },
            {
                'id': 'cam-02',
                'name': 'Cámara remota · Bird Cam sandbox',
                'type': 'remote-api',
                'status': 'online',
                'location': 'Centro Logístico Norte',
                'detail': 'Emisión de aves para simular una cámara remota con actividad ocasional',
                'protocol': 'embed',
                'embed_url': 'https://www.youtube.com/embed/x10vL6_47Dw?autoplay=1&mute=1&playsinline=1',
                'poster_url': 'https://img.youtube.com/vi/x10vL6_47Dw/hqdefault.jpg',
                'city': 'Cornell Bird Cam',
            },
            {
                'id': 'cam-03',
                'name': 'Barcelona · Snapshot público',
                'type': 'public-snapshot',
                'status': 'online',
                'location': 'Referencia pública',
                'detail': 'Imagen pública de tráfico de Barcelona; solo demostración visual',
                'protocol': 'image',
                'image_url': 'https://www.bcn.cat/transit/imatges/PlUrquinaona.gif?hora=',
                'city': 'Barcelona',
                'reference_only': True,
            },
            {
                'id': 'cam-04',
                'name': 'Reus · Plaça Mercadal',
                'type': 'public-webcam',
                'status': 'online',
                'location': 'Reus, Tarragona',
                'detail': 'Cámara pública externa de SkylineWebcams',
                'protocol': 'embed',
                'embed_url': 'https://www.youtube.com/embed/L9HyLjRVN8E?autoplay=1&mute=1&playsinline=1',
                'poster_url': 'https://img.youtube.com/vi/L9HyLjRVN8E/hqdefault.jpg',
                'city': 'Reus',
                'reference_only': True,
                'public_label': 'REUS · PLAÇA MERCADAL',
            },
            {
                'id': 'cam-05',
                'name': "L'Ametlla de Mar · Cámara pública",
                'type': 'public-webcam',
                'status': 'online',
                'location': "L'Ametlla de Mar, Tarragona",
                'detail': 'Cámara pública externa de SkylineWebcams',
                'protocol': 'embed',
                'embed_url': 'https://www.youtube.com/embed/W9DP0Je5rKU?autoplay=1&mute=1&playsinline=1',
                'poster_url': 'https://img.youtube.com/vi/W9DP0Je5rKU/hqdefault.jpg',
                'city': "L'Ametlla de Mar",
                'reference_only': True,
                'public_label': "L'AMETLLA DE MAR",
            },
        ]
        self._events = list(self._dashboard['events'])
        self._next_event_number = 1043
        self._normalise_events()
        self._store = EventStore(Path(__file__).resolve().parents[2] / 'data' / 'events.sqlite3')
        if self._store.is_empty():
            for event in reversed(self._events):
                self._store.save(event)
        else:
            self._events = self._store.list()
            numbers = [int(event['id'].split('-')[-1]) for event in self._events if event.get('id', '').startswith('evt-') and event['id'].split('-')[-1].isdigit()]
            self._next_event_number = max(numbers, default=1042) + 1

    def dashboard(self):
        self._events = self._store.list()
        return {**self._dashboard, 'events': list(self._events)}

    def events(self):
        self._events = self._store.list()
        return list(self._events)

    def taxonomy(self):
        return {
            'event_types': EVENT_TAXONOMY,
            'object_types': OBJECT_TAXONOMY,
            'excluded_attributes': ['gender', 'age', 'race'],
            'appearance_attributes': ['eyewear', 'facial_hair', 'clothing_type', 'clothing_color'],
            'severity_rules': {
                'high': ['line_crossing', 'zone_entry', 'loitering', 'person_in_restricted_zone'],
                'medium': ['vehicle_detected', 'animal_detected', 'camera_offline', 'person_detected'],
                'low': ['motion_detected', 'unknown_object'],
            },
            'review_policy': 'Las detecciones sensibles o ambiguas requieren revisión humana.',
        }

    def severity_for(self, event_type: str, objects: list | None = None, zone: str = 'zona_no_configurada') -> str:
        restricted = zone in {'zona_restringida', 'entrada_principal', 'perimetro'}
        if event_type in {'line_crossing', 'zone_entry', 'loitering'}:
            return 'high'
        if event_type == 'person_detected' and restricted:
            return 'high'
        if event_type in {'person_detected', 'vehicle_detected', 'animal_detected', 'camera_offline'}:
            return 'medium'
        return 'low'

    def _normalise_events(self):
        for event in self._events:
            if event['type'] == 'Vehículo detectado':
                event_type = 'vehicle_detected'
                objects = [{'type': 'car', 'count': 1, 'confidence': event.get('confidence', 0)}]
            elif event['type'] == 'Cámara desconectada':
                event_type = 'camera_offline'
                objects = []
            else:
                event_type = 'motion_detected'
                objects = []
            event.setdefault('event_type', event_type)
            event.setdefault('objects', objects)
            event.setdefault('zone', 'zona_restringida' if event_type == 'motion_detected' else 'zona_no_configurada')
            event.setdefault('direction', None)
            event.setdefault('status', 'closed')
            event.setdefault('requires_human_review', event_type != 'camera_offline')
            event.setdefault('started_at', None)
            event.setdefault('ended_at', None)
            event.setdefault('duration_seconds', None)
            event.setdefault('evidence_url', None)
            event.setdefault('appearance', {})

    def create_motion_event(self, camera_id: str, confidence: int, started_at: str, event_type: str = 'person_detected', objects: list | None = None, zone: str = 'zona_no_configurada', direction: str | None = None):
        camera = next((item for item in self._cameras if item['id'] == camera_id), None)
        event_type = event_type if event_type in EVENT_TAXONOMY else 'motion_detected'
        objects = objects or ([{'type': 'person', 'count': 1, 'confidence': confidence}] if event_type == 'person_detected' else [])
        label = EVENT_TAXONOMY[event_type]['label']
        object_summary = ' · '.join(f"{item.get('count', 1)} {OBJECT_TAXONOMY.get(item.get('type'), 'objeto')}" for item in objects)
        appearance = {
            'eyewear': {'value': True, 'confidence': confidence, 'status': 'visible'},
            'facial_hair': {'value': 'beard', 'confidence': confidence, 'status': 'visible'},
            'clothing_type': {'value': 'jersey', 'confidence': max(confidence - 4, 0), 'status': 'visible'},
            'clothing_color': {'value': 'blue', 'confidence': max(confidence - 7, 0), 'status': 'approximate'},
            'visibility': 'sufficient',
        }
        event = {
            'id': f'evt-{self._next_event_number}',
            'type': label,
            'location': f"{camera['location'] if camera else 'Centro Logístico Norte'} · {camera['name'] if camera else camera_id}",
            'time': 'Ahora',
            'severity': self.severity_for(event_type, objects, zone),
            'confidence': confidence,
            'detail': f"{object_summary + ' · ' if object_summary else ''}{label.lower()} · movimiento en la cámara local",
            'event_type': event_type,
            'objects': objects,
            'zone': zone,
            'direction': direction,
            'camera_id': camera_id,
            'status': 'active',
            'requires_human_review': True,
            'started_at': started_at,
            'ended_at': None,
            'duration_seconds': None,
            'evidence_url': None,
            'appearance': appearance if event_type == 'person_detected' else {},
        }
        self._next_event_number += 1
        self._events.insert(0, event)
        self._store.save(event)
        return event

    def close_motion_event(self, event_id: str, ended_at: str, duration_seconds: float):
        event = next((item for item in self._events if item['id'] == event_id), None)
        if not event:
            return None
        event.update({
            'status': 'closed',
            'ended_at': ended_at,
            'duration_seconds': round(duration_seconds, 2),
            'time': 'Ahora',
            'detail': f"{event['detail'].split(' · movimiento')[0]} · movimiento durante {round(duration_seconds, 1)} s",
        })
        self._store.save(event)
        return event

    def installation(self, installation_id: str):
        for item in self._dashboard['installations']:
            if item['id'] == installation_id:
                return {**item, 'cameras_detail': [f'CAM {i:02d}' for i in range(1, item['cameras'] + 1)]}
        return {'error': 'installation_not_found'}

    def cameras(self):
        return self._cameras
