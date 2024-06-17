import type { Metadata } from "next";
import "../globals.css";

export const metadata: Metadata = {
  title: "Scan",
  description: "Scan",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      {children}
    </>
  );
}
