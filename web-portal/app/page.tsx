'use client'

import { useEffect, useState } from 'react'
import { 
  Activity, 
  AlertCircle, 
  Calendar, 
  ChevronRight, 
  Clock, 
  Database, 
  Eye, 
  FileImage, 
  Loader2, 
  RefreshCw, 
  Server, 
  Shield, 
  User,
  Cpu,
  CheckCircle2,
  XCircle,
} from 'lucide-react'

// Types
interface Study {
  ID: string
  MainDicomTags: {
    PatientName?: string
    PatientID?: string
    StudyDate?: string
    StudyDescription?: string
    AccessionNumber?: string
    StudyInstanceUID?: string
  }
  Series?: string[]
  ParentPatient?: string
}

interface SystemStatus {
  pacs: 'online' | 'offline' | 'checking'
  ai: 'online' | 'offline' | 'checking'
  viewer: 'online' | 'offline' | 'checking'
}

// Albanian translations
const translations = {
  header: {
    ministry: 'Ministria e Shëndetësisë dhe Mbrojtjes Sociale',
    platform: 'Platforma Kombëtare AI e Imazherisë Mjekësore',
    republic: 'Republika e Shqipërisë',
  },
  nav: {
    dashboard: 'Paneli Kryesor',
    studies: 'Studimet',
    ai: 'Analiza AI',
    settings: 'Cilësimet',
  },
  dashboard: {
    recentStudies: 'Studimet e Fundit',
    viewAll: 'Shiko të gjitha',
    noStudies: 'Nuk ka studime të disponueshme',
    loading: 'Duke ngarkuar...',
    error: 'Gabim në ngarkimin e të dhënave',
    refresh: 'Rifresko',
  },
  table: {
    patientName: 'Emri i Pacientit',
    patientId: 'ID Pacienti',
    date: 'Data',
    description: 'Përshkrimi',
    modality: 'Modaliteti',
    actions: 'Veprimet',
    view: 'Shiko',
    analyze: 'Analizo',
  },
  status: {
    system: 'Statusi i Sistemit',
    pacs: 'PACS Server',
    ai: 'AI Engine',
    viewer: 'OHIF Viewer',
    online: 'Aktiv',
    offline: 'Joaktiv',
    checking: 'Duke kontrolluar...',
    aiReady: 'AI Gati',
    aiOffline: 'AI Joaktiv',
  },
  stats: {
    totalStudies: 'Studimet Totale',
    todayStudies: 'Sot',
    pendingAi: 'Në Pritje AI',
    completed: 'Të Përfunduara',
  },
  buttons: {
    openImage: 'Hape Imazhin',
    runAi: 'Fillo Analizën AI',
    export: 'Eksporto',
  },
  footer: {
    copyright: '© 2024 Ministria e Shëndetësisë dhe Mbrojtjes Sociale',
    version: 'Versioni 1.0.0',
    support: 'Mbështetje Teknike',
  },
}

// Format date to Albanian format
function formatDate(dateStr: string | undefined): string {
  if (!dateStr) return '-'
  
  // DICOM date format: YYYYMMDD
  if (dateStr.length === 8) {
    const year = dateStr.substring(0, 4)
    const month = dateStr.substring(4, 6)
    const day = dateStr.substring(6, 8)
    return `${day}.${month}.${year}`
  }
  
  return dateStr
}

// Format patient name
function formatPatientName(name: string | undefined): string {
  if (!name) return 'I Panjohur'
  return name.replace(/\^/g, ' ').trim() || 'I Panjohur'
}

export default function DashboardPage() {
  const [studies, setStudies] = useState<Study[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    pacs: 'checking',
    ai: 'checking',
    viewer: 'checking',
  })
  const [totalCount, setTotalCount] = useState(0)

  // Fetch studies from Orthanc
  const fetchStudies = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Get study IDs
      const response = await fetch('/pacs/studies')
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      const studyIds: string[] = await response.json()
      setTotalCount(studyIds.length)
      
      // Get details for recent studies (last 20)
      const recentIds = studyIds.slice(0, 20)
      const studyDetails = await Promise.all(
        recentIds.map(async (id) => {
          const detailRes = await fetch(`/pacs/studies/${id}`)
          if (!detailRes.ok) return null
          return detailRes.json()
        })
      )
      
      setStudies(studyDetails.filter(Boolean) as Study[])
      setSystemStatus(prev => ({ ...prev, pacs: 'online' }))
    } catch (err) {
      console.error('Error fetching studies:', err)
      setError(translations.dashboard.error)
      setSystemStatus(prev => ({ ...prev, pacs: 'offline' }))
    } finally {
      setLoading(false)
    }
  }

  // Check AI status
  const checkAiStatus = async () => {
    try {
      const response = await fetch('/monai/info/')
      setSystemStatus(prev => ({ 
        ...prev, 
        ai: response.ok ? 'online' : 'offline' 
      }))
    } catch {
      setSystemStatus(prev => ({ ...prev, ai: 'offline' }))
    }
  }

  // Check viewer status
  const checkViewerStatus = async () => {
    try {
      const response = await fetch('/viewer/')
      setSystemStatus(prev => ({ 
        ...prev, 
        viewer: response.ok ? 'online' : 'offline' 
      }))
    } catch {
      setSystemStatus(prev => ({ ...prev, viewer: 'offline' }))
    }
  }

  // Initial load
  useEffect(() => {
    fetchStudies()
    checkAiStatus()
    checkViewerStatus()
    
    // Refresh every 60 seconds
    const interval = setInterval(() => {
      fetchStudies()
      checkAiStatus()
    }, 60000)
    
    return () => clearInterval(interval)
  }, [])

  // Open study in OHIF viewer
  const openInViewer = (studyInstanceUID: string) => {
    const viewerUrl = `/viewer/?StudyInstanceUIDs=${studyInstanceUID}`
    window.open(viewerUrl, '_blank')
  }

  // Status indicator component
  const StatusIndicator = ({ status }: { status: 'online' | 'offline' | 'checking' }) => {
    if (status === 'checking') {
      return (
        <span className="inline-flex items-center gap-1.5 text-sm text-slate-500">
          <Loader2 className="w-3 h-3 animate-spin" />
          {translations.status.checking}
        </span>
      )
    }
    
    if (status === 'online') {
      return (
        <span className="inline-flex items-center gap-1.5 text-sm text-emerald-600">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          {translations.status.online}
        </span>
      )
    }
    
    return (
      <span className="inline-flex items-center gap-1.5 text-sm text-red-600">
        <span className="w-2 h-2 rounded-full bg-red-500" />
        {translations.status.offline}
      </span>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="gov-header-gradient text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Top bar */}
          <div className="flex items-center justify-between py-2 text-xs text-slate-300 border-b border-slate-700">
            <span>{translations.header.republic}</span>
            <span className="flex items-center gap-2">
              <Shield className="w-3 h-3" />
              Sistem i Sigurt Qeveritar
            </span>
          </div>
          
          {/* Main header */}
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center gap-4">
              {/* Albanian Coat of Arms Placeholder */}
              <div className="w-14 h-14 rounded-lg bg-white/10 flex items-center justify-center border border-white/20">
                <span className="text-2xl">🇦🇱</span>
              </div>
              
              <div>
                <h1 className="text-lg font-semibold">
                  {translations.header.ministry}
                </h1>
                <p className="text-sm text-slate-300">
                  {translations.header.platform}
                </p>
              </div>
            </div>
            
            {/* AI Status Badge */}
            <div className="flex items-center gap-4">
              {systemStatus.ai === 'online' ? (
                <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-500/20 rounded-full border border-emerald-500/30">
                  <Cpu className="w-4 h-4 text-emerald-400" />
                  <span className="text-sm font-medium text-emerald-300">
                    {translations.status.aiReady}
                  </span>
                </div>
              ) : (
                <div className="flex items-center gap-2 px-3 py-1.5 bg-red-500/20 rounded-full border border-red-500/30">
                  <Cpu className="w-4 h-4 text-red-400" />
                  <span className="text-sm font-medium text-red-300">
                    {translations.status.aiOffline}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="medical-card p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500">{translations.stats.totalStudies}</p>
                <p className="text-2xl font-bold text-slate-900">{totalCount}</p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
                <Database className="w-5 h-5 text-blue-600" />
              </div>
            </div>
          </div>
          
          <div className="medical-card p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500">{translations.stats.todayStudies}</p>
                <p className="text-2xl font-bold text-slate-900">
                  {studies.filter(s => {
                    const today = new Date().toISOString().split('T')[0].replace(/-/g, '')
                    return s.MainDicomTags?.StudyDate === today
                  }).length}
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-emerald-50 flex items-center justify-center">
                <Calendar className="w-5 h-5 text-emerald-600" />
              </div>
            </div>
          </div>
          
          <div className="medical-card p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500">{translations.stats.pendingAi}</p>
                <p className="text-2xl font-bold text-slate-900">0</p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center">
                <Clock className="w-5 h-5 text-amber-600" />
              </div>
            </div>
          </div>
          
          <div className="medical-card p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500">{translations.stats.completed}</p>
                <p className="text-2xl font-bold text-slate-900">0</p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-purple-50 flex items-center justify-center">
                <CheckCircle2 className="w-5 h-5 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content - Studies Table */}
          <div className="lg:col-span-3">
            <div className="medical-card">
              {/* Table Header */}
              <div className="flex items-center justify-between p-4 border-b border-slate-200">
                <div className="flex items-center gap-2">
                  <FileImage className="w-5 h-5 text-slate-600" />
                  <h2 className="text-lg font-semibold text-slate-900">
                    {translations.dashboard.recentStudies}
                  </h2>
                </div>
                <button
                  onClick={fetchStudies}
                  disabled={loading}
                  className="btn-secondary text-sm"
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <RefreshCw className="w-4 h-4" />
                  )}
                  {translations.dashboard.refresh}
                </button>
              </div>
              
              {/* Table Content */}
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-slate-400" />
                  <span className="ml-2 text-slate-500">
                    {translations.dashboard.loading}
                  </span>
                </div>
              ) : error ? (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <AlertCircle className="w-12 h-12 text-red-400 mb-2" />
                  <p className="text-slate-600">{error}</p>
                  <button
                    onClick={fetchStudies}
                    className="mt-4 btn-primary text-sm"
                  >
                    {translations.dashboard.refresh}
                  </button>
                </div>
              ) : studies.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <FileImage className="w-12 h-12 text-slate-300 mb-2" />
                  <p className="text-slate-500">
                    {translations.dashboard.noStudies}
                  </p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>{translations.table.patientName}</th>
                        <th>{translations.table.patientId}</th>
                        <th>{translations.table.date}</th>
                        <th>{translations.table.description}</th>
                        <th className="text-right">{translations.table.actions}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {studies.map((study) => (
                        <tr key={study.ID}>
                          <td>
                            <div className="flex items-center gap-2">
                              <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center">
                                <User className="w-4 h-4 text-slate-500" />
                              </div>
                              <span className="font-medium text-slate-900">
                                {formatPatientName(study.MainDicomTags?.PatientName)}
                              </span>
                            </div>
                          </td>
                          <td className="text-slate-600 font-mono text-sm">
                            {study.MainDicomTags?.PatientID || '-'}
                          </td>
                          <td className="text-slate-600">
                            {formatDate(study.MainDicomTags?.StudyDate)}
                          </td>
                          <td className="text-slate-600">
                            {study.MainDicomTags?.StudyDescription || '-'}
                          </td>
                          <td>
                            <div className="flex items-center justify-end gap-2">
                              <button
                                onClick={() => openInViewer(
                                  study.MainDicomTags?.StudyInstanceUID || study.ID
                                )}
                                className="btn-primary text-sm py-1.5"
                              >
                                <Eye className="w-4 h-4" />
                                {translations.buttons.openImage}
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar - System Status */}
          <div className="lg:col-span-1 space-y-6">
            {/* System Status Card */}
            <div className="medical-card p-4">
              <h3 className="text-sm font-semibold text-slate-900 mb-4 flex items-center gap-2">
                <Activity className="w-4 h-4" />
                {translations.status.system}
              </h3>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <Server className="w-4 h-4 text-slate-400" />
                    <span className="text-sm text-slate-700">
                      {translations.status.pacs}
                    </span>
                  </div>
                  <StatusIndicator status={systemStatus.pacs} />
                </div>
                
                <div className="flex items-center justify-between py-2 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <Cpu className="w-4 h-4 text-slate-400" />
                    <span className="text-sm text-slate-700">
                      {translations.status.ai}
                    </span>
                  </div>
                  <StatusIndicator status={systemStatus.ai} />
                </div>
                
                <div className="flex items-center justify-between py-2">
                  <div className="flex items-center gap-2">
                    <Eye className="w-4 h-4 text-slate-400" />
                    <span className="text-sm text-slate-700">
                      {translations.status.viewer}
                    </span>
                  </div>
                  <StatusIndicator status={systemStatus.viewer} />
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="medical-card p-4">
              <h3 className="text-sm font-semibold text-slate-900 mb-4">
                Veprime të Shpejta
              </h3>
              
              <div className="space-y-2">
                <a
                  href="/viewer"
                  target="_blank"
                  className="flex items-center justify-between p-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center shadow-sm">
                      <Eye className="w-4 h-4 text-blue-600" />
                    </div>
                    <span className="text-sm font-medium text-slate-700">
                      Hap OHIF Viewer
                    </span>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
                </a>
                
                <a
                  href="/pacs"
                  target="_blank"
                  className="flex items-center justify-between p-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center shadow-sm">
                      <Database className="w-4 h-4 text-emerald-600" />
                    </div>
                    <span className="text-sm font-medium text-slate-700">
                      Orthanc Explorer
                    </span>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
                </a>
                
                <a
                  href="/monai/info/"
                  target="_blank"
                  className="flex items-center justify-between p-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center shadow-sm">
                      <Cpu className="w-4 h-4 text-purple-600" />
                    </div>
                    <span className="text-sm font-medium text-slate-700">
                      MONAI Label API
                    </span>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between text-sm text-slate-500">
            <span>{translations.footer.copyright}</span>
            <div className="flex items-center gap-4">
              <span>{translations.footer.version}</span>
              <span>•</span>
              <a href="#" className="hover:text-slate-700">
                {translations.footer.support}
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
