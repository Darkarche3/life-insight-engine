import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

function parseTags(input) {
  if (!input) return [];
  return input
    .split(",")
    .map((t) => t.trim())
    .filter((t) => t.length > 0);
}

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export default function App() {
  const [content, setContent] = useState("");
  const [type, setType] = useState("note");
  const [sentiment, setSentiment] = useState(0.5);
  const [tagsInput, setTagsInput] = useState("");
  const [status, setStatus] = useState("");

  const [search, setSearch] = useState("");
  const [tag, setTag] = useState("");
  const [typeFilter, setTypeFilter] = useState("");

  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState("");

  const queryString = useMemo(() => {
    const params = new URLSearchParams();
    if (search.trim()) params.set("search", search.trim());
    if (tag.trim()) params.set("tag", tag.trim());
    if (typeFilter) params.set("type", typeFilter);
    params.set("limit", "25");
    return params.toString();
  }, [search, tag, typeFilter]);

  async function refresh() {
    setLoading(true);
    setLoadError("");
    try {
      const res = await fetch(`${API_BASE}/entries?${queryString}`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setEntries(data);
    } catch (e) {
      setLoadError(String(e?.message || e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryString]);

  async function onSubmit(e) {
    e.preventDefault();
    setStatus("Saving...");

    const tags = parseTags(tagsInput);

    const res = await fetch(`${API_BASE}/entries`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content,
        type,
        tags,
        sentiment_score: Number(sentiment),
      }),
    });

    if (!res.ok) {
      let detail = "Error saving entry.";
      try {
        const data = await res.json();
        if (data?.detail) detail = data.detail;
      } catch {
        /* empty */
      }
      setStatus(detail);
      return;
    }

    setStatus("Saved!");
    setContent("");
    setTagsInput("");
    await refresh();
  }

  return (
    <div className="page">
      <div className="container">
        <header className="header">
          <h1>Life Insights Engine</h1>
          <p className="subtitle">Capture moments. Find patterns. Build insights.</p>
        </header>

        <section className="card">
          <h2>Add Entry</h2>

          <form className="form" onSubmit={onSubmit}>
            <label>
              Content
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write a note..."
                required
              />
            </label>

            <div className="row">
              <label>
                Type
                <select value={type} onChange={(e) => setType(e.target.value)}>
                  <option value="note">note</option>
                  <option value="habit">habit</option>
                  <option value="reflection">reflection</option>
                </select>
              </label>

              <label>
                Sentiment (0–1)
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={sentiment}
                  onChange={(e) => setSentiment(e.target.value)}
                />
              </label>
            </div>

            <label>
              Tags (comma separated)
              <input
                value={tagsInput}
                onChange={(e) => setTagsInput(e.target.value)}
                placeholder="e.g. gym, work, coding"
              />
            </label>

            <button type="submit">Save Entry</button>
            <p className="status">{status}</p>
          </form>
        </section>

        <section className="card">
          <div className="entriesHeader">
            <h2>Recent Entries</h2>

            <div className="filters">
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search content..."
              />
              <input
                value={tag}
                onChange={(e) => setTag(e.target.value)}
                placeholder="Filter tag..."
              />
              <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
                <option value="">All types</option>
                <option value="note">note</option>
                <option value="habit">habit</option>
                <option value="reflection">reflection</option>
              </select>
              <button type="button" onClick={refresh}>
                Refresh
              </button>
            </div>
          </div>

          {loading && <div className="small">Loading...</div>}
          {loadError && <div className="small">Error: {loadError}</div>}
          {!loading && !loadError && entries.length === 0 && (
            <div className="small">No entries yet.</div>
          )}

          <div className="entries">
            {entries.map((e) => (
              <div key={e.id} className="entry">
                <div className="entryTop">
                  <div>
                    <span className="badge">{e.type}</span>
                    <span className="small"> • {formatDate(e.timestamp)}</span>
                  </div>
                  <div className="small">Sentiment: {Number(e.sentiment_score).toFixed(2)}</div>
                </div>

                <p className="content">{e.content}</p>

                <div className="tags">
                  {(e.tags || []).map((t) => (
                    <span key={t} className="tag">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
