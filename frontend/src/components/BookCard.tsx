import Image from "next/image";
import Link from "next/link";

interface BookCardProps {
  title: string;
  author: string;
  price: number;
  discount: number;
  imageUrl: string;
  damage?: number; // Changed to number
}

export default function BookCard({
  title,
  author,
  price,
  discount,
  imageUrl,
}: BookCardProps) {
  return (
    <Link href={`/books/${encodeURIComponent(title)}`}>
      <div className="relative bg-white rounded-lg overflow-hidden shadow-md border border-gray-200 transition-transform hover:scale-[1.02]">
        <div className="aspect-[3/4] relative">
          <Image
            src={imageUrl}
            alt={title}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        </div>
        <div className="p-4">
          <h2 className="text-xl font-bold mb-1 text-gray-900">{title}</h2>
          <p className="text-gray-600 mb-4">{author}</p>
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-lg text-gray-900">${price.toFixed(2)}</span>
            </div>
            <div className="text-sm bg-red-600 text-white px-2 py-1 rounded">
              {discount.toFixed(0)}% OFF
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
