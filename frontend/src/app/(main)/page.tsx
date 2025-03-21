"use client";

import { useState, useEffect } from "react";
import BookCard from "@/components/BookCard";
import FilterBar from "@/components/FilterBar";

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

interface BooksResponse {
  books: Book[];
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDamages, setSelectedDamages] = useState<number[]>([]);
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/books`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch books");
        }
        const data: BooksResponse = await response.json();
        setBooks(data.books);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBooks();
  }, []);

  const filteredBooks = books.filter((book) => {
    const matchesSearch =
      book.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.author.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesDamage =
      selectedDamages.length === 0 ||
      selectedDamages.includes(book["damage-level"]);

    return matchesSearch && matchesDamage;
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
        <div className="text-gray-700">Loading books...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
        <div className="text-red-600">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="mb-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Books For Sale
        </h1>
        <FilterBar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          selectedDamages={selectedDamages}
          setSelectedDamages={setSelectedDamages}
        />
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredBooks.map((book) => (
          <BookCard
            key={book.name}
            title={book.name}
            author={book.author}
            price={book.price}
            discount={book.discount * 100}
            imageUrl={`${process.env.NEXT_PUBLIC_BACKEND_URL}/${book.img}`}
            damage={book["damage-level"]}
          />
        ))}
      </div>

      {filteredBooks.length === 0 && (
        <div className="text-gray-700 text-center mt-8">
          No books found matching your criteria
        </div>
      )}
    </div>
  );
}
