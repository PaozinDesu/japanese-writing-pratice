import type { Metadata } from "next";
import { Zen_Kaku_Gothic_New, Shippori_Mincho, Klee_One } from "next/font/google";
import { Header } from "@/components/layout/header";
import "./globals.css";

const zenKakuGothicNew = Zen_Kaku_Gothic_New({
  variable: "--font-zen-kaku-gothic-new",
  subsets: ["latin"],
  weight: ["400", "500", "700"],
});

const shipporiMincho = Shippori_Mincho({
  variable: "--font-shippori-mincho",
  subsets: ["latin"],
  weight: ["500", "700"],
});

const kleeOne = Klee_One({
  variable: "--font-klee-one",
  subsets: ["latin"],
  weight: ["400", "600"],
});

export const metadata: Metadata = {
  title: "Kaku — aprenda a escrever japonês",
  description:
    "Pratique hiragana, katakana e os 2.136 kanji de uso comum: reconhecimento de traço, leitura e acompanhamento de progresso.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body
        className={`${zenKakuGothicNew.variable} ${shipporiMincho.variable} ${kleeOne.variable} antialiased`}
      >
        <Header />
        <div className="pb-24 md:pb-0">{children}</div>
      </body>
    </html>
  );
}
