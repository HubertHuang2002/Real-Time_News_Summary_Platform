import React from "react";
import "./MainContent.css";

const MainContent = ({ news, loading }) => {
  return (
    <div className="main-content-container">
      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="news-grid">
          {news.map((item, index) => (
            <article
              key={index}
              id={`post-${index}`}
              className="news-card"
            >
              <h3 className="entry-title">
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.title}
                </a>
              </h3>
              <div className="post-content">
                <div className="post-content-inner">
                  <p dangerouslySetInnerHTML={{ __html: item.content.replace(/"/g, '') }}></p>
                </div>
                <a
                  href={item.url}
                  className="more-link"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  read more
                </a>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
};

export default MainContent;
