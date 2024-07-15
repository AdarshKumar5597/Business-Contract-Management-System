import { NERItems, ValidatorItems, SummarizerItems, ClassifyItems } from "@/data";
import Approach from "@/components/Approach";
import Contributions from "@/components/Contributions";
import { FloatingNav } from "@/components/FloatingNav";
import Footer from "@/components/Footer";
import Grid from "@/components/Grid";
import Hero from "@/components/Hero";
import { navItems } from "@/data";;

export default function Home() {
  return (
    <main className="relative bg-black-100 flex justify-center items-center flex-col mx-auto sm:px-10 px-5 overflow-clip">
      <div className="max-w-7xl w-full">
        <h1>
          <FloatingNav navItems={navItems}/>
          <Hero />
          <Grid items={NERItems} num={1} linkText={"ner"}/>
          <Grid items={ValidatorItems} num={2} linkText={"compare"}/>
          <Grid items={SummarizerItems} num={3} linkText={"summarize"}/>
          <Grid items={ClassifyItems} num={4} linkText={"classify"}/>
          <Contributions />
          <Approach />
          <Footer />
        </h1>
      </div>
    </main>
  );
}
