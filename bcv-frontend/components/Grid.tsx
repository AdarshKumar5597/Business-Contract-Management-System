import { BentoGrid, BentoGridItem } from "./ui/BentoGrid";

type Item = {
  id: number;
  title?: string;
  description?: string;
  className?: string;
  img?: string;
  imgClassName?: string;
  titleClassName?: string;
  spareImg?: string;
  btnText?: string;
};

const Grid = ({ items, num, linkText }: { items: Item[], num: number, linkText: string }) => {
  return (
    <section id="about" className={`${num !== 1 && "border-blue-600 border-t-[3px]"}`}>
      {num === 1 && <h1 className="heading pb-10">
        Fea<span className="text-purple">tures</span>
      </h1>}
      <BentoGrid className="w-full pb-20">
        {items.map((item, i) => (
          <BentoGridItem
            id={item.id}
            key={i}
            title={item.title}
            description={item.description}
            className={item.className}
            img={item.img}
            imgClassName={item.imgClassName}
            titleClassName={item.titleClassName}
            spareImg={item.spareImg}
            btnText={item.btnText}
            linkText={linkText}
          />
        ))}
      </BentoGrid>
    </section>
  );
};

export default Grid;