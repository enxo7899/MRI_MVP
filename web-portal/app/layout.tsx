import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Ministria e Shëndetësisë - Platforma AI e Imazherisë',
  description: 'Platforma Kombëtare AI e Imazherisë Mjekësore - Ministria e Shëndetësisë dhe Mbrojtjes Sociale e Republikës së Shqipërisë',
  keywords: ['medical imaging', 'AI', 'Albania', 'Ministry of Health', 'DICOM', 'radiology'],
  authors: [{ name: 'Ministria e Shëndetësisë dhe Mbrojtjes Sociale' }],
  robots: 'noindex, nofollow', // Government internal system
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="sq">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="theme-color" content="#dc2626" />
      </head>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
