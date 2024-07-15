"use client";
import React, { useEffect } from "react";
import { Worker, Viewer } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

const SummarizedText = ({ pdfUrl }: { pdfUrl: string }) => {

  useEffect(() => {
    const fetchPdf = async () => {
      try {
        if (!pdfUrl) {
          return;
        }
        const response = await fetch(pdfUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/pdf'
          }
        });
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
      } catch (error) {
        console.error('Error fetching PDF:', error);
      }
    };

    fetchPdf();
  }, [pdfUrl]);

  const defaultLayoutPluginInstance = defaultLayoutPlugin();

  return (
    <div className="h-full w-full flex flex-col">
      <div className="w-full flex justify-between items-center py-1 px-3">
        <h1 className="w-full h-[10%] font-bold text-lg">SUMMARY</h1>
      </div>
      <div className="w-full h-[100%] font-body overflow-y-scroll max-h-[100%] p-3">
        {pdfUrl ? (
          <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js`}>
            <Viewer
              fileUrl={pdfUrl}
              plugins={[defaultLayoutPluginInstance]}
            />
          </Worker>
        ) : (
          <p>Loading PDF...</p>
        )}
      </div>
    </div>
  );
};

export default SummarizedText;
