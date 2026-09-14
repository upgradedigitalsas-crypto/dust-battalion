module.exports = async function handler(req, res) {
  const key = process.env.OPENAI_API_KEY;
  if (!key) { res.status(500).json({ error: "missing OPENAI_API_KEY" }); return; }

  const prompt = (req.query.prompt || "").toString();
  if (!prompt) { res.status(400).json({ error: "missing prompt" }); return; }
  const size = (req.query.size || "1536x1024").toString();

  try {
    const r = await fetch("https://api.openai.com/v1/images/generations", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${key}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ model: "gpt-image-1", prompt, size, n: 1 })
    });
    const data = await r.json();
    if (!r.ok) { res.status(r.status).json(data); return; }
    res.status(200).json(data);
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
};
