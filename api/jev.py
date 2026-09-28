from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        api_key = os.environ.get("AI_GATEWAY_API_KEY")

        if not api_key:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "error": "AI_GATEWAY_API_KEY is niet ingesteld"
                }).encode()
            )
            return

        payload = {
            "model": "typesafe-ai/jev",
            "state": (
                "Oracle database alert: ORA-19809. "
                "Fast Recovery Area is 99% full and the archiver is stuck."
            ),
            "questions": {
                "storage_problem": {
                    "type": "boolean",
                    "instructions": (
                        "Is this primarily a storage or capacity related problem?"
                    )
                }
            }
        }

        request = urllib.request.Request(
            "https://ai-gateway.vercel.sh/v1/evaluate",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(request) as response:
                result = json.loads(response.read())

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": str(e)}).encode()
            )