import React, { useEffect, useState } from 'react';

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch("https://archibaldnews-backend.onrender.com/news/today")
      .then(res => res.json())
      .then(data => setArticles(data));
  }, []);

  return (
    <div style={{ backgroundColor: '#121212', color: '#fff', padding: '20px' }}>
      <h1>ArchibaldNews – News Today</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
        {articles.map((a, i) => (
          <div key={i} style={{ backgroundColor: '#1e1e1e', padding: '10px', borderRadius: '8px' }}>
            {a.img && <img src={a.img} alt={a.title} style={{ width: '100%', height: '200px', objectFit: 'cover' }} />}
            <h3>{a.title}</h3>
            <a href={a.link} target="_blank" style={{ color: '#00bcd4' }}>Read More</a>
            <div>{a.tags?.map(tag => <span key={tag} style={{ marginRight: '8px' }}>#{tag}</span>)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
