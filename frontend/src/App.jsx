import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [articles, setArticles] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]);
  const [sources, setSources] = useState([]);
  const [tags, setTags] = useState([]);

  const [selectedSource, setSelectedSource] = useState("All");
  const [selectedTag, setSelectedTag] = useState("All");

  useEffect(() => {
    fetch("https://archibaldnews-backend.onrender.com/news/today")
      .then((res) => res.json())
      .then((data) => {
        setArticles(data);
        setFilteredArticles(data);

        const allSources = Array.from(new Set(data.map((a) => a.source))).sort();
        setSources(["All", ...allSources]);

        const allTags = Array.from(new Set(data.flatMap((a) => a.tags || []))).sort();
        setTags(["All", ...allTags]);
      });
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

      <ul>
        {filteredArticles.map((article, i) => (
          <li key={i} style={{ marginBottom: "20px", textAlign: "left" }}>
            <a href={article.link} target="_blank" rel="noopener noreferrer"><strong>{article.title}</strong></a>
            <div><em>{article.source}</em></div>
            {article.tags && article.tags.length > 0 && (
              <div>Tags: {article.tags.join(", ")}</div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;