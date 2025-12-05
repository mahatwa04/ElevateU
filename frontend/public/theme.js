// theme.js - toggles dark/light mode and persists choice in localStorage
// Save as frontend/public/theme.js

(function(){
  const root = document.documentElement;
  const key = "elevate_theme";
  function applyTheme(t){
    if(t === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
  }
  // read saved
  const saved = localStorage.getItem(key) || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(saved);

  // expose toggle
  window.toggleTheme = function(){
    const now = root.classList.contains("dark") ? "light" : "dark";
    applyTheme(now);
    localStorage.setItem(key, now);
  };

  // update elements with .theme-toggle buttons
  document.addEventListener("DOMContentLoaded", ()=>{
    const els = document.querySelectorAll(".theme-toggle");
    els.forEach(el => el.addEventListener("click", (e)=>{ e.preventDefault(); window.toggleTheme(); }));
  });
})();
