"use client";

import { useState, useEffect, use } from "react";
import Image from "next/image";
import { useCart } from "@/context/CartContext";

interface Book {
  name: string;
  author: string;
  price: number;
  discount: number;
  img: string;
  "damage-level": number;
  type: string;
  publisher: string;
  sold: boolean;
}

interface BookPageProps {
  params: Promise<{
    name: string;
  }>;
}

export default function BookPage({ params }: BookPageProps) {
  const { name } = use(params);
  const [book, setBook] = useState<Book | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { addToCart } = useCart();

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/books`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch books");
        }
        const data = await response.json();
        const foundBook = data.books.find(
          (b: Book) => b.name === decodeURIComponent(name)
        );
        if (!foundBook) {
          throw new Error("Book not found");
        }
        setBook(foundBook);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBook();
  }, [name]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
        <div className="text-gray-700">Loading book details...</div>
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
        <div className="text-red-600">Error: {error}</div>
      </div>
    );
  }

  const handleQuantityChange = (change: number) => {
    const newQuantity = quantity + change;
    if (newQuantity >= 1) {
      setQuantity(newQuantity);
    }
  };

  const handleAddToCart = () => {
    if (book) {
      addToCart({
        name: book.name,
        author: book.author,
        price: book.price,
        discount: book.discount,
        img: book.img,
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Left side - Images */}
          <div className="w-full md:w-1/2 space-y-4">
            <div className="aspect-[3/4] relative rounded-lg overflow-hidden">
              <Image
                src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/${book.img}`}
                alt={book.name}
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 50vw"
                priority
              />
            </div>
          </div>

          {/* Right side - Details */}
          <div className="w-full md:w-1/2">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              {book.name}
            </h1>
            <p className="text-xl text-gray-600 mb-4">{book.author}</p>

            <div className="space-y-6">
              {/* Price and Discount */}
              <div className="flex items-baseline gap-4">
                <span className="text-3xl font-bold text-gray-900">
                  ${book.price}
                </span>
                {book.discount > 0 && (
                  <span className="text-lg text-red-600">
                    {book.discount * 100}% off
                  </span>
                )}
              </div>

              {/* Book Details Grid */}
              <div className="grid grid-cols-1 gap-4">
                {/* Quality Rating */}
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-700 min-w-24">
                    Quality:
                  </span>
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <svg
                        key={i}
                        className={`w-4 h-4 ${
                          i < 6 - book["damage-level"]
                            ? "text-yellow-400"
                            : "text-gray-300"
                        }`}
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    ))}
                  </div>
                </div>

                {/* Damage Type */}
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-700 min-w-24">
                    Damage:
                  </span>
                  <span className="text-gray-600">{book.type}</span>
                </div>

                {/* Publisher */}
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-700 min-w-24">
                    Publisher:
                  </span>
                  <span className="text-gray-600">{book.publisher}</span>
                </div>
              </div>

              {/* Quantity Selector */}
              <div>
                <p className="text-gray-700 font-medium mb-2">Quantity</p>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => handleQuantityChange(-1)}
                    className="w-10 h-10 rounded-lg border border-gray-300 flex items-center justify-center hover:bg-gray-100 text-gray-700 text-xl font-medium"
                  >
                    -
                  </button>
                  <span className="text-xl text-gray-900">{quantity}</span>
                  <button
                    onClick={() => handleQuantityChange(1)}
                    className="w-10 h-10 rounded-lg border border-gray-300 flex items-center justify-center hover:bg-gray-100 text-gray-700 text-xl font-medium"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Add to Cart Button */}
              <button
                onClick={handleAddToCart}
                className="w-full py-3 px-6 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add To Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
