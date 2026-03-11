import { useState } from 'react'
import { api } from '../lib/api'

const widgets = {
  patient: ['View Reports', 'Create Medicine Order', 'Share Report'],
  lab: ['Upload Report', 'List Reports', 'Verification Status'],
  pharmacy: ['View Orders', 'Process Orders', 'Dispatch Tracking'],
  doctor: ['Review Reports', 'Prescribe Medicines', 'Clinical Notes'],
  admin: ['Approve Labs', 'Approve Pharmacies', 'Audit Logs'],
}

export default function Dashboard({ role }) {
  const [result, setResult] = useState('')

  const checkService = async () => {
    const map = {
      patient: '/patient/reports',
      lab: '/lab/reports',
      pharmacy: '/pharmacy/orders',
      doctor: '/patient/reports',
      admin: '/admin/users',
    }
    try {
      const token = localStorage.getItem('token')
      const res = await api.get(map[role], {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      })
      setResult(JSON.stringify(res.data).slice(0, 250))
    } catch (error) {
      setResult(error.response?.data?.detail || error.message)
    }
  }

  return (
    <section>
      <h2 className="mb-4 text-2xl font-bold capitalize">{role} Dashboard</h2>
      <div className="grid gap-4 md:grid-cols-3">
        {widgets[role].map((item) => (
          <article key={item} className="rounded-lg border bg-white p-4 shadow-sm">
            <h3 className="font-semibold">{item}</h3>
          </article>
        ))}
      </div>
      <button className="mt-6 rounded bg-blue-600 px-4 py-2 text-white" onClick={checkService}>
        Check {role} API
      </button>
      {result && <pre className="mt-3 overflow-x-auto rounded bg-slate-900 p-3 text-xs text-green-300">{result}</pre>}
    </section>
  )
}
