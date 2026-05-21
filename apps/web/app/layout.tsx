import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "kreppa.is",
  description: "Opinber gögn, einfaldur mælir og smá þjóðarsálarkvíði."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="is">
      <body>
        <div className="shell">
          <nav className="nav" aria-label="Aðalvalmynd">
            <a href="/" className="brand">kreppa.andri.is</a>
            <div className="nav-links">
              <a href="/">Mælir</a>
              <a href="/methodology">Aðferðafræði</a>
              <a href="/data">Gögn</a>
              <a href="https://andri.is">Andri.is</a>
              <a href="https://github.com/AndriGitDev">GitHub</a>
            </div>
          </nav>
        </div>
        {children}
      </body>
    </html>
  );
}
