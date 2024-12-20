'use client';

import React, { useState, useEffect } from "react";
import axios from "axios";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import Footer from "./components/Footer";
import "./App.css";

const App = () => {
  const [category, setCategory] = useState("");
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isSidebarVisible, setIsSidebarVisible] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  useEffect(() => {
    const fetchNews = async () => {
      if (!category) return;

      setLoading(true);
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/news?category=${category}`);
        setNews(res.data);
      } catch (error) {
        console.error("Failed to fetch news:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, [category]);

  return (
    <div className="app-container">
      <Header
        resetCategory={() => setCategory("")}
        toggleSidebar={toggleSidebar}
        isSidebarVisible={isSidebarVisible}
      />
      <Sidebar
        isVisible={isSidebarVisible}
        onCategoryChange={(selectedCategory) => {
          setCategory(selectedCategory);
        }}
      />
      <div
        className={`main-content-container ${isSidebarVisible ? "with-sidebar" : ""}`}
      >
        {category ? (
          <MainContent news={news} loading={loading} />
        ) : (
          <div className="welcome-message">
            <h2>歡迎使用新聞摘要</h2>
            <p>請點擊左上角的選單來選擇分類</p>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default App;
