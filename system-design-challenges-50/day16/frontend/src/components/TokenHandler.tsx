import React, { useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'

const TokenHandler: React.FC = () => {
  const { handleToken } = useAuth()

  useEffect(() => {
    // Get token from URL query parameters
    const urlParams = new URLSearchParams(window.location.search)
    const token = urlParams.get('token')
    
    if (token) {
      handleToken(token)
    }
  }, [handleToken])

  return (
    <div className="token-handler">
      <p>Processing authentication token...</p>
    </div>
  )
}

export default TokenHandler