import fs from 'node:fs'
import readline from 'node:readline'
import { Brida } from '@brida/sdk'

if (!process.env.BRIDA_API_KEY) {
  throw new Error('BRIDA_API_KEY is required')
}

const input = process.argv[2]
if (!input) {
  throw new Error('usage: node examples/reflex-audit.mjs <reflex-states.jsonl>')
}

const brida = new Brida({ apiKey: process.env.BRIDA_API_KEY })

const stream = readline.createInterface({
  input: fs.createReadStream(input, { encoding: 'utf8' }),
  crlfDelay: Infinity,
})

for await (const line of stream) {
  if (!line.trim()) continue
  const row = JSON.parse(line)
  const result = await brida.reflex.run('alignment', { state: row.state })
  process.stdout.write(
    JSON.stringify({
      case_id: row.case_id,
      selected_action: row.selected_action,
      expected_branch: row.expected_branch,
      actual_branch: result.decision.branch,
    }) + '\n',
  )
}
