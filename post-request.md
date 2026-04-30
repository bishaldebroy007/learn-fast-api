# Post Request

A POST request is one of the most common HTTP methods. It is used when the client (browser, mobile app, or your Next.js frontend) wants to send new data to the server for processing or storage.

In everyday terms:

- GET = “Give me something” (read)

- POST = “Here’s something, please create it” (write)

**Formal definition:** A POST request submits an entity to the specified resource, often causing a change in state or side effects on the server.

In FastAPI, you create a POST endpoint with `@app.post("/path")`.

## Request Body

The request body is the actual data sent by the client in the POST request. It is the payload that accompanies the request, typically in JSON format, but can also be form data, files, etc.

Think of it like this:

- The URL is the address on the envelope.

- The HTTP method (POST) tells the postman what to do.

- The request body is the letter inside – the real content.

**Formal definition:** The request body is the data transmitted from the client to the server in the body of an HTTP request, most commonly used with POST, PUT, and PATCH methods.


