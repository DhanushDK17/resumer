import { useMemo, useState } from "react";

const defaultApi = import.meta.env.VITE_API_URL || "http://192.168.1.67:8000";

function formatFilename(path) {
  if (!path) return "";
  const parts = path.split("/");
  return parts[parts.length - 1] || path;
}

export default function App() {
  const [url, setUrl] = useState("");
  const [template, setTemplate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const isValid = useMemo(() => {
    try {
      const parsed = new URL(url);
      return ["http:", "https:"].includes(parsed.protocol);
    } catch {
      return false;
    }
  }, [url]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!isValid) {
      setError("Enter a valid http(s) job URL.");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("url", url);
      if (template) {
        formData.append("template", template);
      }
      console.log(defaultApi)
      const response = await fetch(`${defaultApi}/generate-resume-file/`, {
        method: "POST",
        body: formData
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || "Request failed. Try again.");
      }
      const blob = await response.blob();
      const disposition = response.headers.get("content-disposition") || "";
      const match = disposition.match(/filename=\"?([^\";]+)\"?/i);
      const filename = match?.[1] || "resume.docx";
      const blobUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(blobUrl);
      const data = { file_path: filename };
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="ambient" aria-hidden="true" />
      <header className="hero">
        <div className="badge">Resumer</div>
        <h1>Turn job URLs into tailored resumes.</h1>
        <p>
          Paste a job post link and let the engine craft an ATS-ready experience
          section in seconds.
        </p>
      </header>

      <main className="card">
        <form onSubmit={handleSubmit} className="form">
          <label htmlFor="jobUrl">Job URL</label>
          <div className="input-row">
            <input
              id="jobUrl"
              type="url"
              placeholder="https://company.com/careers/role"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              autoComplete="off"
              required
            />
            <div className="file-control">
              <input
                id="template"
                type="file"
                accept=".docx"
                onChange={(event) => setTemplate(event.target.files?.[0] || null)}
              />
              <span className="file-name">
                {template?.name || "Your resume"}
              </span>
            </div>
            <button type="submit" disabled={loading}>
              {loading ? "Generating..." : "Generate"}
            </button>
          </div>
        </form>

        <section className="status" aria-live="polite">
          {error && <div className="alert error">{error}</div>}
          {loading && (
            <div className="alert info">
              Generating resume… This can take up to a minute.
            </div>
          )}
          {result?.file_path && (
            <div className="alert success">
              <div>
                <strong>Resume ready.</strong>
                <p>
                  File: <span>{formatFilename(result.file_path)}</span>
                </p>
              </div>
              <button
                type="button"
                onClick={() => navigator.clipboard.writeText(result.file_path)}
              >
                Copy path
              </button>
            </div>
          )}
        </section>
      </main>

      {/* <footer className="footer">
        <div>
          <h2>What happens next</h2>
          <ul>
            <li>We scrape the job description.</li>
            <li>Gemini rewrites your experience section.</li>
            <li>A DOCX is generated and saved locally.</li>
          </ul>
        </div>
      </footer> */}
    </div>
  );
}
