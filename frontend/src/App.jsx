import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [articles, setArticles] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]);
  const [sources, setSources] = useState([]);
  const [tags, setTags] = useState([]);
  const [selectedSource, setSelectedSource] = useState("All");
  const [selectedTag, setSelectedTag] = useState("All");
  const [visibleCount, setVisibleCount] = useState(9);

  const ARTICLES_PER_PAGE = 9;

  useEffect(() => {
    fetch("https://archibaldnews-backend.onrender.com/news/today")
      .then((res) => res.json())
      .then((data) => {
        console.log("✅ Raw article data:", data);
        setArticles(data);
        setFilteredArticles(data);

        const allSources = Array.from(new Set(data.map((a) => a.source))).sort();
        setSources(["All", ...allSources]);

        const allTags = Array.from(new Set(data.flatMap((a) => a.tags || []))).sort();
        setTags(["All", ...allTags]);
      })
      .catch((err) => console.error("❌ Failed to fetch articles:", err));
  }, []);

  useEffect(() => {
    let filtered = articles;

    if (selectedSource !== "All") {
      filtered = filtered.filter((a) => a.source === selectedSource);
    }

    if (selectedTag !== "All") {
      filtered = filtered.filter((a) => (a.tags || []).includes(selectedTag));
    }

    setFilteredArticles(filtered);
    setVisibleCount(ARTICLES_PER_PAGE); // Reset on filter change
  }, [selectedSource, selectedTag, articles]);

  return (
    <div className="App">
      <h1>🗞️ Archibald News</h1>

      <div style={{ marginBottom: "1rem" }}>
        <label>
          Source:{" "}
          <select value={selectedSource} onChange={(e) => setSelectedSource(e.target.value)}>
            {sources.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </label>

        <label style={{ marginLeft: "1rem" }}>
          Tag:{" "}
          <select value={selectedTag} onChange={(e) => setSelectedTag(e.target.value)}>
            {tags.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="card-grid">
        {filteredArticles.slice(0, visibleCount).map((article, i) => (
          <div className="card" key={i}>
            <img
              src={article.image || "https://placehold.co/300x200?text=No+Image"}
              alt={article.title}
              className="card-image"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "https://placehold.co/300x200?text=No+Image";
              }}
            />
            <div className="card-content">
              <a href={article.link} target="_blank" rel="noopener noreferrer">
                <h3 className="card-title">{article.title}</h3>
              </a>

              <div className="card-meta">
                {article.author && article.author !== "Unknown" && (
                  <p className="card-author">🖊️ {article.author}</p>
                )}
                {article.published && (
                  <p className="card-date">
                    📅 {new Date(article.published).toLocaleDateString("en-IN", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </p>
                )}
              </div>

              <p className="card-source">{article.source}</p>

              {article.tags && article.tags.length > 0 && (
                <div className="card-tags">
                  {article.tags.map((tag, idx) => (
                    <span className="tag" key={idx}>{tag}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Load More button */}
      {visibleCount < filteredArticles.length && (
        <div style={{ textAlign: "center", marginTop: "2rem" }}>
          <button className="load-more" onClick={() => setVisibleCount(prev => prev + ARTICLES_PER_PAGE)}>
            Load More
          </button>
        </div>
      )}
    </div>
  );
}

export default App;