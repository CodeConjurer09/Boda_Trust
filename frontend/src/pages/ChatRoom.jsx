import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from '../lib/axios'
import Navbar from '../components/Navbar'

export default function ChatRoom(){
  const { roomId } = useParams()
  const [messages, setMessages] = useState([])
  const [text, setText] = useState('')

  useEffect(()=>{
    // load messages
    axios.get(`/chat/messages/?room=${roomId}`)
      .then(res=> setMessages(res.data))
      .catch(err=> console.error(err))
  }, [roomId])

  async function send(){
    if(!text) return
    const res = await axios.post('/chat/messages/', { room: roomId, content: text })
    setMessages(prev => [...prev, res.data])
    setText('')
  }

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <h4>Chat Room {roomId}</h4>
        <div className="card mb-3 p-3" style={{height: '400px', overflowY: 'auto'}}>
          {messages.map(m => (
            <div key={m.id} className="mb-2"><strong>{m.sender_name}</strong>: {m.content}</div>
          ))}
        </div>
        <div className="d-flex">
          <input className="form-control me-2" value={text} onChange={e=>setText(e.target.value)} />
          <button className="btn btn-primary" onClick={send}>Send</button>
        </div>
      </div>
    </>
  )
}
