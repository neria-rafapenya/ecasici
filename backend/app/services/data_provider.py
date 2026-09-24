"""Fuente de datos aislada para sustituir mocks por conectores reales."""

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

    def dashboard(self):
        return self._dashboard

    def installation(self, installation_id: str):
        for item in self._dashboard['installations']:
            if item['id'] == installation_id:
                return {**item, 'cameras_detail': [f'CAM {i:02d}' for i in range(1, item['cameras'] + 1)]}
        return {'error': 'installation_not_found'}
