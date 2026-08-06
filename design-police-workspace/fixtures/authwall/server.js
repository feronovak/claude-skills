const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const PORT = process.env.PORT || 8877;
const ROOT = path.join(__dirname, "public");
const ORIGIN = `http://127.0.0.1:${PORT}`;

// Dev-only in-memory stores. Production uses Redis; see README.
const magicTokens = new Map();
const sessions = new Set();

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".png": "image/png",
  ".svg": "image/svg+xml",
};

function send(res, code, body, headers = {}) {
  res.writeHead(code, { "content-type": "text/html; charset=utf-8", ...headers });
  res.end(body);
}

function serveFile(res, name) {
  const file = path.join(ROOT, name);
  fs.readFile(file, (err, buf) => {
    if (err) return send(res, 404, "not found");
    res.writeHead(200, { "content-type": TYPES[path.extname(file)] || "application/octet-stream" });
    res.end(buf);
  });
}

function cookies(req) {
  return Object.fromEntries(
    (req.headers.cookie || "")
      .split(";")
      .map((c) => c.trim().split("="))
      .filter((p) => p[0])
  );
}

const PROTECTED = new Set(["/dashboard", "/team"]);

http
  .createServer((req, res) => {
    const url = new URL(req.url, ORIGIN);
    const route = url.pathname.replace(/\/$/, "") || "/";

    if (route === "/") return send(res, 302, "", { location: "/dashboard" });

    if (route === "/login" && req.method === "GET") return serveFile(res, "login.html");

    // Magic-link request. In production this hands off to the mailer; in dev
    // the link is printed to this console, which is the only way in locally.
    if (route === "/login" && req.method === "POST") {
      let body = "";
      req.on("data", (c) => (body += c));
      req.on("end", () => {
        const email = decodeURIComponent(
          (body.split("email=")[1] || "").split("&")[0].replace(/\+/g, " ")
        );
        const token = crypto.randomBytes(16).toString("hex");
        magicTokens.set(token, email);
        console.log("");
        console.log("  ┌─ dev mailer ─────────────────────────────────────────");
        console.log(`  │ magic link for ${email}:`);
        console.log(`  │ ${ORIGIN}/auth/verify?token=${token}`);
        console.log("  └──────────────────────────────────────────────────────");
        console.log("");
        send(res, 200, `<!doctype html><meta charset=utf-8><title>Check your email</title>
          <p style="font:16px system-ui;padding:40px">Magic link sent to ${email}.
          In development it is printed to the dev server console.</p>`);
      });
      return;
    }

    if (route === "/auth/verify") {
      const token = url.searchParams.get("token");
      if (!token || !magicTokens.has(token)) return send(res, 401, "invalid or expired link");
      magicTokens.delete(token);
      const sid = crypto.randomBytes(16).toString("hex");
      sessions.add(sid);
      return send(res, 302, "", {
        location: "/dashboard",
        "set-cookie": `sid=${sid}; Path=/; HttpOnly; SameSite=Lax`,
      });
    }

    if (route === "/logout") {
      sessions.delete(cookies(req).sid);
      return send(res, 302, "", { location: "/login", "set-cookie": "sid=; Path=/; Max-Age=0" });
    }

    if (PROTECTED.has(route)) {
      if (!sessions.has(cookies(req).sid)) return send(res, 302, "", { location: "/login" });
      return serveFile(res, route.slice(1) + ".html");
    }

    // static assets are public
    if (/\.[a-z0-9]+$/i.test(route)) return serveFile(res, route.slice(1));

    send(res, 404, "not found");
  })
  .listen(PORT, "127.0.0.1", () => {
    console.log(`orbit console dev server on ${ORIGIN}`);
    console.log("routes: /login  /dashboard (auth)  /team (auth)");
  });
