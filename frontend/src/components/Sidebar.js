import React from "react";
import "./Sidebar.css";

const Sidebar = ({ isVisible, onCategoryChange }) => {
  const categories = [
    "政治", "國際", "科技", "兩岸", "財經", "旅遊", "健康", "生活",
    "社會", "地方", "文化", "運動", "娛樂", "時尚"
  ];

  return (
    <div className={`sidebar ${isVisible ? "visible" : ""}`}>
      <div className="category-list">
        {categories.map((category, index) => (
          <div
            key={index}
            className="category-item"
            onClick={() => onCategoryChange(category)}
          >
            {category}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
