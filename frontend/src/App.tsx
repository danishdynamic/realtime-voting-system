import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'sonner'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import { HomePage } from '@/pages/HomePage'
import { PollPage } from '@/pages/PollPage'
import { CreatePollPage } from '@/pages/CreatePollPage'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-white font-sans antialiased">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/poll/:pollId" element={<PollPage />} />
            <Route path="/create" element={<CreatePollPage />} />
          </Routes>
        </main>
        <Footer />
        <Toaster 
          position="top-center" 
          richColors 
          toastOptions={{
            style: {
              background: '#1e293b',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#fff',
            },
          }}
        />
      </div>
    </BrowserRouter>
  )
}

export default App