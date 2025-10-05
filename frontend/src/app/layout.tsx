import type React from "react";
import type { Metadata } from "next";
import { Inter, Instrument_Serif } from "next/font/google";
import localFont from "next/font/local";
import "./globals.css";
import { AuthProvider } from "../contexts/AuthContext";
import { ThemeProvider } from "../providers/theme-provider";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
  preload: true,
});

const instrumentSerif = Instrument_Serif({
  subsets: ["latin"],
  variable: "--font-instrument-serif",
  weight: ["400"],
  display: "swap",
  preload: true,
});

const ppMondwest = localFont({
  src: "../../public/fonts/PPMondwest-Regular.otf",
  variable: "--font-pp-mondwest",
  display: "swap",
});

export const metadata: Metadata = {
  title: "FlowAI - Build AI Agent Workflows",
  description:
    "Build, deploy, and manage AI agent workflows effortlessly. The natural language platform for creating intelligent multi-agent systems.",
  appleWebApp: {
    title: "FlowAI",
  },
  metadataBase: new URL("https://flowai.dev"),
  openGraph: {
    title: "FlowAI - AI Agent Workflow Platform",
    description: "Build, deploy, and manage AI agent workflows effortlessly.",
    url: "https://flowai.dev",
    siteName: "FlowAI",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "FlowAI - Build AI Agent Workflows",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "FlowAI - AI Agent Workflow Platform",
    description: "Build, deploy, and manage AI agent workflows effortlessly.",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${instrumentSerif.variable} ${ppMondwest.variable} antialiased`}
      suppressHydrationWarning
    >
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Instrument+Serif:wght@400&display=swap"
        />

        {/* Favicon links for compatibility */}
        <link rel="icon" type="image/x-icon" href="/favicon.ico" />
        <link rel="icon" type="image/svg+xml" href="/icon.svg" />
        <link rel="icon" type="image/png" sizes="32x32" href="/icon.png" />
        <link rel="apple-touch-icon" href="/apple-icon.png" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="apple-mobile-web-app-title" content="FlowAI" />
      </head>
      <body className="font-sans antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <AuthProvider>
            {children}
            <Toaster theme="system" />
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
