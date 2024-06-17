import type { Metadata } from "next";
import "../globals.css";


export const metadata: Metadata = {
  title: "Scan Results",
  description: "Scan Results",
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
