import '../styles/globals.css'
import type { AppProps } from 'next/app'

const config = {
  backendUrl: String(process.env.NEXT_PUBLIC_BACKEND_URL),
  masterDocumentUri: String(process.env.NEXT_PUBLIC_MASTER_DOCUMENT_URI)
}

const validateConfig = () => {
  if (!config.backendUrl) {
    throw new Error('NEXT_PUBLIC_BACKEND_URL is not defined in the environment variables');
  }
  if (!config.masterDocumentUri) {
    throw new Error('NEXT_PUBLIC_MASTER_DOCUMENT_URI is not defined in the environment variables');
  }
}

validateConfig();

function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}

App.config = config;

export default App 