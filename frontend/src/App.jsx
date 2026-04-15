import { Link, Route, Routes } from 'react-router-dom';
import { pages } from './pages/pageRegistry';

export default function App() {
  return (
    <div className="shell">
      <aside className="sidebar">
        <h2>ZTA Multi-Cloud</h2>
        <nav>
          {pages.map((p) => (
            <Link key={p.path} to={p.path}>{p.label}</Link>
          ))}
        </nav>
      </aside>
      <main className="content">
        <Routes>
          {pages.map((p) => (
            <Route key={p.path} path={p.path} element={p.component} />
          ))}
        </Routes>
      </main>
    </div>
  );
}
