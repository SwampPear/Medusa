import subprocess


def app(environ, start_response):
  data = b"<html lang=\"en\"><body><div>one</div><div>two</div></body></html>\n"
  status = '200 OK'
  headers = [
      ("Content-Type", "html"),
      ("Content-Length", str(len(data))),
      ("Custom-Test-Header", "This-Is-A-Test"),
  ]

  start_response(status, headers)
  return iter([data])

