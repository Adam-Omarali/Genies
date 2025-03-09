"use client";
import { useState, useRef, useEffect } from "react";

interface FilterBarProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  selectedDamages: number[];
  setSelectedDamages: (damages: number[]) => void;
}

export default function FilterBar({
  searchQuery,
  setSearchQuery,
  selectedDamages,
  setSelectedDamages,
}: FilterBarProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleDamageToggle = (damage: number) => {
    if (selectedDamages.includes(damage)) {
      setSelectedDamages(selectedDamages.filter((d) => d !== damage));
    } else {
      setSelectedDamages([...selectedDamages, damage]);
    }
  };

  const handleAllDamagesToggle = () => {
    if (selectedDamages.length === 5) {
      setSelectedDamages([]);
    } else {
      setSelectedDamages([1, 2, 3, 4, 5]);
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="flex flex-col md:flex-row gap-4 mb-8">
      <div className="flex-1">
        <input
          type="text"
          placeholder="Search books..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 rounded-lg bg-white border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
        />
      </div>
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 flex items-center gap-2"
        >
          <span>Filter by Condition</span>
          <svg
            className={`w-4 h-4 transition-transform ${
              isOpen ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        {isOpen && (
          <div className="absolute right-0 mt-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
            <div className="p-3 border-b border-gray-200">
              <label className="flex items-center gap-2 text-gray-700 cursor-pointer hover:bg-gray-100 p-2 rounded-md">
                <input
                  type="checkbox"
                  checked={selectedDamages.length === 5}
                  onChange={handleAllDamagesToggle}
                  className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="whitespace-nowrap font-medium">
                  All Conditions
                </span>
              </label>
            </div>
            <div className="p-3">
              {[1, 2, 3, 4, 5].map((damage) => (
                <label
                  key={damage}
                  className="flex items-center gap-2 text-gray-700 cursor-pointer hover:bg-gray-100 p-2 rounded-md"
                >
                  <input
                    type="checkbox"
                    checked={selectedDamages.includes(damage)}
                    onChange={() => handleDamageToggle(damage)}
                    className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="whitespace-nowrap">
                    Level {damage}
                    <span className="text-gray-500 text-sm ml-1">
                      ({getDamageLabel(damage)})
                    </span>
                  </span>
                </label>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function getDamageLabel(damage: number): string {
  switch (damage) {
    case 1:
      return "Like New";
    case 2:
      return "Minor Wear";
    case 3:
      return "Moderate Wear";
    case 4:
      return "Significant Wear";
    case 5:
      return "Heavy Wear";
    default:
      return "";
  }
}
