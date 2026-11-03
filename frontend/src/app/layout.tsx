import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AccountIQ — Enterprise Intelligence Platform",
  description: "Evidence-driven Account and Contact Intelligence Platform for Zscaler Enterprise Sales",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        {children}
      </body>
    </html>
  );
}
