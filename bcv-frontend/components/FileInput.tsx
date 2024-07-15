"use client";
import React, { useState } from "react";
import { TbFileUpload } from "react-icons/tb";
import { FaFileAlt, FaPlayCircle } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { usePathname } from "next/navigation";

type FileInputProps = {
  setPdfUrl: React.Dispatch<React.SetStateAction<string>>;
  displayText: string;
};

const FileInput = ({ setPdfUrl, displayText }: FileInputProps) => {
  const {
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [files, setFiles] = useState<File[]>([]);
  const [currentPdf, setCurrentPdf] = useState<number>(0);
  const pathname = usePathname();

  const handleUploadClick = () => {
    document.getElementById("fileupload")?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (pathname === "/compare" && files.length === 2) {
      toast.error("You can only upload 2 files for comparison");
      return;
    }
    const file = e.target.files?.[0];
    if (file) {
      setFiles([...files, file]);
    }
  };

  const handleFileDelete = (index: number) => {
    const newFiles = files.filter((file, i) => i !== index);
    setFiles(newFiles);
  };

  const handleDragOver = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
  };

  const handleDragEnter = (e: { preventDefault: () => void }) => {
    e.preventDefault();
  };

  const handleDragLeave = (e: { preventDefault: () => void }) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (pathname === "/compare" && files.length === 2) {
      toast.error("You can only upload 2 files for comparison");
      return;
    }
    const file = e.dataTransfer.files[0];
    setFiles([...files, file]);
  };

  const onSubmit = async (data: any) => {

    if (files.length === 0) {
      toast.error("Please upload a file");
      return;
    }


    let loadingToastId;
    try {

      if (pathname === "/ner") {
        loadingToastId = toast.loading("Extracting Entities...");
        const formData = new FormData();
        console.log(files[currentPdf]);
        formData.append("pdfFile", files[currentPdf]);
        const response = await fetch("http://127.0.0.1:5000/ner", {
          method: "POST",
          body: formData,
        });
        const result = await response.json();
        console.log(result);
        toast.dismiss(loadingToastId);
        toast.success("Entities extracted successfully");

        if (result?.success) {
          setPdfUrl(result?.pdfUrl);
        }
      }

      if (pathname === "/compare") {
        loadingToastId = toast.loading("Comparing Files...");
        const formData = new FormData();
        console.log(files[currentPdf]);
        formData.append("originalPdfFile", files[0]);
        formData.append("templatePdfFile", files[1]);
        const response = await fetch("http://127.0.0.1:5000/compare", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        console.log(result);
        toast.dismiss(loadingToastId);
        toast.success("File compared successfully");

        if (result?.success) {
          setPdfUrl(result?.pdfUrl);
        }
      }

      if (pathname === "/classify") {
        loadingToastId = toast.loading("Classifying Files...");
        const formData = new FormData();
        console.log(files[currentPdf]);
        formData.append("originalPdfFile", files[0]);
        formData.append("templatePdfFile", files[1]);
        const response = await fetch("http://127.0.0.1:5000/classify", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        console.log(result);
        toast.dismiss(loadingToastId);
        toast.success("File Classified successfully");

        if (result?.success) {
          setPdfUrl(result?.pdfUrl);
        }
      }

      if (pathname === "/summarize") {
        loadingToastId = toast.loading("Summarizing File...");
        const formData = new FormData();
        console.log(files[currentPdf]);
        formData.append("pdfFile", files[currentPdf]);
        const response = await fetch("http://127.0.0.1:5000/summarize", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        console.log(result);
        toast.dismiss(loadingToastId);
        toast.success("File summarized successfully");

        if (result?.success) {
          setPdfUrl(result?.pdfUrl);
        }
      }
    } catch (error) {
      toast.dismiss(loadingToastId);
      toast.error("Error while summarizing file");
      console.error(error);
    }
  };

  const handleSummarizeIconClick = (index: number) => {
    setCurrentPdf(index);
    document.getElementById("submitButton")?.click();
  };

  return (
    <div
      className="h-[80vh] w-[60%] rounded-md"
      onDragOver={handleDragOver}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {displayText === "Named Entity Recognition" && <h1 className="heading">
        Named <span className="text-purple">Entity</span> Recognition
      </h1>}
      {displayText === "Compare" && <h1 className="heading">
        Co<span className="text-purple">mpa</span>re
      </h1>}
      {displayText === "Summarize" && <h1 className="heading">
        Contract<span className="text-purple">Summarizer</span>
      </h1>}
      {displayText === "Text Classifier" && <h1 className="heading">
        Contract<span className="text-purple"> Classifier</span>
      </h1>}
      <form
        action=""
        encType="multipart/form-data"
        className="p-5 flex flex-col gap-3"
        onSubmit={handleSubmit(onSubmit)}
      >
        {/* Your existing file upload section */}
        <div className="w-full bg-white p-5 rounded-3xl border-[2px] border-dashed border-purple-600 flex flex-col gap-3 items-center">
          <div className="file-upload-icon rounded-full bg-[#EEF2FE] flex items-center justify-center h-[50px] w-[50px]">
            <TbFileUpload className="text-[#4D41E4] font-bold text-3xl" />
          </div>
          <div className="file-upload-text-middle">
            <p className="text-[0.750rem] text-[#586579]">
              <span
                className="font-bold text-[#4D41E4] cursor-pointer"
                onClick={handleUploadClick}
              >
                click here{" "}
              </span>
              to upload your file <span className="font-bold">OR</span> Drag and
              drop your file here
            </p>
          </div>
          <div className="file-upload-supported-format">
            <p className="text-[0.750rem] text-[#CBD1D9]">
              Supported Format: PDF
            </p>
          </div>
          {/* Hidden file input */}
          <input
            type="file"
            className="hidden"
            accept=".pdf"
            id="fileupload"
            name="fileupload"
            onChange={handleFileChange}
          />
        </div>

        {/* Your existing uploaded files section */}
        <div className="overflow-y-scroll max-h-[40vh]">
          {files.length > 0 &&
            files.map((file, index) => (
              <div
                className="mt-3 w-full bg-purple-600 rounded-xl flex flex-col border border-white"
                key={index}
              >
                {/* Displaying file details */}
                <div className="flex w-full p-3">
                  <div className="w-[10%]">
                    <FaFileAlt className="h-[30px] w-[30px]" />
                  </div>
                  <div className="flex flex-col w-[90%]">
                    <div className="flex items-center p-1 w-full justify-between">
                      <p className="font-bold text-white text-xs">
                        {file.name}
                      </p>
                      <div className="flex gap-1">
                        <FaPlayCircle
                          className="h-[20px] w-[20px]"
                          title="summarize"
                          onClick={() => handleSummarizeIconClick(index)}
                        />
                        <button
                          type="submit"
                          className="hidden"
                          id="submitButton"
                        ></button>
                        <MdDelete
                          className="h-[20px] w-[20px]"
                          title="Delete"
                          onClick={() => handleFileDelete(index)}
                        />
                      </div>
                    </div>
                    <div
                      className={`text-gray-400 text-xs font-semibold flex`}
                      style={{ paddingLeft: "10px" }}
                    >
                      {(file.size / 1024).toFixed(2)} KB
                    </div>
                  </div>
                </div>
                <div className="pb-1 px-5 flex items-center justify-center gap-5">
                  <div className="bg-white h-[2px] w-full"></div>
                  <p className="progress-percentage">100%</p>
                </div>
              </div>
            ))}
        </div>
      </form>
    </div>
  );
};

export default FileInput;
