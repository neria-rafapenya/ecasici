import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Activity, Bell, Camera, ChevronRight, CircleAlert, Clock3, MapPin, Radio, ShieldCheck, Users, Wifi } from 'lucide-react'
import './styles.css'

const mock = {
  summary: { installations: 4, cameras: 32, openEvents: 3, availability: 98.7 },
  installations: [
    { id:'eca-001', name:'Centro Logístico Norte', city:'Barcelona', status:'online', cameras:8, events:2, health:99.4 },
    { id:'eca-002', name:'Almacén Frío Levante', city:'Valencia', status:'online', cameras:12, events:1, health:98.2 },
    { id:'eca-003', name:'Oficinas ECA SICI', city:'Madrid', status:'attention', cameras:6, events:0, health:96.8 },
    { id:'eca-004', name:'Parking Cliente Premium', city:'Girona', status:'online', cameras:6, events:0, health:99.9 },
  ],
  events: [
    { id:'evt-1042', type:'Actividad detectada', location:'Centro Logístico Norte · Cámara 03', time:'Hace 2 min', severity:'high', confidence:94, detail:'Movimiento en zona restringida fuera de horario' },
    { id:'evt-1041', type:'Cámara desconectada', location:'Almacén Frío Levante · Cámara 08', time:'Hace 18 min', severity:'medium', detail:'Sin señal recibida durante más de 90 segundos' },
    { id:'evt-1040', type:'Vehículo detectado', location:'Centro Logístico Norte · Cámara 07', time:'Hoy, 08:43', severity:'low', confidence:91, detail:'Entrada registrada en zona de carga' },
  ]
}

function App() {
  const [data,setData]=useState(mock),[selected,setSelected]=useState(mock.installations[0]),[filter,setFilter]=useState('all'),[loading,setLoading]=useState(true)
  useEffect(()=>{fetch('/api/dashboard').then(r=>r.ok?r.json():Promise.reject()).then(x=>{setData(x);setSelected(x.installations[0])}).catch(()=>{}).finally(()=>setLoading(false))},[])
  const events=data.events.filter(x=>filter==='all'||x.severity===filter)
  return <div className="shell">
    <aside className="side"><div className="brand"><div className="mark">E</div><div><b>ECA SICI</b><small>MONITORING HUB</small></div></div><nav><label>OPERACIONES</label><a className="active"><Activity/>Resumen general</a><a><Camera/>Instalaciones <em>4</em></a><a><CircleAlert/>Eventos <em className="orange">3</em></a><a><MapPin/>Mapa de calor</a><label className="gap">ADMINISTRACIÓN</label><a><Users/>Clientes y accesos</a><a><ShieldCheck/>Auditoría</a></nav><div className="side-bottom"><div className="demo-state"><span className="pulse"/> <div><b>Demo local activa</b><small>Datos simulados · API conectada</small></div></div><div className="profile"><span>RP</span><div><b>Rafa Penya</b><small>Administrador</small></div><ChevronRight/></div></div></aside>
    <main className="main"><header className="top"><div><label>CENTRO DE SUPERVISIÓN / DEMO</label><h1>Buenos días, Rafa <i>✦</i></h1><p>Vista consolidada de tus instalaciones y eventos inteligentes.</p></div><div className="top-right"><span className="live"><span className="pulse"/>Sistema operativo</span><button className="bell"><Bell/><i/></button><span className="date"><Clock3/>24 septiembre 2026</span></div></header>{loading&&<div className="loading">Conectando con el backend mock...</div>}
      <section className="stats"><Stat icon={<MapPin/>} label="Instalaciones activas" value={data.summary.installations} note="Todas las sedes" tone="blue"/><Stat icon={<Camera/>} label="Cámaras monitorizadas" value={data.summary.cameras} note="+8 en este piloto" tone="teal"/><Stat icon={<CircleAlert/>} label="Eventos pendientes" value={data.summary.openEvents} note="Requieren revisión" tone="orange"/><Stat icon={<Wifi/>} label="Disponibilidad" value={`${data.summary.availability}%`} note="Últimas 24 horas" tone="green"/></section>
      <section className="grid"><div className="card"><Head kicker="CONTROL CENTRALIZADO" title="Instalaciones" action="Ver todas"/><div className="sites">{data.installations.map(x=><button className={`site ${selected.id===x.id?'selected':''}`} key={x.id} onClick={()=>setSelected(x)}><span className={`site-icon ${x.status}`}><Radio/></span><span className="site-main"><b>{x.name}</b><small><MapPin/> {x.city} · {x.cameras} cámaras</small></span><span className="site-meta"><b>{x.events?<strong>{x.events} eventos</strong>:'Sin incidencias'}</b><small><span className="dot"/> {x.health}% salud</small></span><ChevronRight/></button>)}</div></div>
      <div className="card camera-card"><Head kicker="VISTA DE INSTALACIÓN" title={selected.name}/><span className="online"><span className="dot"/> Online</span><div className="preview"><span className="cam">CAM 03 · ZONA RESTRINGIDA</span><span className="time">LIVE MOCK · 08:45:12</span><div className="target"><b>Actividad detectada · 94%</b></div><div className="scan"/><footer><span><Radio/> STREAM LOCAL</span><span>IA ACTIVA</span></footer></div><div className="details"><div><small>Último evento</small><b>Hace 2 min</b></div><div><small>Reglas activas</small><b>6 reglas</b></div><div><small>Retención</small><b>7 días</b></div></div></div></section>
      <section className="grid lower"><div className="card"><Head kicker="INTELIGENCIA DE EVENTOS" title="Actividad reciente"/><div className="tabs">{['all','high','medium','low'].map(x=><button className={filter===x?'active':''} onClick={()=>setFilter(x)} key={x}>{x==='all'?'Todos':x==='high'?'Alta':x==='medium'?'Media':'Baja'}</button>)}</div><div className="events">{events.map(x=><div className="event" key={x.id}><span className={`bar ${x.severity}`}/><span className="event-icon"><CircleAlert/></span><span className="event-copy"><b>{x.type}</b><small>{x.location}</small><i>{x.detail}</i></span><span className="event-time">{x.confidence&&<b>{x.confidence}% <small>IA</small></b>}<small>{x.time}</small></span></div>)}</div></div><div className="card value"><Head kicker="PROPUESTA DE VALOR" title="Servicio añadido"/><div className="value-box"><span><Activity/></span><div><b>De cámara a decisión</b><p>Cada evento se contextualiza, se prioriza y queda trazable para ECA SICI y el cliente.</p></div></div><div className="mini"><div><b>8</b><small>cámaras piloto</small></div><div><b>24/7</b><small>supervisión</small></div><div><b>1</b><small>panel central</small></div></div><button className="primary">Ver circuito operativo <ChevronRight/></button></div></section>
      <footer><span><span className="pulse"/> Datos simulados para demostración</span><span>Arquitectura preparada para AWS · <b>v0.1</b></span></footer></main></div>
}
function Head({kicker,title,action}){return <div className="head"><div><label>{kicker}</label><h2>{title}</h2></div>{action&&<button className="link">{action}<ChevronRight/></button>}</div>}
function Stat({icon,label,value,note,tone}){return <div className={`stat ${tone}`}><span className="stat-icon">{icon}</span><div><small>{label}</small><b>{value}</b><i>{note}</i></div></div>}
createRoot(document.getElementById('root')).render(<App/>)
