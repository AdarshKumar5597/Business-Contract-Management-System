"use client";
import FileInput from "@/components/FileInput";
import bgSummarizer from "@/app/assets/summarizerBg.jpg";
import Image from "next/image";
import SummarizedText from "@/components/SummarizedText";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
function Summariser() {
  const [pdfUrl, setPdfUrl] = useState("");
  const pathname = usePathname();
  const [displayText, setDisplayText] = useState("")

  useEffect(() => {
    if (pathname === "/classify") {
      setDisplayText("Text Classifier")
    }
  }, [])

  return (
    <div className="w-[100vw] h-[100vh] flex items-center">
      <div className="w-1/2 h-full flex justify-center items-center">
        <FileInput setPdfUrl={setPdfUrl} displayText={displayText} />
      </div>
      <div className="w-1/2 h-[90vh] relative flex items-center justify-center">
        <Image
          src={bgSummarizer}
          className="h-full w-full absolute bg-contain z-[-1] rounded-md"
          alt="Summarizer Background Image"
        />
        <div className="w-[90%] h-[90%] bg-white/10 rounded-md border-white-20">
          <SummarizedText pdfUrl={pdfUrl} />
        </div>
      </div>
    </div>
  );
}

export default Summariser;
