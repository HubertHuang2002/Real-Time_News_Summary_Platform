import React from "react";
import "./Header.css";

const Header = ({ toggleSidebar, isSidebarVisible, resetCategory }) => {
  const handleLogoClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    resetCategory();
  };
  return (
    <header className="header">
      <button
        className="menu-button"
        onClick={toggleSidebar}
        aria-label="Toggle Menu"
      >
        {isSidebarVisible ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false"
            role="presentation"
            className="icon icon-close"
            fill="none"
            viewBox="0 0 12 12"
          >
            <path
              d="M1 1L11 11"
              stroke="currentColor"
              stroke-linecap="round"
              fill="none"
            ></path>
            <path
              d="M11 1L1 11"
              stroke="currentColor"
              stroke-linecap="round"
              fill="none"
            ></path>
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false"
            role="presentation"
            className="icon icon-hamburger"
            fill="none"
            viewBox="0 0 32 32"
          >
            <path
              d="M0 26.667h32M0 16h26.98M0 5.333h32"
              stroke="currentColor"
            ></path>
          </svg>
        )}
      </button>
      <span className="logo" onClick={handleLogoClick}>
        新聞摘要
      </span>
    </header>
  );
};

export default Header;