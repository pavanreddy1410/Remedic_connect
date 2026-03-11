import { useState } from 'react'
import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import { api } from './lib/api'

const roles = ['patient', 'lab', 'pharmacy', 'doctor', 'admin']

function AuthPanel() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: 'Demo User', email: '', password: '', role: 'patient' })
  const [message, setMessage] = useState('')

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const register = async () => {
    try {
      await api.post('/auth/register', form)
      setMessage('Registered successfully. You can now login.')
    } catch (error) {
      setMessage(error.response?.data?.detail || error.message)
    }
  }

  const login = async () => {
    try {
      const res = await api.post('/auth/login', { email: form.email, password: form.password })
      localStorage.setItem('token', res.data.access_token)
      setMessage('Login success. Token saved in localStorage.')
      navigate(`/${form.role}`)
    } catch (error) {
      setMessage(error.response?.data?.detail || error.message)
    }
  }

  return (
    <div className="mb-6 rounded-lg border bg-white p-4 shadow-sm">
      <h2 className="mb-2 text-lg font-semibold">Quick Auth</h2>
      <div className="grid gap-2 md:grid-cols-4">
        <input className="rounded border p-2" name="name" placeholder="Name" value={form.name} onChange={onChange} />
        <input className="rounded border p-2" name="email" placeholder="Email" value={form.email} onChange={onChange} />
        <input className="rounded border p-2" type="password" name="password" placeholder="Password" value={form.password} onChange={onChange} />
        <select className="rounded border p-2" name="role" value={form.role} onChange={onChange}>
          {roles.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </div>
      <div className="mt-3 flex gap-2">
        <button className="rounded bg-emerald-600 px-3 py-2 text-white" onClick={register}>Register</button>
        <button className="rounded bg-blue-600 px-3 py-2 text-white" onClick={login}>Login</button>
      </div>
      {message && <p className="mt-2 text-sm text-slate-700">{message}</p>}
    </div>
  )
}

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between p-4">
          <h1 className="text-xl font-semibold text-blue-700">Remedic Connect</h1>
          <nav className="flex gap-3 text-sm">
            {roles.map((role) => (
              <Link key={role} className="rounded bg-blue-50 px-3 py-1 hover:bg-blue-100" to={`/${role}`}>{role}</Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl p-4">
        <AuthPanel />
        <Routes>
          <Route path="/" element={<Dashboard role="patient" />} />
          {roles.map((role) => <Route key={role} path={`/${role}`} element={<Dashboard role={role} />} />)}
        </Routes>
      </main>
    </div>
  )
}
