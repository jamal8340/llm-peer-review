
import React, { useState } from 'react'

// Tymczasowo korzystamy z działającego portu 8001.
// Później przeniesiemy adres API do konfiguracji.
const API_URL = 'http://localhost:8001'

export default function PeerReview() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function runExperiment() {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(
        `${API_URL}/api/peer-review/experiments/run`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            case_id: 'case_001',
          }),
        }
      )

      if (!response.ok) {
        const message = await response.text()
        throw new Error(
          `Błąd HTTP ${response.status}: ${message}`
        )
      }

      const data = await response.json()
      setResult(data)

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function downloadResults() {
    if (!result) return

    const content = JSON.stringify(result, null, 2)
    const blob = new Blob([content], {
      type: 'application/json',
    })

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')

    link.href = url
    link.download = 'peer_review_case_001.json'
    link.click()

    URL.revokeObjectURL(url)
  }

  function displayDecision(value) {
    return value === 'accept' ? 'ACCEPT' : 'REJECT'
  }

  return (
    <div className="h-full overflow-y-auto px-8 py-6 text-text">
      <div className="max-w-5xl mx-auto space-y-6">

        <div>
          <h1 className="text-2xl font-bold">
            Peer Review POC
          </h1>
          <p className="text-sm text-text-dim mt-2">
            E2 – Editorial Strategy Optimization
          </p>
        </div>

        <div className="rounded-xl border border-border bg-surface p-6 space-y-4">
          <div>
            <h2 className="text-lg font-semibold">
              Pierwszy eksperyment
            </h2>
            <p className="text-sm text-text-dim mt-2">
              Porównanie dwóch strategii podejmowania
              decyzji redakcyjnych na tych samych recenzjach.
            </p>
          </div>

          <div className="text-sm space-y-2">
            <p>
              <strong>Przypadek:</strong> case_001
            </p>
            <p>
              <strong>Recenzenci:</strong> 3
            </p>
            <p>
              <strong>Strategie:</strong> R1 i R2
            </p>
          </div>

          <button
            onClick={runExperiment}
            disabled={loading}
            className="px-5 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold transition-colors"
          >
            {loading
              ? 'Uruchamianie...'
              : '▶ Uruchom eksperyment'}
          </button>
        </div>

        {error && (
          <div className="rounded-xl border border-red-500 p-4 text-red-400">
            <strong>Wystąpił błąd:</strong>
            <p className="mt-2 text-sm">{error}</p>
          </div>
        )}

        {result && (
          <div className="space-y-5">

            <div className="rounded-xl border border-border bg-surface p-5">
              <h2 className="text-lg font-semibold mb-3">
                Wyniki eksperymentu
              </h2>

              <p className="text-sm">
                <strong>Artykuł:</strong> {result.paper_id}
              </p>

              <p className="text-sm mt-2">
                <strong>Decyzja referencyjna:</strong>{' '}
                {displayDecision(result.expected_decision)}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.results.map((item) => (
                <div
                  key={item.strategy}
                  className="rounded-xl border border-border bg-surface p-5 space-y-3"
                >
                  <p className="text-sm text-text-dim">
                    {item.strategy === 'majority'
                      ? 'R1 – Majority-Based'
                      : 'R2 – Expertise-Weighted'}
                  </p>

                  <h3 className="text-2xl font-bold">
                    {displayDecision(item.recommendation)}
                  </h3>

                  <span
                    className={
                      item.correct
                        ? 'inline-block px-3 py-1 rounded bg-green-500/20 text-green-400 text-sm'
                        : 'inline-block px-3 py-1 rounded bg-red-500/20 text-red-400 text-sm'
                    }
                  >
                    {item.correct
                      ? 'Poprawna decyzja'
                      : 'Błędna decyzja'}
                  </span>

                  <p className="text-sm">
                    <strong>Udział głosów za akceptacją:</strong>{' '}
                    {(item.score * 100).toFixed(2)}%
                  </p>

                  <p className="text-sm text-text-dim">
                    {item.justification}
                  </p>
                </div>
              ))}
            </div>

            <button
              onClick={downloadResults}
              className="px-4 py-2 rounded-lg border border-border hover:bg-surface text-sm"
            >
              ↓ Pobierz wyniki JSON
            </button>

          </div>
        )}

      </div>
    </div>
  )
}
